import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform

# Native Android GPS-Integration über Pyjnius
if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.INTERNET,
        Permission.ACCESS_FINE_LOCATION,
        Permission.ACCESS_COARSE_LOCATION,
        Permission.FOREGROUND_SERVICE,
        Permission.WAKE_LOCK
    ])

class AtlasApp(App):
    def build(self):
        self.title = "Atlas E-Lkw Tracker"
        
        # Telegram Konfiguration
        self.telegram_token = "DEIN_TELEGRAM_BOT_TOKEN"
        self.chat_id = "DEINE_TELEGRAM_CHAT_ID"
        
        self.kontingent_kwh = 180.0  # Standardwert

        # Haupt-Container
        self.root_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # 1. Header / Menüleiste
        top_bar = BoxLayout(size_hint_y=0.1, spacing=10)
        self.title_label = Label(text="ATLAS TRACKER", font_size='20sp', bold=True)
        self.toggle_input_btn = Button(
            text="Eingabe ausblenden", 
            size_hint_x=0.4, 
            on_press=self.toggle_inputs
        )
        top_bar.add_widget(self.title_label)
        top_bar.add_widget(self.toggle_input_btn)
        self.root_layout.add_widget(top_bar)

        # 2. Haupt-Dashboard (Geschwindigkeit & Reichweite)
        dashboard = BoxLayout(orientation='vertical', size_hint_y=0.35, spacing=5)
        self.speed_label = Label(text="0 km/h", font_size='48sp', bold=True)
        self.range_label = Label(text=f"Restreichweite: ~{int(self.kontingent_kwh * 1.2)} km", font_size='20sp')
        dashboard.add_widget(self.speed_label)
        dashboard.add_widget(self.range_label)
        self.root_layout.add_widget(dashboard)

        # 3. Kontingent-Eingabebereich (Ausblendbar im Menü)
        self.input_box = BoxLayout(orientation='horizontal', size_hint_y=0.15, spacing=10)
        self.kontingent_input = TextInput(
            hint_text="Kontingent (kWh)", 
            input_filter='float', 
            multiline=False,
            font_size='18sp'
        )
        self.save_btn = Button(
            text="Speichern", 
            size_hint_x=0.35, 
            on_press=self.save_kontingent,
            background_color=(0.2, 0.6, 1, 1)
        )
        self.input_box.add_widget(self.kontingent_input)
        self.input_box.add_widget(self.save_btn)
        self.root_layout.add_widget(self.input_box)

        # 4. GPS-Datenanzeige ganz unten
        gps_box = BoxLayout(orientation='vertical', size_hint_y=0.25)
        self.gps_status_label = Label(text="GPS: Verbinde...", font_size='14sp')
        self.gps_coords_label = Label(text="Lat: -- | Lon: --", font_size='16sp', bold=True)
        gps_box.add_widget(self.gps_status_label)
        gps_box.add_widget(self.gps_coords_label)
        self.root_layout.add_widget(gps_box)

        # GPS auf Android starten
        if platform == 'android':
            self.start_android_gps()
        else:
            self.gps_status_label.text = "GPS: Modus (Desktop/Test)"

        return self.root_layout

    def toggle_inputs(self, instance):
        """ Blendet das Kontingent-Eingabefeld im Menü/Dashboard ein oder aus """
        if self.input_box.parent:
            self.root_layout.remove_widget(self.input_box)
            self.toggle_input_btn.text = "Eingabe anzeigen"
        else:
            # Fügt das Eingabefeld wieder an Stelle 2 ein
            self.root_layout.add_widget(self.input_box, index=1)
            self.toggle_input_btn.text = "Eingabe ausblenden"

    def save_kontingent(self, instance):
        """ Speichert das eingegebene Kontingent und blendet die Maske aus """
        val = self.kontingent_input.text.strip()
        if val:
            try:
                self.kontingent_kwh = float(val)
                self.range_label.text = f"Restreichweite: ~{int(self.kontingent_kwh * 1.2)} km"
                self.kontingent_input.text = ""
                # Nach dem Speichern automatisch ausblenden
                self.toggle_inputs(None)
            except ValueError:
                pass

    def start_android_gps(self):
        """ Startet die GPS-Abfrage direkt über die Android LocationManager-API """
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Context = autoclass('android.content.Context')
            LocationManager = autoclass('android.location.LocationManager')

            activity = PythonActivity.mActivity
            self.location_manager = activity.getSystemService(Context.LOCATION_SERVICE)

            from jnius import PythonJavaClass, java_method
            class GPSListener(PythonJavaClass):
                __javainterface__ = 'android/location/LocationListener'

                def __init__(self, app):
                    super().__init__()
                    self.app = app

                @java_method('(Landroid/location/Location;)V')
                def onLocationChanged(self, location):
                    lat = location.getLatitude()
                    lon = location.getLongitude()
                    speed = location.getSpeed() * 3.6  # m/s in km/h
                    acc = location.getAccuracy()

                    self.app.update_gps_ui(lat, lon, speed, acc)

                @java_method('(Ljava/lang/String;ILandroid/os/Bundle;)V')
                def onStatusChanged(self, provider, status, extras): pass
                @java_method('(Ljava/lang/String;)V')
                def onProviderEnabled(self, provider): pass
                @java_method('(Ljava/lang/String;)V')
                def onProviderDisabled(self, provider): pass

            self.listener = GPSListener(self)
            self.location_manager.requestLocationUpdates(
                LocationManager.GPS_PROVIDER,
                2000,  # Aktualisierung alle 2 Sekunden
                1,     # Mindestens 1 Meter Bewegung
                self.listener
            )
            self.gps_status_label.text = "GPS: Aktiviert (Warte auf Signal)"
        except Exception as e:
            self.gps_status_label.text = f"GPS-Fehler: {str(e)}"

    def update_gps_ui(self, lat, lon, speed, acc):
        """ Aktualisiert Tacho und GPS-Koordinaten in der Benutzeroberfläche """
        self.speed_label.text = f"{int(speed)} km/h"
        self.gps_status_label.text = f"GPS: Empfang ok (±{int(acc)}m)"
        self.gps_coords_label.text = f"Lat: {lat:.5f} | Lon: {lon:.5f}"

if __name__ == '__main__':
    AtlasApp().run()
