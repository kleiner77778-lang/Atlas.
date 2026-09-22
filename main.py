import json
import math
import os
import random
import threading
import urllib.parse
import urllib.request
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.utils import platform

# --- TELEGRAM EINSTELLUNGEN ---
TELEGRAM_BOT_TOKEN = '8413301731:AAHRM32xA2CkAkrrcf85sqYDR88YK14k3bs'
TELEGRAM_CHAT_ID = '8941361378'


def send_telegram_message(message):
  """Sendet Telegram-Nachrichten via urllib im Hintergrund-Thread (ohne requests/C-Libs)."""

  def _send():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown',
    }
    try:
      data = json.dumps(payload).encode('utf-8')
      req = urllib.request.Request(
          url, data=data, headers={'Content-Type': 'application/json'}
      )
      urllib.request.urlopen(req, timeout=5)
    except Exception as e:
      print(f'Telegram Send Error: {e}')

  threading.Thread(target=_send, daemon=True).start()


def calculate_distance(lat1, lon1, lat2, lon2):
  """Berechnet die Distanz zwischen zwei GPS-Punkten in Kilometern."""
  R = 6371.0
  dlat = math.radians(lat2 - lat1)
  dlon = math.radians(lon2 - lon1)
  a = (
      math.sin(dlat / 2) ** 2
      + math.cos(math.radians(lat1))
      * math.cos(math.radians(lat2))
      * math.sin(dlon / 2) ** 2
  )
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  return R * c


# --- SAFELY LOAD PYJNIUS GPS ---
GPSListener = None
if platform == 'android':
  try:
    from jnius import PythonJavaClass, java_method

    class GPSListener(PythonJavaClass):

      __javainterfaces__ = ['android/location/LocationListener']
      __javacontext__ = 'app'

      def __init__(self, callback):
        super(GPSListener, self).__init__()
        self.callback = callback

      @java_method('(Landroid/location/Location;)V')
      def onLocationChanged(self, location):
        if location:
          lat = location.getLatitude()
          lon = location.getLongitude()
          speed = location.getSpeed() * 3.6  # m/s in km/h
          self.callback(lat, lon, speed)

      @java_method('(Ljava/lang/String;ILandroid/os/Bundle;)V')
      def onStatusChanged(self, provider, status, extras):
        pass

      @java_method('(Ljava/lang/String;)V')
      def onProviderEnabled(self, provider):
        pass

      @java_method('(Ljava/lang/String;)V')
      def onProviderDisabled(self, provider):
        pass

  except Exception as e:
    print(f'GPS Listener Class Error: {e}')


class MatrixRainWidget(Widget):

  def __init__(self, **kwargs):
    super(MatrixRainWidget, self).__init__(**kwargs)
    self.columns = []
    self.bind(size=self._setup_matrix, pos=self._setup_matrix)
    Clock.schedule_interval(self.update_matrix, 0.05)

  def _setup_matrix(self, *args):
    self.canvas.before.clear()
    with self.canvas.before:
      Color(0, 0, 0, 1)
      Rectangle(pos=self.pos, size=self.size)

    col_width = 30
    num_cols = int(self.width / col_width) + 1 if self.width > 0 else 10
    self.columns = []

    for i in range(num_cols):
      self.columns.append({
          'x': self.x + (i * col_width),
          'y': random.randint(0, int(self.height) if self.height > 0 else 800),
          'speed': random.randint(8, 22),
          'length': random.randint(6, 12),
      })

  def update_matrix(self, dt):
    self.canvas.clear()
    with self.canvas:
      for col in self.columns:
        col['y'] -= col['speed']
        if col['y'] < 0:
          col['y'] = self.height + random.randint(10, 100)
          col['speed'] = random.randint(8, 22)

        Color(0, 1, 0, 0.45)
        for j in range(col['length']):
          py = col['y'] + (j * 25)
          if 0 <= py <= self.height:
            Rectangle(pos=(col['x'], py), size=(10, 22))


class MainScreen(FloatLayout):
  pass


