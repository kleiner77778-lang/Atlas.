import random
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel

# Plyer für Android-GPS-Hardware Zugriff
try:
    from plyer import gps
except ImportError:
    gps = None

# Original Katakana, Zahlen & Matrix-Spezialzeichen
MATRIX_CHARS = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ0123456789ABCDEF$#@%&*"

class MatrixRainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = []
        self.font_size = 18
        self.char_textures = {}
        
        # Texturen einmalig vor-rendern für maximale Performance & Stabilität
        self.preload_textures()
        
        # Reagiert dynamisch auf Bildschirmdrehung / Resizing
        self.bind(size=self.reinit_rain)
        Clock.schedule_once(self.init_rain, 0.1)

    def preload_textures(self):
        for char in MATRIX_CHARS:
            core_label = CoreLabel(text=char, font_size=self.font_size)
            core_label.refresh()
            self.char_textures[char] = core_label.texture

    def init_rain(self, dt):
        self.rebuild_columns()
        Clock.schedule_interval(self.update_rain, 0.05)

    def reinit_rain(self, instance, value):
        self.rebuild_columns()

    def rebuild_columns(self):
        if self.width <= 0 or self.height <= 0:
            return
        num_cols = int(self.width / self.font_size) + 1
        self.cols = []
        for i in range(num_cols):
            self.cols.append({
                'x': i * self.font_size,
                'y': random.randint(0, int(self.height)),
                'speed': random.randint(6, 16),
                'length': random.randint(8, 18),
                'chars': [random.choice(MATRIX_CHARS) for _ in range(25)]
            })

    def update_rain(self, dt):
        self.canvas.clear()
        with self.canvas:
            # Tiefschwarzer Hintergrund
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

            for col in self.cols:
                col['y'] -= col['speed']
                if col['y'] < -col['length'] * self.font_size:
                    col['y'] = self.height + random.randint(10, 100)
                    col['speed'] = random.randint(6, 16)

                for j in range(col['length']):
                    char_y = col['y'] + (j * self.font_size)
                    if 0 <= char_y <= self.height:
                        if j == 0:
                            # Tropfenkopf leuchtet hellgrün/weiß
                            Color(0.85, 1.0, 0.85, 1)
                        else:
                            # Verblassen nach oben
                            alpha = max(0.08, 1.0 - (j / col['length']))
                            Color(0.0, 1.0, 0.25, alpha)

                        # Matrix Glitch Effect
                        if random.random() < 0.05:
                            col['chars'][j] = random.choice(MATRIX_CHARS)

                        char = col['chars'][j]
                        texture = self.char_textures.get(char)
                        if texture:
                            Rectangle(texture=texture, pos=(col['x'], char_y), size=texture.size)

class AtlasApp(App):
    def build(self):
        self.is_tracking = False
        self.current_speed = 0.0
        self.lat = 0.0
        self.lon = 0.0

        root = FloatLayout()

        # Matrix Rain Hintergrund
        self.rain = MatrixRainWidget(size_hint=(1, 1))
        root.add_widget(self.rain)

        # UI Overlay
        ui_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Header Status
        self.header = Label(
            text="[ SYSTEM: ATLAS ONLINE ]",
            font_size='20sp',
            bold=True,
            color=(0, 1, 0, 1),
            size_hint=(1, 0.1)
        )
        ui_layout.add_widget(self.header)

        # GPS Live-Anzeige
        self.gps_label = Label(
            text="GPS: SIGNAL SUCHE...",
            font_size='14sp',
            color=(0.2, 0.8, 0.2, 0.9),
            size_hint=(1, 0.1)
        )
        ui_layout.add_widget(self.gps_label)

        # Stauwarner Banner
        self.traffic_label = Label(
            text="[ STAUWARNER: INAKTIV ]",
            font_size='16sp',
            bold=True,
            color=(0, 0.8, 1, 1),
            size_hint=(1, 0.1)
        )
        ui_layout.add_widget(self.traffic_label)

        # Freifläche für den Regeneffekt
        ui_layout.add_widget(BoxLayout(size_hint=(1, 0.5)))

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
        
        # Überprüft alle 10 Sekunden die Verkehrslage/Geschwindigkeit
        Clock.schedule_interval(self.check_traffic, 10)

        return root

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
        self.current_speed = kwargs.get('speed', 0.0) * 3.6  # m/s in km/h
        self.gps_label.text = f"LAT: {self.lat:.5f} | LON: {self.lon:.5f} | V: {self.current_speed:.1f} km/h"

    def check_traffic(self, dt):
        if not self.is_tracking:
            return

        if self.current_speed < 15.0 and self.current_speed > 1.0:
            self.traffic_label.text = "⚠️ WARNUNG: ZÄHFLIESSENDER VERKEHR / STAU!"
            self.traffic_label.color = (1, 0.5, 0, 1)
        elif self.current_speed <= 1.0:
            self.traffic_label.text = "🛑 WARNUNG: STILLSTAND DETEKTIERT"
            self.traffic_label.color = (1, 0, 0, 1)
        else:
            self.traffic_label.text = "🟢 FREIE FAHRT AUF DER ROUTE"
            self.traffic_label.color = (0, 1, 0.3, 1)

if __name__ == '__main__':
    AtlasApp().run()
