from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput

from widgets_fixes.assistant.messenger import AssistantMessenger, Image
from widgets_fixes.team.messenger import TeamMessenger
import logging

logging.basicConfig(level=logging.DEBUG)

import os

primary_color = get_color_from_hex("#4CAF50")  # Vert vif
secondary_color = get_color_from_hex("#6C9BCF")  # Bleu clair
accent_color = get_color_from_hex("#FFA726")  # Orange énergique
warning_color = get_color_from_hex("#FF6F61")
text_color = get_color_from_hex("#FFFFFF")  # Texte blanc
background_color = get_color_from_hex("#F9F9F9")  # Fond gris très clair
dark_color = get_color_from_hex("#333333")

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 0
        self.spacing = 0

        # Barre de menu officielle en haut
        self.create_menu_bar()

        # Boutons prédéfinis pour les widgets
        self.create_widget_buttons()

        # Onglets
        self.tab_panel = TabbedPanel(
            do_default_tab=False,  # Désactive l'onglet par défaut
            tab_width=dp(120)  # Largeur des onglets
        )
        self.add_widget(self.tab_panel)

        # Onglet "Welcome" par défaut
        self.create_welcome_tab()

        # Bouton "+" pour ajouter des onglets
        self.add_button = Button(
            text="+",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            background_color=accent_color,  # Orange énergique
            color=text_color,  # Texte blanc
            font_size=dp(20)
        )
        self.add_button.bind(on_release=self.add_new_tab)
        self.tab_panel.add_widget(self.add_button)

        # Pied de page fixe pour les widgets
        self.footer = BoxLayout(
            orientation="horizontal",  # Changé à horizontal pour afficher côte à côte
            size_hint=(1, None),
            height=dp(50),  # Hauteur réduite par défaut
            spacing=dp(5),
            padding=dp(5)
        )
        self.add_widget(self.footer)

        # Ajouter les widgets AssistantMessenger et TeamMessenger
        self.add_widgets_to_footer()

    def add_widgets_to_footer(self):
        """Ajoute les widgets AssistantMessenger et TeamMessenger au pied de page avec un style amélioré."""
        self.footer.clear_widgets()  # Nettoyer le footer avant d'ajouter de nouveaux widgets

        # Bouton pour ouvrir le Widget AssistantMessenger
        self.assistant_button = Button(
            text="[size=20]🤖[/size]",  # Utilisation d'une icône
            markup=True,
            size_hint_y=None,
            height=dp(50),
            background_color=primary_color,  # Vert vif
            color=text_color,  # Texte blanc
            background_normal='',  # Supprime l'image de fond par défaut
            border=(0, 0, 0, 0)  # Supprime la bordure
        )
        self.assistant_button.bind(on_release=lambda btn: self.toggle_widget(self.assistant_messenger))
        self.footer.add_widget(self.assistant_button)

        # Bouton pour ouvrir le Widget TeamMessenger
        self.team_button = Button(
            text="[size=20]👥[/size]",  # Utilisation d'une icône
            markup=True,
            size_hint_y=None,
            height=dp(50),
            background_color=secondary_color,  # Bleu clair
            color=text_color,  # Texte blanc
            background_normal='',  # Supprime l'image de fond par défaut
            border=(0, 0, 0, 0)  # Supprime la bordure
        )
        self.team_button.bind(on_release=lambda btn: self.toggle_widget(self.team_messenger))
        self.footer.add_widget(self.team_button)

        # Ajouter les widgets AssistantMessenger et TeamMessenger
        self.assistant_messenger = AssistantMessenger(size_hint_y=dp(5), height=dp(5))
        self.assistant_messenger.height = 0  # Réduit par défaut
        self.footer.add_widget(self.assistant_messenger)

        self.team_messenger = TeamMessenger(size_hint_y=dp(5), height=dp(5))
        self.team_messenger.height = 0  # Réduit par défaut
        self.footer.add_widget(self.team_messenger)

    def close_app(self, instance):
        """Ferme l'application."""
        App.get_running_app().stop()

    def toggle_widget(self, widget):
        """Réduit ou affiche le widget spécifié."""
        logging.debug(f"Toggling widget: {widget}")
        if widget.size_hint_y is None:
            widget.size_hint_y = 1  # Affiche le widget
            widget.height = dp(200)  # Définit une hauteur fixe
            logging.debug(f"Widget {widget} is now visible")
        else:
            widget.size_hint_y = None  # Cache le widget
            widget.height = 0  # Réduit la hauteur à 0
            logging.debug(f"Widget {widget} is now hidden")
        self.footer.do_layout()  # Force la mise à jour de la mise en page
    def create_menu_bar(self):
        """Crée une barre de menu officielle en haut."""
        menu_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(1, None),
            height=dp(50),
            padding=0,
            spacing=0
        )

        # Ajouter un fond coloré avec un Canvas
        with menu_bar.canvas.before:
            Color(*secondary_color)  # Bleu clair
            menu_bar.rect = Rectangle(size=menu_bar.size, pos=menu_bar.pos)
        menu_bar.bind(size=self._update_rect, pos=self._update_rect)

        # Bouton "Fichier"
        file_button = Button(
            text="Fichier",
            size_hint=(None, 1),
            width=dp(100),
            background_color=secondary_color,  # Bleu clair
            color=text_color,  # Texte blanc
            bold=True
        )
        file_button.bind(on_release=self.show_file_menu)
        menu_bar.add_widget(file_button)

        # Bouton "Aide"
        help_button = Button(
            text="Aide",
            size_hint=(None, 1),
            width=dp(100),
            background_color=secondary_color,  # Bleu clair
            color=text_color,  # Texte blanc
            bold=True
        )
        help_button.bind(on_release=self.show_help_menu)
        menu_bar.add_widget(help_button)

        self.add_widget(menu_bar)

    def _update_rect(self, instance, value):
        """Met à jour la taille et la position du rectangle de fond."""
        instance.rect.size = instance.size
        instance.rect.pos = instance.pos

    def show_file_menu(self, instance):
        """Affiche un menu déroulant pour 'Fichier'."""
        file_dropdown = BoxLayout(orientation="vertical", size_hint=(None, None), size=(dp(150), dp(80)))

        # Option "Quitter"
        quit_button = Button(
            text="Quitter",
            size_hint_y=None,
            height=dp(40),
            background_color=get_color_from_hex(warning_color),  # Rouge vif
            color=text_color  # Texte blanc
        )
        quit_button.bind(on_release=self.quit_app)
        file_dropdown.add_widget(quit_button)

        # Popup pour simuler un menu déroulant
        popup = Popup(title="Fichier", content=file_dropdown, size_hint=(None, None), size=(dp(200), dp(100)))
        popup.open()

    def show_help_menu(self, instance):
        """Affiche un menu déroulant pour 'Aide'."""
        help_dropdown = BoxLayout(orientation="vertical", size_hint=(None, None), size=(dp(150), dp(80)))

        # Option "À propos"
        about_button = Button(
            text="À propos",
            size_hint_y=None,
            height=dp(40),
            background_color=primary_color,  # Vert vif
            color=text_color  # Texte blanc
        )
        about_button.bind(on_release=self.show_about_popup)
        help_dropdown.add_widget(about_button)

        # Popup pour simuler un menu déroulant
        popup = Popup(title="Aide", content=help_dropdown, size_hint=(None, None), size=(dp(200), dp(100)))
        popup.open()

    def quit_app(self, instance):
        """Ferme l'application."""
        App.get_running_app().stop()

    def show_about_popup(self, instance):
        """Affiche une popup 'À propos'."""
        popup_content = Label(text="Team-Task-Sync\nVersion 1.0\n© 2023")
        popup = Popup(title="À propos", content=popup_content, size_hint=(0.8, 0.4))
        popup.open()

    def create_widget_buttons(self):
        """Crée des boutons prédéfinis pour les widgets."""
        widget_layout = GridLayout(
            cols=5,
            size_hint=(1, None),
            height=dp(60),
            spacing=dp(5),
            padding=dp(10)
        )

        # Ajouter un fond coloré avec un Canvas
        with widget_layout.canvas.before:
            Color(*background_color)  # Fond gris très clair
            widget_layout.rect = Rectangle(size=widget_layout.size, pos=widget_layout.pos)
        widget_layout.bind(size=self._update_rect, pos=self._update_rect)

        # Boutons prédéfinis
        widgets = ["Assistants", "Team Chat", "Projet", "Calendrier", "Statistiques"]
        for widget in widgets:
            button = Button(
                text=widget,
                size_hint=(None, None),
                size=(dp(120), dp(50)),
                background_color=primary_color,  # Vert vif
                color=text_color,  # Texte blanc
                bold=True
            )
            button.bind(on_release=lambda btn, w=widget: self.open_widget_tab(w))
            widget_layout.add_widget(button)

        self.add_widget(widget_layout)

    def open_widget_tab(self, widget_name):
        """Ouvre un onglet pour le widget sélectionné."""
        # Vérifie si l'onglet existe déjà
        for tab in self.tab_panel.tabs:
            if tab.text == widget_name:
                self.tab_panel.switch_to(tab)
                return

        # Crée un nouvel onglet
        new_tab = TabbedPanelItem(text=widget_name)
        new_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        # Exemple de contenu pour le nouvel onglet
        new_layout.add_widget(Label(text=f"Contenu de {widget_name}"))
        new_layout.add_widget(Button(
            text=f"Fonctionnalité 1 de {widget_name}",
            background_color=secondary_color,  # Bleu clair
            color=text_color  # Texte blanc
        ))
        new_layout.add_widget(Button(
            text=f"Fonctionnalité 2 de {widget_name}",
            background_color=accent_color,  # Orange énergique
            color=text_color  # Texte blanc
        ))

        new_tab.add_widget(new_layout)
        self.tab_panel.add_widget(new_tab)
        self.tab_panel.switch_to(new_tab)

    def create_welcome_tab(self):
        """Crée l'onglet 'Welcome' avec une description améliorée."""
        welcome_tab = TabbedPanelItem(text="Welcome")
        welcome_layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))

        # Ajouter un logo ou une image
        # logo = Image(source='logo.png', size_hint=(1, None), height=dp(100))
        # welcome_layout.add_widget(logo)

        # Description de l'application
        description = (
            "[b]Team-Task-Sync[/b] est une application de gestion de tâches en équipe.\n\n"
            "Elle permet de synchroniser les tâches entre les membres de l'équipe, "
            "de suivre les progrès et de gérer les ressources partagées.\n\n"
            "Pour commencer, utilisez les boutons ci-dessus pour ouvrir les widgets."
        )
        welcome_label = Label(
            text=description,
            size_hint=(1, None),
            height=dp(200),
            markup=True,
            font_size=dp(16),
            color=get_color_from_hex(dark_color)  # Couleur de texte plus foncée
        )
        welcome_layout.add_widget(welcome_label)

        welcome_tab.add_widget(welcome_layout)
        self.tab_panel.add_widget(welcome_tab)

    def add_new_tab(self, instance):
        """Ajoute un nouvel onglet entre 'Welcome' et le bouton '+'."""
        new_tab = TabbedPanelItem(text=f"Onglet {len(self.tab_panel.tabs) - 1}")  # -1 pour ignorer le bouton '+'
        new_layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))

        # Exemple de contenu pour le nouvel onglet
        new_layout.add_widget(Label(text=f"Contenu de l'onglet {len(self.tab_panel.tabs) - 1}"))
        new_layout.add_widget(Button(
            text=f"Fonctionnalité 1",
            background_color=secondary_color,  # Bleu clair
            color=text_color  # Texte blanc
        ))
        new_layout.add_widget(Button(
            text=f"Fonctionnalité 2",
            background_color=accent_color,  # Orange énergique
            color=text_color  # Texte blanc
        ))

        new_tab.add_widget(new_layout)
        self.tab_panel.add_widget(new_tab)
        self.tab_panel.switch_to(new_tab)

class TeamTaskSyncApp(App):
    def build(self):
        Window.clearcolor = background_color  # Fond gris très clair
        return MainLayout()

if __name__ == "__main__":
    TeamTaskSyncApp().run()
