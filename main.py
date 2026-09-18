from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window

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
            color=(0, 1, 0.4, 1),  # Neon-Grün
            size_hint_y=0.15
        )
        
        # Matrix-Konsolenfenster für Standort- & Telemetriedaten
        self.console = Label(
            text="> System initialisiert...\n> Warte auf GPS-Signal...\n> Telemetrie: Standby\n> Server-Verbindung: Bereit",
            font_size='15sp',
            color=(0, 0.8, 0.3, 1),
            halign='left',
            valign='top',
            size_hint_y=0.65
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
        return root

    def toggle_tracking(self, instance):
        if not self.tracking_active:
            self.tracking_active = True
            self.btn.text = "[ TRACKING STOPPEN ]"
            self.btn.background_color = (0.5, 0.1, 0.1, 1)  # Dunkelrot bei Aktivität
            self.btn.color = (1, 0.3, 0.3, 1)
            self.console.text = "> TRACKING AKTIV\n> GPS-Daten werden gesendet...\n> Route: Live\n> Modus: E-LKW Telemetrie"
        else:
            self.tracking_active = False
            self.btn.text = "[ TRACKING STARTEN ]"
            self.btn.background_color = (0, 0.3, 0.1, 1)
            self.btn.color = (0, 1, 0.5, 1)
            self.console.text = "> Tracking gestoppt.\n> System im Standby."

if __name__ == '__main__':
    AtlasMatrixApp().run()
