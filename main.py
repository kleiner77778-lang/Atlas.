from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class AtlasApp(App):

  def build(self):
    # Layout erstellen
    layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

    # Text-Anzeige
    self.label = Label(
        text='Atlas EV Navi\nBereit für Android!',
        font_size=24,
        halign='center',
    )

    # Ein interaktiver Button
    btn = Button(
        text='Klick mich',
        size_hint=(1, 0.3),
        background_color=(0.1, 0.6, 0.8, 1),
    )
    btn.bind(on_press=self.on_button_click)

    layout.add_widget(self.label)
    layout.add_widget(btn)

    return layout

  def on_button_click(self, instance):
    self.label.text = 'Button gedrückt!\nAtlas funktioniert.'


if __name__ == '__main__':
  AtlasApp().run()
