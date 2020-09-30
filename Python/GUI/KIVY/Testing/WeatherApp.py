from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.network.urlrequest import UrlRequest
import json

class AddLocationForm(BoxLayout):
    search_input = ObjectProperty()
        
    def search_location(self):
        search_template = "http://api.openweathermap.ord/data/2.5/" + "find?q={}&type=like"
        search_url      = search_template.format(self.search_input.text)
        request         = UrlRequest(search_url, self.found_location)
        
        print("The user searched for {}".format(self.search_input.text))

    def found_location(self, request, data):
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("\n".join(cities))
        self.search_results.items_strings = cities
        
class WeatherApp(App):
    title = "WeatherApp"
    pass

if __name__ == '__main__':
    WeatherApp().run()