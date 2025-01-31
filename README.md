# Team-Task-Sync

## Description

Ce projet est une application de synchronisation des tâches d'équipe. Il permet aux membres de l'équipe de créer, assigner et suivre les tâches de manière collaborative.

## Structure du Projet

Le projet est organisé en plusieurs modules pour une meilleure gestion et maintenance.

### Dossiers Principaux

- **widgets_fixes** : Contient les widgets fixes de l'application.
- **widgets_personnalises** : Contient les widgets personnalisés de l'application.
- **data_tmp** : Contient les données temporaires.
- **data** : Contient les données permanentes.

## Comment Démarrer

1. Clonez ce dépôt sur votre machine locale.
2. Installez les dépendances nécessaires.
3. Configurez les variables d'environnement.
4. Lancez l'application.

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les [directives de contribution](lien_vers_les_directives) pour plus d'informations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Analyse des Fichiers

### `main.py`

Le fichier `main.py` est le point d'entrée de l'application. Il configure l'interface utilisateur principale et initialise les différents widgets et onglets de l'application.

### `widgets_fixes/assistant/messenger.py`

Le fichier `widgets_fixes/assistant/messenger.py` définit le widget `AssistantMessenger`, qui permet aux utilisateurs d'interagir avec un assistant IA. Ce widget inclut des fonctionnalités pour :

- Envoyer des messages à l'assistant.
- Afficher les réponses de l'assistant.

### `widgets_fixes/team/messenger.py`

Le fichier `widgets_fixes/team/messenger.py` définit le widget `TeamMessenger`, qui permet aux membres de l'équipe de communiquer entre eux via un chat intégré. Ce widget permet :

- L'envoi de messages au sein de l'équipe.
- La réception de messages des autres membres de l'équipe.
