from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class SimpleApp(App):
    def build(self):
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Add a title label
        title = Label(
            text='My Simple Kivy App',
            size_hint=(1, 0.2),
            font_size='24sp'
        )
        
        # Add a text input
        self.text_input = TextInput(
            hint_text='Enter something here...',
            size_hint=(1, 0.2),
            multiline=False
        )
        
        # Add a button
        button = Button(
            text='Click Me!',
            size_hint=(1, 0.2),
            background_color=(0.2, 0.7, 0.3, 1)
        )
        button.bind(on_press=self.on_button_click)
        
        # Add a label to show output
        self.output_label = Label(
            text='Output will appear here',
            size_hint=(1, 0.4),
            text_size=(None, None),
            halign='center'
        )
        
        # Add all widgets to layout
        main_layout.add_widget(title)
        main_layout.add_widget(self.text_input)
        main_layout.add_widget(button)
        main_layout.add_widget(self.output_label)
        
        return main_layout
    
    def on_button_click(self, instance):
        # Update output label with input text
        user_input = self.text_input.text
        if user_input:
            self.output_label.text = f'You entered: {user_input}'
        else:
            self.output_label.text = 'Please enter some text!'

# Run the app
if __name__ == '__main__':
    SimpleApp().run()