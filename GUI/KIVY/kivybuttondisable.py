from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial

class kivy_test_app(App):
    def disable(self,instance, *args):
        instance.disable = True
    
    def update(self,instance, *args):
        instance.text = "I am disabled!"
        
    def build(self):
            mybtn = Button(text="Click me to disable")
            
            mybtn.bind(on_press=partial(self.disable, mybtn))
            
            mybtn.bind(on_press=partial(self.update, mybtn))

            return mybtn
    
kivy_test_app().run()