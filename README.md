
# Application Get'zere

### Installation

##### Etapes :
1. Vous pouvez installer les fichier _requirements.txt_ en lançant la commande `pip install -r requirements.txt`
2. Vérifier que le fichier _user_api.py_ est bien installé à la racine du projet.

Le projet doit se décomposer de la manière suivante :
``` text
> CommentYAller
    > APIs
    > Flask
    > Trip
    README.md
    requirements.txt
    user_api.py
```

### Lancement du projet

_Vous devez posséder python3 pour lancer le projet._

##### Etapes :
1. Lancer le script _run.py_ dans le dossier _Flask_.
2. Dans votre navigateur tapez _http://localhost:5000/_ ou _http://127.0.0.1:5000/_

##### Fonctionnement :
Le cadre du projet se limite à la ville de Paris : si vous tapez une adresse n'étant pas dans Paris, l'application peut renvoyer un résultat mais celui-ci sera sans doute biaisé.
Vous pouvez sélectionner 'Ma position' ou tout autre adresse. 'Ma position' va cherche l'adresse IP de l'utilisateur et essayer de s'y connecter.
Si l'application n'arrive pas à localiser l'adresse IP ou que celle-ci ne se trouve pas à Paris, l'application ne voudra pas charger la page de résultat.

Vous pouvez renseigner diverses informations à votre sujet et concernant vos préférences de trajets, celles-ci seront prises en compte dans la recommandation que nous vous fournirons.


