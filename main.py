import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.text import Label as CoreLabel

# Original Katakana, Zahlen & Matrix-Spezialzeichen
MATRIX_CHARS = "ｦｱｳｴｵｶｷｹｺｻｼｽｾｿﾀﾂﾃﾅﾆﾇﾈﾊﾋﾎﾏﾐﾑﾒﾓﾔﾕﾗﾘﾜ0123456789ABCDEF$#@%&*"

class MatrixRainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = []
        self.font_size = 18
        self.is_tracking = False
        # Reagiert dynamisch auf Bildschirmskalierung und -drehung
        self.bind(size=self.reinit_rain)
        Clock.schedule_once(self.init_rain, 0.1)
        
    def init_rain(self, dt):
        self.rebuild_columns()
        Clock.schedule_interval(self.update_rain, 0.04)

    def reinit_rain(self, instance, value):
        # Berechnet die Regenspalten neu, wenn das Gerät gedreht wird
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
                'length': random.randint(10, 22),
                'chars': [random.choice(MATRIX_CHARS) for _ in range(30)]
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
                            # Der Tropfenkopf leuchtet hellgrün/weiß
                            Color(0.85, 1.0, 0.85, 1)
                        else:
                            # Verblassen nach oben
                            alpha = max(0.08, 1.0 - (j / col['length']))
                            Color(0.0, 1.0, 0.25, alpha)

                        # Zufälliger Zeichenwechsel (Matrix Glitch Effect)
                        if random.random() < 0.05:
                            col['chars'][j] = random.choice(MATRIX_CHARS)

                        char = col['chars'][j]
                        core_label = CoreLabel(text=char, font_size=self.font_size)
                        core_label.refresh()
                        texture = core_label.texture
                        Rectangle(texture=texture, pos=(col['x'], char_y), size=texture.size)

class AtlasApp(App):
    def build(self):
        root = FloatLayout()

        # Matrix Regeneffekt als Vollbild-Hintergrund
        self.rain = MatrixRainWidget(size_hint=(1, 1))
        root.add_widget(self.rain)

        # Overlay Benutzeroberfläche
        ui_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        self.header = Label(
            text="[ SYSTEM: ATLAS ONLINE ]",
            font_size='22sp',
            bold=True,
            color=(0, 1, 0, 1),
            size_hint=(1, 0.15)
        )
        ui_layout.add_widget(self.header)

        # Transparenter Zwischenraum für den freien Blick auf den Regen
        ui_layout.add_widget(BoxLayout(size_hint=(1, 0.65)))

        # Tracking Start/Stop Button
        self.btn = Button(
            text="[ TRACKING STARTEN ]",
            font_size='20sp',
            bold=True,
            background_normal='',
            background_color=(0, 0.4, 0.1, 0.85),
            color=(0, 1, 0, 1),
            size_hint=(1, 0.2)
        )
        self.btn.bind(on_press=self.toggle_tracking)
        ui_layout.add_widget(self.btn)

        root.add_widget(ui_layout)
        return root

    def toggle_tracking(self, instance):
        self.rain.is_tracking = not self.rain.is_tracking
        if self.rain.is_tracking:
            self.btn.text = "[ TRACKING STOPPEN ]"
            self.btn.background_color = (0.6, 0, 0, 0.85)
            self.btn.color = (1, 0.3, 0.3, 1)
            self.header.text = "[ SYSTEM: TRACKING ACTIVE ]"
        else:
            self.btn.text = "[ TRACKING STARTEN ]"
            self.btn.background_color = (0, 0.4, 0.1, 0.85)
            self.btn.color = (0, 1, 0, 1)
            self.header.text = "[ SYSTEM: ATLAS ONLINE ]"

if __name__ == '__main__':
    AtlasApp().run()
