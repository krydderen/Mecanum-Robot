from kivy.app import App
from kivy.uix.button import Button

class MainWindow(App):
    
    def build(self):
        return Button(text="hei hååkon", pos=(300,350),size_hint=(0.25,0.18))
MainWindow().run()   