import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage, Image
from kivy.clock import Clock
from kivy.uix.button import Button

class LoadingScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoadingScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 50
        self.spacing = 20

        # Add the app logo
        self.app_logo = Image(
            source='assets/images/logo.png', 
            size_hint=(1, 0.5)
        )
        self.add_widget(self.app_logo)

        # Add the loading GIF (spinner)
        self.loading_gif = AsyncImage(
            source='assets/images/loading.gif',
            anim_delay=0.1,       
            size_hint=(1, 0.3)    
        )
        self.add_widget(self.loading_gif)

        # Add a label for status
        self.status_label = Label(text="Checking internet connection...", size_hint=(1, 0.2))
        self.add_widget(self.status_label)

        # Start the spinner and check internet after 3.6 seconds
        Clock.schedule_once(self.check_internet, 3.6)

    def check_internet(self, dt):
        # Check internet connectivity
        try:
            response = requests.get("https://www.google.com", timeout=5)
            if response.status_code == 200:
                self.status_label.text = "Internet connected!"
                Clock.schedule_once(self.go_to_main_screen, 2)  
            else:
                self.show_no_internet()
        except requests.ConnectionError:
            self.show_no_internet()

    def show_no_internet(self):
        # Remove the spinner and status label
        self.remove_widget(self.loading_gif)
        self.remove_widget(self.status_label)

        # Add a "No internet" icon
        self.no_internet_icon = Image(
            source='assets/no_internet.png', 
            size_hint=(1, 0.3))
        self.add_widget(self.no_internet_icon)

        # Add "No internet" text
        self.no_internet_text = Label(text="No internet connection", size_hint=(1, 0.2))
        self.add_widget(self.no_internet_text)

        # Add a retry button
        self.retry_button = Button(text="Retry", size_hint=(1, 0.2))
        self.retry_button.bind(on_press=self.retry_check)
        self.add_widget(self.retry_button)

    def retry_check(self, instance):
        # Remove the "No internet" widgets
        self.remove_widget(self.no_internet_icon)
        self.remove_widget(self.no_internet_text)
        self.remove_widget(self.retry_button)

        # Re-add the spinner and status label
        self.add_widget(self.loading_gif)
        self.add_widget(self.status_label)
        self.status_label.text = "Checking internet connection..."

        # Re-trigger the spinner and internet check after 3.6 seconds
        Clock.schedule_once(self.check_internet, 3.6)

    def go_to_main_screen(self, dt):
        # Replace this with your main screen logic
        self.clear_widgets() 
        self.add_widget(Label(text="Unleashing the magic ... just a moment!", font_size=30))  # Transition to the main screen


class MyApp(App):
    def build(self):
        return LoadingScreen()


if __name__ == '__main__':
    MyApp().run()