from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

import logging
import requests
import os
from dotenv import load_dotenv
from threading import Thread

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class IconButton(ButtonBehavior, Image):
    """Bouton avec une icône."""
    pass

class AssistantMessenger(BoxLayout):
    def __init__(self, **kwargs):
        super(AssistantMessenger, self).__init__(**kwargs)
        self.messages = []
        self.orientation = 'vertical'
        self.first_message_sent = False

        # Load API key
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            logger.error("La clé API Mistral n'a pas été trouvée dans les variables d'environnement.")
            return

        # Set up UI
        with self.canvas.before:
            Color(*get_color_from_hex("#4CAF50"))
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[(dp(15), dp(15)), (dp(15), dp(15)), (0, 0), (0, 0)])

        # Title bar
        self.title_bar = BoxLayout(size_hint_y=0.1, orientation='horizontal', padding=[10, 5], spacing=10)
        self.title_label = Label(
            text="Assistant IA",
            color=get_color_from_hex("#FFFFFF"),
            font_size='20sp',
            size_hint_x=0.8,
            bold=True
        )
        self.close_button = IconButton(
            source="close_icon.png",  # Remplacez par le chemin de votre icône
            size_hint_x=0.2,
        )
        self.close_button.bind(on_press=self.close_widget)
        self.title_bar.add_widget(self.title_label)
        self.title_bar.add_widget(self.close_button)

        # Chat display
        self.scroll_view = ScrollView(size_hint_y=0.7, do_scroll_x=False)
        self.chat_display = BoxLayout(
            size_hint_y=None,
            orientation='vertical',
            padding=[10, 10],
            spacing=10
        )
        self.chat_display.bind(minimum_height=self.chat_display.setter('height'))
        self.scroll_view.add_widget(self.chat_display)

        # Input area
        self.input_area = BoxLayout(size_hint_y=0.15, orientation='horizontal', padding=[10, 5], spacing=10)

        # User input
        self.user_input = TextInput(
            size_hint_x=0.8,
            multiline=True,
            background_color=get_color_from_hex("#FFFFFF"),
            foreground_color=get_color_from_hex("#000000"),
            font_size='16sp',
            padding=[10, 10],
            hint_text="Tapez votre message ici...",
        )
        self.user_input.bind(on_text_validate=self.send_message)  # Enter pour envoyer
        self.user_input.bind(on_key_down=self.handle_key_down)  # Gestion de Shift + Enter

        # Send button
        self.send_button = Button(
            size_hint_x=0.2,
            text="Envoyer",
            background_color=get_color_from_hex("#00796B"),
            color=get_color_from_hex("#FFFFFF"),
            font_size='18sp',
            bold=True
        )
        self.send_button.bind(on_press=self.send_message)

        # Add widgets to input area
        self.input_area.add_widget(self.user_input)
        self.input_area.add_widget(self.send_button)

        # Add widgets to layout
        self.add_widget(self.title_bar)
        self.add_widget(self.scroll_view)
        self.add_widget(self.input_area)

        # Bind events
        self.bind(pos=self.update_rect, size=self.update_rect)
        logger.info("AssistantMessenger initialisé")

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def handle_key_down(self, instance, keyboard, keycode, text, modifiers):
        """Gère les touches du clavier."""
        if keycode == 40 and "shift" in modifiers:  # Shift + Enter
            instance.insert_text("\n")  # Saut de ligne
            return True
        elif keycode == 40:  # Enter seul
            self.send_message()
            return True
        return False

    def send_message(self, *args):
        user_message = self.user_input.text.strip()
        if not user_message:
            return  # Ne rien faire si le champ est vide

        if not self.first_message_sent:
            self.chat_display.clear_widgets()
            self.first_message_sent = True

        self.add_message(f"Vous: {user_message}", "user")
        self.user_input.text = ''

        # Start a thread to handle the API call
        Thread(target=self.get_ai_response, args=(user_message,)).start()

    def add_message(self, message, role):
        """Ajoute un message à l'affichage."""
        message_label = Label(
            text=message,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex("#FFFFFF") if role == "assistant" else get_color_from_hex("#000000"),
            font_size='16sp',
            halign="left" if role == "user" else "right",
            padding=[10, 10],
            markup=True
        )
        with message_label.canvas.before:
            Color(*get_color_from_hex("#00796B" if role == "assistant" else "#E0E0E0"))
            RoundedRectangle(pos=message_label.pos, size=message_label.size, radius=[(dp(10), dp(10))])
        self.chat_display.add_widget(message_label)
        self.scroll_view.scroll_to(message_label)

    def get_ai_response(self, message):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistral-large-latest",
            "messages": [
                {"role": "system", "content": "Vous êtes un assistant utile. Répondez toujours dans la langue de l'utilisateur. Soyez concis et poli."},
                {"role": "user", "content": message}
            ],
            "max_tokens": 150
        }
        try:
            response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)
            logger.info(f"Response from Mistral API: {response.json()}")
            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content'].strip()
                Clock.schedule_once(lambda dt: self.add_message(f"Assistant: {ai_response}", "assistant"))
            else:
                Clock.schedule_once(lambda dt: self.add_message(f"Assistant: Désolé, je n'ai pas pu traiter votre demande. (Code: {response.status_code})", "assistant"))
        except Exception as e:
            logger.error(f"Erreur lors de l'appel à l'API Mistral : {e}")
            Clock.schedule_once(lambda dt: self.add_message(f"Assistant: Erreur de connexion à l'API.", "assistant"))

    def close_widget(self, instance):
        self.parent.remove_widget(self)

class AssistantApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#E0F7FA")
        return AssistantMessenger()

if __name__ == "__main__":
    AssistantApp().run()