KV = '''
<MainScreen>:
    MatrixRainWidget:
        id: matrix_bg

    BoxLayout:
        orientation: 'vertical'
        size_hint: (0.9, 0.6)
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        spacing: 10

        Label:
            text: "ATLAS TRACKER"
            font_size: '22sp'
            bold: True
            color: (0, 1, 0, 1)

        Label:
            text: app.traffic_warning
            font_size: '14sp'
            bold: True
            color: (1, 0.2, 0.2, 1) if app.traffic_alert_active else (0, 0, 0, 0)

        Label:
            text: app.speed_text
            font_size: '64sp'
            bold: True
            color: (1, 1, 1, 1)

        Label:
            text: app.battery_text
            font_size: '22sp'
            bold: True
            color: (0.2, 0.9, 0.3, 1) if app.battery_level > 20 else (1, 0.2, 0.2, 1)

        Label:
            text: app.drive_time_text
            font_size: '20sp'
            bold: True
            color: (0, 1, 0, 1) if app.tracking_active else (1, 0.5, 0, 1)

        Label:
            text: app.distance_text
            font_size: '16sp'
            color: (0.8, 0.8, 0.8, 1)

        Label:
            text: app.coords_text
            font_size: '12sp'
            color: (0.5, 0.5, 0.5, 1)

    Button:
        text: "STOPP & BERICHT" if app.tracking_active else "FAHRT STARTEN"
        font_size: '16sp'
        bold: True
        background_normal: ''
        background_color: (0.8, 0.1, 0.1, 0.85) if app.tracking_active else (0, 0.7, 0, 0.85)
        color: (1, 1, 1, 1)
        size_hint: (0.5, 0.08)
        pos_hint: {'center_x': 0.5, 'y': 0.04}
        on_press: app.toggle_tracking()

    Button:
        text: "≡" if not app.tracking_active else ""
        font_size: '24sp'
        bold: True
        background_normal: ''
        background_color: (0, 0, 0, 0.6) if not app.tracking_active else (0, 0, 0, 0)
        color: (0, 1, 0, 1)
        size_hint: (None, None)
        size: (50, 50) if not app.tracking_active else (0, 0)
        pos_hint: {'right': 0.95, 'y': 0.04}
        on_press: app.toggle_menu() if not app.tracking_active else None

    BoxLayout:
        id: menu_overlay
        orientation: 'vertical'
        size_hint: (0.88, 0.7)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5} if app.menu_open and not app.tracking_active else {'center_x': -2, 'center_y': -2}
        padding: 15
        spacing: 10
        canvas.before:
            Color:
                rgba: 0, 0, 0, 0.95
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: "EINSTELLUNGEN"
            font_size: '18sp'
            bold: True
            color: (0, 1, 0, 1)

        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            Label:
                text: "Akku Stand (%):"
                font_size: '14sp'
            TextInput:
                id: battery_input
                text: str(int(app.battery_level))
                input_filter: 'int'
                multiline: False
                size_hint_x: 0.4

        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            Label:
                text: "Reichweite bei 100% (km):"
                font_size: '13sp'
            TextInput:
                id: max_range_input
                text: str(int(app.max_range_km))
                input_filter: 'int'
                multiline: False
                size_hint_x: 0.4

        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            Label:
                text: "Tageskontingent (Std):"
                font_size: '14sp'
            TextInput:
                id: quota_input
                text: str(app.daily_quota_hours)
                input_filter: 'int'
                multiline: False
                size_hint_x: 0.4

        Button:
            text: "Speichern & Menü Schließen"
            background_color: (0, 0.6, 0, 0.9)
            on_press: app.save_settings(battery_input.text, max_range_input.text, quota_input.text)

        Button:
            text: "Telegram Test-Senden"
            background_color: (0, 0.4, 0.8, 0.8)
            on_press: app.trigger_telegram_status()

        Button:
            text: "Schließen"
            background_color: (0.3, 0.3, 0.3, 0.8)
            on_press: app.toggle_menu()
'''


