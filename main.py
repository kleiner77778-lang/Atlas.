from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# Plyer für Android-GPS-Hardware Zugriff
try:
    from plyer import gps
except ImportError:
    gps = None

class AtlasApp(App):
    def build(self):
        self.is_tracking = False
        self.current_speed = 0.0
        self.lat = 0.0
        self.lon = 0.0

        root = FloatLayout()

        # Schwarz-Hintergrund
        with root.canvas.before:
            Color(0, 0, 0, 1)
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self.update_bg, size=self.update_bg)

        # Haupt-UI Layout
        ui_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Header Status
        self.header = Label(
            text="[ SYSTEM: ATLAS ONLINE ]",
            font_size='20sp',
            bold=True,
            color=(0, 1, 0, 1),
            size_hint=(1, 0.15)
        )
        ui_layout.add_widget(self.header)

        # GPS Live-Anzeige
        self.gps_label = Label(
            text="GPS: SIGNAL SUCHE...",
            font_size='14sp',
            color=(0.2, 0.8, 0.2, 0.9),
            size_hint=(1, 0.15)
        )
        ui_layout.add_widget(self.gps_label)

        # Stauwarner Banner
        self.traffic_label = Label(
            text="[ STAUWARNER: INAKTIV ]",
            font_size='15sp',
            bold=True,
            color=(0, 0.8, 1, 1),
            size_hint=(1, 0.2),
            text_size=(None, None),
            halign='center',
            valign='middle'
        )
        ui_layout.add_widget(self.traffic_label)

        # Freiraum in der Mitte
        ui_layout.add_widget(BoxLayout(size_hint=(1, 0.3)))

        # Tracking Start/Stop Button
        self.btn = Button(
            text="[ TRACKING STARTEN ]",
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0, 0.4, 0.1, 0.85),
            color=(0, 1, 0, 1),
            size_hint=(1, 0.2)
        )
        self.btn.bind(on_press=self.toggle_tracking)
        ui_layout.add_widget(self.btn)

        root.add_widget(ui_layout)
        
        Clock.schedule_interval(self.check_traffic, 10)
        return root

    def update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def toggle_tracking(self, instance):
        self.is_tracking = not self.is_tracking
        if self.is_tracking:
            self.btn.text = "[ TRACKING STOPPEN ]"
            self.btn.background_color = (0.6, 0, 0, 0.85)
            self.btn.color = (1, 0.3, 0.3, 1)
            self.header.text = "[ TRACKING AKTIV ]"
            self.traffic_label.text = "[ STAUWARNER: SCANNE ROUTE... ]"
            self.start_gps()
        else:
            self.btn.text = "[ TRACKING STARTEN ]"
            self.btn.background_color = (0, 0.4, 0.1, 0.85)
            self.btn.color = (0, 1, 0, 1)
            self.header.text = "[ SYSTEM: ATLAS ONLINE ]"
            self.traffic_label.text = "[ STAUWARNER: INAKTIV ]"
            self.traffic_label.color = (0, 0.8, 1, 1)
            self.stop_gps()

    def start_gps(self):
        try:
            if gps:
                gps.configure(on_location=self.on_gps_location)
                gps.start(minTime=2000, minDistance=1)
        except Exception as e:
            self.gps_label.text = f"GPS FEHLER: {str(e)}"

    def stop_gps(self):
        try:
            if gps:
                gps.stop()
                self.gps_label.text = "GPS: INAKTIV"
        except Exception:
            pass

    def on_gps_location(self, **kwargs):
        self.lat = kwargs.get('lat', 0.0)
        self.lon = kwargs.get('lon', 0.0)
        self.current_speed = kwargs.get('speed', 0.0) * 3.6
        self.gps_label.text = f"LAT: {self.lat:.5f} | LON: {self.lon:.5f}\nV: {self.current_speed:.1f} km/h"

    def check_traffic(self, dt):
        if not self.is_tracking:
            return

        if self.current_speed < 15.0 and self.current_speed > 1.0:
            self.traffic_label.text = "⚠️ WARNUNG:\nZÄHFLIESSENDER VERKEHR"
            self.traffic_label.color = (1, 0.5, 0, 1)
        elif self.current_speed <= 1.0:
            self.traffic_label.text = "🛑 WARNUNG:\nSTILLSTAND DETEKTIERT"
            self.traffic_label.color = (1, 0, 0, 1)
        else:
            self.traffic_label.text = "🟢 FREIE FAHRT AUF DER ROUTE"
            self.traffic_label.color = (0, 1, 0.3, 1)

if __name__ == '__main__':
    AtlasApp().run()
