import random
import threading
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel

# Plyer für Android-GPS-Hardware und Sprachausgabe
try:
    from plyer import gps, tts
except ImportError:
    gps = None
    tts = None

# -------------------------------------------------------------
# TELEGRAM KONFIGURATION (Trage hier deine Daten ein!)
# -------------------------------------------------------------
TELEGRAM_BOT_TOKEN = "DEIN_BOT_TOKEN_HIER"
TELEGRAM_CHAT_ID = "DEINE_CHAT_ID_HIER"

MATRIX_CHARS = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ0123456789ABCDEF$#@%&*"

class MatrixRainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = []
        self.font_size = 18
        self.char_textures = {}
        self.preload_textures()
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
                            Color(0.85, 1.0, 0.85, 1)
                        else:
                            alpha = max(0.08, 1.0 - (j / col['length']))
                            Color(0.0, 1.0, 0.25, alpha)

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
        self.last_status = ""

        self.root_layout = FloatLayout()

        # 1. Matrix Rain Hintergrund
        self.rain = MatrixRainWidget(size_hint=(1, 1))
        self.root_layout.add_widget(self.rain)

        # 2. Oberes Banner
        self.top_bar = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.08),
            pos_hint={'top': 1},
            padding=[10, 5],
            spacing=10
        )
        with self.top_bar.canvas.before:
            Color(0, 0, 0, 0.75)
            self.bar_rect = Rectangle(pos=self.top_bar.pos, size=self.top_bar.size)
        self.top_bar.bind(pos=self.update_bar_rect, size=self.update_bar_rect)

        self.banner_label = Label(
            text="[ ATLAS: ONLINE ]",
            font_size='14sp',
            bold=True,
            color=(0, 1, 0, 1),
            halign='left',
            valign='middle'
        )
        self.banner_label.bind(size=self.banner_label.setter('text_size'))

        self.menu_btn = Button(
            text="⚙️ MENÜ",
            size_hint=(0.3, 1),
            background_normal='',
            background_color=(0, 0.3, 0.1, 0.9),
            color=(0, 1, 0, 1),
            bold=True
        )
        self.menu_btn.bind(on_press=self.toggle_menu)

        self.top_bar.add_widget(self.banner_label)
        self.top_bar.add_widget(self.menu_btn)
        self.root_layout.add_widget(self.top_bar)

        # 3. Hauptmenü Overlay
        self.menu_overlay = BoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.55),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            padding=20,
            spacing=15
        )
        with self.menu_overlay.canvas.before:
            Color(0, 0, 0, 0.88)
            self.overlay_rect = Rectangle(pos=self.menu_overlay.pos, size=self.menu_overlay.size)
        self.menu_overlay.bind(pos=self.update_overlay_rect, size=self.update_overlay_rect)

        self.gps_label = Label(
            text="GPS: SIGNAL SUCHE...",
            font_size='14sp',
            color=(0.2, 0.8, 0.2, 1),
            size_hint=(1, 0.2)
        )
        self.menu_overlay.add_widget(self.gps_label)

        self.traffic_label = Label(
            text="[ STAUWARNER: INAKTIV ]",
            font_size='16sp',
            bold=True,
            color=(0, 0.8, 1, 1),
            size_hint=(1, 0.2)
        )
        self.menu_overlay.add_widget(self.traffic_label)

        self.track_btn = Button(
            text="[ TRACKING STARTEN ]",
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0, 0.4, 0.1, 0.9),
            color=(0, 1, 0, 1),
            size_hint=(1, 0.3)
        )
        self.track_btn.bind(on_press=self.toggle_tracking)
        self.menu_overlay.add_widget(self.track_btn)

        self.root_layout.add_widget(self.menu_overlay)

        Clock.schedule_interval(self.check_traffic, 10)
        return self.root_layout

    def send_telegram_async(self, text):
        """Startet den Telegram-Versand in einem separaten Thread, damit die App nicht blockiert"""
        threading.Thread(target=self._send_telegram, args=(text,), daemon=True).start()

    def _send_telegram(self, text):
        if TELEGRAM_BOT_TOKEN == "DEIN_BOT_TOKEN_HIER":
            return
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text}
        try:
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Telegram Fehler: {e}")

    def update_bar_rect(self, instance, value):
        self.bar_rect.pos = instance.pos
        self.bar_rect.size = instance.size

    def update_overlay_rect(self, instance, value):
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size

    def toggle_menu(self, instance):
        if self.menu_overlay.parent:
            self.root_layout.remove_widget(self.menu_overlay)
            self.menu_btn.text = "⚙️ MENÜ"
        else:
            self.root_layout.add_widget(self.menu_overlay)
            self.menu_btn.text = "✖ SCHLIESSEN"

    def speak(self, text):
        try:
            if tts:
                tts.speak(text)
        except Exception:
            pass

    def toggle_tracking(self, instance):
        self.is_tracking = not self.is_tracking
        if self.is_tracking:
            self.track_btn.text = "[ TRACKING STOPPEN ]"
            self.track_btn.background_color = (0.6, 0, 0, 0.85)
            self.track_btn.color = (1, 0.3, 0.3, 1)
            self.banner_label.text = "[ TRACKING AKTIV ]"
            self.banner_label.color = (0, 1, 0, 1)
            self.traffic_label.text = "[ STAUWARNER: SCANNE... ]"
            self.speak("Tracking gestartet")
            self.send_telegram_async("🚛 Atlas Tracking GESTARTET")
            self.start_gps()
        else:
            self.track_btn.text = "[ TRACKING STARTEN ]"
            self.track_btn.background_color = (0, 0.4, 0.1, 0.85)
            self.track_btn.color = (0, 1, 0, 1)
            self.banner_label.text = "[ ATLAS: ONLINE ]"
            self.banner_label.color = (0, 1, 0, 1)
            self.traffic_label.text = "[ STAUWARNER: INAKTIV ]"
            self.speak("Tracking gestoppt")
            self.send_telegram_async("🛑 Atlas Tracking GESTOPPT")
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
        speed_ms = kwargs.get('speed', 0.0)
        self.current_speed = speed_ms * 3.6
        self.gps_label.text = f"Geschwindigkeit: {self.current_speed:.1f} km/h"

    def check_traffic(self, dt):
        if not self.is_tracking:
            return

        new_status = ""
        if self.current_speed < 15.0 and self.current_speed > 1.0:
            new_status = "slow"
            self.traffic_label.text = "⚠️ ZÄHFLIESSENDER VERKEHR"
            self.banner_label.text = "⚠️ WARNUNG: STAU"
            self.banner_label.color = (1, 0.5, 0, 1)
            if self.last_status != "slow":
                msg = f"⚠️ Atlas Stauwarner:\nZähfließender Verkehr ({self.current_speed:.1f} km/h)"
                self.speak("Achtung, zähfließender Verkehr voraus.")
                self.send_telegram_async(msg)
        elif self.current_speed <= 1.0:
            new_status = "stop"
            self.traffic_label.text = "🛑 STILLSTAND DETEKTIERT"
            self.banner_label.text = "🛑 STILLSTAND"
            self.banner_label.color = (1, 0, 0, 1)
            if self.last_status != "stop":
                msg = f"🛑 Atlas Stauwarner:\nStillstand detektiert! (Pos: {self.lat:.4f}, {self.lon:.4f})"
                self.speak("Achtung, Stillstand detektiert.")
                self.send_telegram_async(msg)
        else:
            new_status = "clear"
            self.traffic_label.text = "🟢 FREIE FAHRT"
            self.banner_label.text = "[ TRACKING AKTIV ]"
            self.banner_label.color = (0, 1, 0, 1)
            if self.last_status in ["slow", "stop"]:
                self.speak("Freie Fahrt.")
                self.send_telegram_async("🟢 Atlas Stauwarner: Freie Fahrt auf der Route")

        self.last_status = new_status

if __name__ == '__main__':
    AtlasApp().run()
