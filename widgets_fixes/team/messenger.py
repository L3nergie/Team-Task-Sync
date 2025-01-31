from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.metrics import dp

import logging

logging.basicConfig(level=logging.DEBUG)

class TeamMessenger(BoxLayout):
    def __init__(self, **kwargs):
        super(TeamMessenger, self).__init__(**kwargs)
        self.messages = []
        self.orientation = 'vertical'
        self.first_message_sent = False  # Pour vérifier si le premier message a été envoyé

        # Couleur de fond
        with self.canvas.before:
            Color(*get_color_from_hex("#E0F7FA"))  # Fond clair
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Barre de titre personnalisée
        self.title_bar = BoxLayout(size_hint_y=0.1, orientation='horizontal', padding=[10, 5], spacing=10)

        # Titre du chat
        self.title_label = Label(
            text="Team Chat",
            color=get_color_from_hex("#00796B"),  # Texte vert foncé

            font_size='20sp',
            size_hint_x=0.8,
            bold=True
        )

        # Bouton de fermeture
        self.close_button = Button(
            text="X",
            size_hint_x=0.2,
            background_color=get_color_from_hex("#D32F2F"),  # Rouge foncé
            color=get_color_from_hex("#FFFFFF"),  # Texte blanc
            font_size='18sp',
            bold=True
        )
        self.close_button.bind(on_press=self.close_widget)

        # Ajout des éléments à la barre de titre
        self.title_bar.add_widget(self.title_label)
        self.title_bar.add_widget(self.close_button)

        # Zone d'affichage des messages
        self.chat_display = Label(
            size_hint_y=0.7,
            text="Bienvenue dans le chat d'équipe!\n",
            color=get_color_from_hex("#000000"),  # Texte en noir
            font_size='16sp',  # Taille de la police
            padding=[10, 10],
            markup=True
        )

        # Champ de saisie
        self.user_input = TextInput(
            size_hint_y=0.1,
            multiline=False,
            background_color=get_color_from_hex("#FFFFFF"),  # Fond blanc
            foreground_color=get_color_from_hex("#000000"),  # Texte noir
            font_size='16sp',
            padding=[10, 10]
        )

        # Bouton d'envoi
        self.send_button = Button(
            size_hint_y=0.1,
            text="Envoyer",
            background_color=get_color_from_hex("#00796B"),  # Vert foncé
            color=get_color_from_hex("#FFFFFF"),  # Texte blanc
            font_size='18sp',
            bold=True
        )

        # Ajout des widgets à la mise en page
        self.add_widget(self.title_bar)
        self.add_widget(self.chat_display)
        self.add_widget(self.user_input)
        self.add_widget(self.send_button)

        # Liaison des événements
        self.send_button.bind(on_press=self.send_message)
        self.bind(pos=self.update_rect, size=self.update_rect)
        logging.info("TeamMessenger initialisé {self.send_message}")

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def send_message(self, instance):
        user_message = self.user_input.text
        if not self.first_message_sent:
            # Supprimer le message de bienvenue après le premier message
            self.chat_display.text = ""
            self.first_message_sent = True

        self.add_message(f"[b]Vous:[/b] {user_message}")
        self.user_input.text = ''  # Effacer le champ de saisie

        # Simuler une réponse de l'équipe
        self.add_message(f"[b]Équipe:[/b] Message reçu: '{user_message}'")
        logging.info(f"Message envoyé à l'équipe: {user_message}")

    def add_message(self, message):
        self.messages.append(message)
        self.chat_display.text += f"{message}\n"

    def close_widget(self, instance):
        """Masque ou supprime le widget au lieu de fermer l'application."""
        self.parent.remove_widget(self)  # Supprime le widget de son parent

class TeamMessengerApp(App):
    def build(self):
        Window.clearcolor = get_color_from_hex("#E0F7FA")  # Couleur de fond de la fenêtre
        return TeamMessenger()

if __name__ == "__main__":
    TeamMessengerApp().run()