class AtlasApp(App):

  speed_text = StringProperty('0 km/h')
  battery_text = StringProperty('Akku: 100 % (~450 km)')
  distance_text = StringProperty('Strecke: 0.0 km')
  drive_time_text = StringProperty('Lenkzeit: 00:00:00')
  coords_text = StringProperty('GPS wird initialisiert...')
  traffic_warning = StringProperty('')

  tracking_active = BooleanProperty(False)
  traffic_alert_active = BooleanProperty(False)
  menu_open = BooleanProperty(False)

  battery_level = NumericProperty(100.0)
  max_range_km = NumericProperty(450.0)
  daily_quota_hours = NumericProperty(9)
  drive_seconds = NumericProperty(0)
  total_distance_km = NumericProperty(0.0)

  last_lat = None
  last_lon = None
  current_speed = 0.0

  known_traffic_jam_point = (47.7320, 8.8510)

  def build(self):
    return Builder.load_string(KV)

  def on_start(self):
    Clock.schedule_interval(self.update_timers, 1)
    send_telegram_message('🚀 *Atlas Tracker gestartet* & online.')

    if platform == 'android':
      Clock.schedule_once(self.init_android_gps, 1.5)
    else:
      self.start_gps_desktop()

  def init_android_gps(self, dt):
    try:
      from android.permissions import Permission, request_permissions

      request_permissions(
          [
              Permission.ACCESS_FINE_LOCATION,
              Permission.ACCESS_COARSE_LOCATION,
          ],
          self.on_permissions_result,
      )
    except Exception as e:
      self.coords_text = f'Fehler bei Berechtigung: {e}'

  def on_permissions_result(self, permissions, grants):
    if all(grants):
      self.start_gps_android()
    else:
      self.coords_text = 'GPS-Berechtigung verweigert!'

  def start_gps_android(self):
    try:
      from jnius import autoclass

      PythonActivity = autoclass('org.kivy.android.PythonActivity')
      Context = autoclass('android.content.Context')
      Looper = autoclass('android.os.Looper')

      activity = PythonActivity.mActivity
      self.location_manager = activity.getSystemService(
          Context.LOCATION_SERVICE
      )

      if not self.location_manager.isProviderEnabled('gps'):
        self.coords_text = 'Bitte GPS am Handy aktivieren!'
        return

      if GPSListener:
        self.gps_listener = GPSListener(self.update_gps_ui)
        self.location_manager.requestLocationUpdates(
            'gps', 1000, 0.0, self.gps_listener, Looper.getMainLooper()
        )
        self.coords_text = 'Warte auf GPS-Fix...'
    except Exception as e:
      self.coords_text = f'GPS-Startfehler: {str(e)}'

  def start_gps_desktop(self):
    self.coords_text = 'Desktop-Modus (Simulation)'
    Clock.schedule_interval(self._simulate_movement, 2)

  def update_gps_ui(self, lat, lon, speed):
    self.current_speed = speed
    self.speed_text = f'{int(speed)} km/h'
    self.coords_text = f'Lat: {lat:.4f} | Lon: {lon:.4f}'

    if (
        self.tracking_active
        and self.last_lat is not None
        and self.last_lon is not None
    ):
      delta_km = calculate_distance(self.last_lat, self.last_lon, lat, lon)
      if delta_km > 0.002:
        self.total_distance_km += delta_km
        self.distance_text = f'Strecke: {self.total_distance_km:.1f} km'

        if self.max_range_km > 0:
          consumption_percent = (delta_km / self.max_range_km) * 100.0
          self.battery_level = max(
              0.0, self.battery_level - consumption_percent
          )

        self.update_battery_display()

    self.last_lat = lat
    self.last_lon = lon

    self.check_traffic_ahead(lat, lon)

    if speed > 5 and not self.tracking_active:
      self.tracking_active = True
      self.menu_open = False
      send_telegram_message(
          '🚨 *Fahrt automatisch gestartet!* Geschwindigkeit:'
          f' {int(speed)} km/h'
      )

  def update_battery_display(self):
    remaining_km = int((self.battery_level / 100.0) * self.max_range_km)
    self.battery_text = f'Akku: {int(self.battery_level)} % (~{remaining_km} km)'

  def check_traffic_ahead(self, lat, lon):
    jam_lat, jam_lon = self.known_traffic_jam_point
    dist_to_jam = calculate_distance(lat, lon, jam_lat, jam_lon)

    if 1.5 <= dist_to_jam <= 2.5:
      if not self.traffic_alert_active:
        self.traffic_alert_active = True
        self.traffic_warning = f'⚠️ STAU IN {dist_to_jam:.1f} KM!'
        send_telegram_message(
            f'🛑 *STAU-WARNUNG:* Stau in ca. *{dist_to_jam:.1f} km* voraus!'
        )
    elif dist_to_jam < 1.5 or dist_to_jam > 3.0:
      self.traffic_alert_active = False
      self.traffic_warning = ''

  def toggle_tracking(self):
    if self.tracking_active:
      self.tracking_active = False
      self.send_daily_report()
    else:
      self.tracking_active = True
      self.menu_open = False
      send_telegram_message('▶️ *Lenkzeit-Erfassung manuell gestartet.*')

  def send_daily_report(self):
    hrs = int(self.drive_seconds // 3600)
    mins = int((self.drive_seconds % 3600) // 60)
    secs = int(self.drive_seconds % 60)
    time_formatted = f'{hrs:02d}:{mins:02d}:{secs:02d}'

    avg_speed = (
        (self.total_distance_km / (self.drive_seconds / 3600))
        if self.drive_seconds > 0
        else 0.0
    )
    remaining_quota = max(
        0.0, self.daily_quota_hours - (self.drive_seconds / 3600)
    )
    remaining_km = int((self.battery_level / 100.0) * self.max_range_km)

    report_msg = (
        '📋 *ATLAS TAGESBERICHT*\n'
        '----------------------------\n'
        f'⏱ *Gesamtlenkzeit:* `{time_formatted}`\n'
        f'🛣 *Gefahrene Strecke:* `{self.total_distance_km:.2f} km`\n'
        f'🔋 *Restakku:* `{int(self.battery_level)} % (~{remaining_km} km)`\n'
        f'⚡ *Durchschnitt:* `{avg_speed:.1f} km/h`\n'
        f'⏳ *Restkontingent:* `{remaining_quota:.1f} Std.`\n'
        '----------------------------\n'
        'Fahrt beendet und protokolliert.'
    )
    send_telegram_message(report_msg)

  def toggle_menu(self):
    if not self.tracking_active:
      self.menu_open = not self.menu_open

  def save_settings(self, bat_val, max_range_val, quota_val):
    try:
      if bat_val:
        self.battery_level = float(bat_val)
      if max_range_val:
        self.max_range_km = float(max_range_val)
      if quota_val:
        self.daily_quota_hours = int(quota_val)

      self.update_battery_display()
      send_telegram_message(
          '⚙️ *Einstellungen angepasst:*\nAkku:'
          f' `{int(self.battery_level)} %` | Max: `{int(self.max_range_km)} km`'
          f' | Kontingent: `{self.daily_quota_hours} Std.`'
      )
      self.menu_open = False
    except ValueError:
      pass

  def update_timers(self, dt):
    if self.tracking_active:
      self.drive_seconds += 1
      hrs = int(self.drive_seconds // 3600)
      mins = int((self.drive_seconds % 3600) // 60)
      secs = int(self.drive_seconds % 60)
      self.drive_time_text = f'Lenkzeit: {hrs:02d}:{mins:02d}:{secs:02d}'

      if self.drive_seconds == 16200:
        send_telegram_message(
            '⚠️ *WARNUNG:* 4,5 Stunden Lenkzeit erreicht! Bitte Pause einlegen.'
        )

  def trigger_telegram_status(self):
    msg = (
        '📊 *ATLAS LIVE-STATUS*\nSpeed:'
        f' `{self.speed_text}`\n`{self.battery_text}`\n`{self.drive_time_text}`\n`{self.distance_text}`\n`{self.coords_text}`'
    )
    send_telegram_message(msg)

  def _simulate_movement(self, dt):
    sim_speed = random.randint(50, 85)
    sim_lat = 47.7450 + (self.drive_seconds * 0.0001)
    sim_lon = 8.8450 + (self.drive_seconds * 0.0001)
    self.update_gps_ui(sim_lat, sim_lon, sim_speed)


if __name__ == '__main__':
  AtlasApp().run()
