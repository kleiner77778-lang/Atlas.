import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

# Matrix-Look: Schwarzer Hintergrund
Window.clearcolor = (0, 0, 0, 1)

class AtlasMatrixApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Header / Status-Titel
        header = Label(
            text="[ SYSTEM: ATLAS ONLINE ]",
            font_size='22sp',
            bold=True,
            color=(0, 1, 0.4, 1),
            size_hint_y=0.12
        )
        
        # Fließendes Matrix-Konsolenfenster
        self.console_lines = [
            "> SYSTEM INITIALISIERT...",
            "> BEREIT FUER TELEMETRIE-STREAM..."
        ]
        
        self.console = Label(
            text="\n".join(self.console_lines),
            font_size='13sp',
            color=(0, 0.9, 0.3, 1),
            halign='left',
            valign='bottom',
            size_hint_y=0.68
        )
        self.console.bind(size=self.console.setter('text_size'))

        # Start / Stop Button
        self.btn = Button(
            text="[ TRACKING STARTEN ]",
            font_size='18sp',
            bold=True,
            background_normal='',
            background_color=(0, 0.3, 0.1, 1),
            color=(0, 1, 0.5, 1),
            size_hint_y=0.2
        )
        self.btn.bind(on_press=self.toggle_tracking)

        root.add_widget(header)
        root.add_widget(self.console)
        root.add_widget(self.btn)

        self.tracking_active = False
        
        # Starte den regelmäßigen Matrix-Stream (alle 0.4 Sekunden)
        Clock.schedule_interval(self.update_matrix_stream, 0.4)
        
        return root

    def update_matrix_stream(self, dt):
        if self.tracking_active:
            # Generiere zufällige Matrix- / GPS-Hex-Strings
            hex_data = ''.join(random.choices('0123456789ABCDEF', k=12))
            lat = round(47.75 + random.uniform(-0.01, 0.01), 6)
            lon = round(8.83 + random.uniform(-0.01, 0.01), 6)
            
            new_line = f"> [LIVE GPS] LAT: {lat} | LON: {lon} | HEX: {hex_data}"
        else:
            # Passiver Standby Matrix Stream
            passive_code = ''.join(random.choices('01', k=32))
            new_line = f"> IDLE STREAM: {passive_code}"

        self.console_lines.append(new_line)
        
        # Behalte nur die letzten 14 Zeilen im Bild
        if len(self.console_lines) > 14:
            self.console_lines.pop(0)

        self.console.text = "\n".join(self.console_lines)

    def toggle_tracking(self, instance):
        if not self.tracking_active:
            self.tracking_active = True
            self.btn.text = "[ TRACKING STOPPEN ]"
            self.btn.background_color = (0.5, 0.1, 0.1, 1)
            self.btn.color = (1, 0.3, 0.3, 1)
            self.console_lines.append("> --- LIVE-TRACKING AKTIVIERT ---")
        else:
            self.tracking_active = False
            self.btn.text = "[ TRACKING STARTEN ]"
            self.btn.background_color = (0, 0.3, 0.1, 1)
            self.btn.color = (0, 1, 0.5, 1)
            self.console_lines.append("> --- TRACKING PAUSIERT ---")

if __name__ == '__main__':
    AtlasMatrixApp().run()
