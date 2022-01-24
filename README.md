# OCR_P10 - Projet P10 - créez une API sécurisée RESTful en utilisant Django REST

### créer un back-end performant et sécurisé via des points de terminaison d'API pour la conception d'une application de suivi de problèmes

---

## Présentation

[![Generic badge](https://img.shields.io/badge/Statut-Stable-<COLOR>.svg)](https://shields.io/)

Le but de l'excercice est de concevoir une API en utilisant les outils Django-server et Django-Rest-FrameWork pour la conception de points de terminaison d'API via une connexion sécurisée.<br/>
Seuls les utilisations connectées et contribuant aux différents projects peuvent avoir accès aux informations demandées. Chaque projet peut se voir associer des problèmes qui lui sont liés ; l'utilisateur ne doit pouvoir appliquer le processus CRUD aux problèmes du projet que si il ou elle figure sur la liste des contributeurs.
Ceci pour le respect des conditions dictées par le RGPD pour la confidentialités des données présentes dans la base de données.
Une connexion des utilisateurs se fera par la mise en place de Token via une authentification JWT

---

## Prérequis :

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Python badge](https://img.shields.io/badge/Python->=3.7-blue.svg)](https://www.python.org/)

---

## Clonage du Repository :

```shell
git clone https://github.com/Litibe/P10.git
```

---

## Environnement Virtuel :

création de l'environnement virtuel

```shell
python3 -m venv [nom_de_votre_environnement_virtuel]
```

activation de l'environnement virtuel

### Mac/Linux

```shell
source [nom_de_votre_environnement_virtuel]/bin/activate
```

### Windows

```shell
source .\[nom_de_votre_environnement_virtuel]\Scripts\activate
```

Aller dans le dossier P10 contenant les fichiers

```shell
cd P10
```

---

## Installation des packages nécessaires

```shell
pip install -r requirements.txt
```

---

## Lancement du programme :

Exécution du serveur local Django via la commande :

```shell
python manage.py runserver
```

Cette commande produit le resultat suivant :
en effet, le programme dispose d'une interface dans le terminal.

```shell
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
DATE - HEURE
Django version 4.0, using settings 'softDesk.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Vous pouvez lancer votre navigateur web avec le lien [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Connexion au Site web généré par le serveur Django :

le lien [http://127.0.0.1:8000/](http://127.0.0.1:8000/) affichera une simple page d'accueil de l'application afin d'avoir accès à la documentation des différents points de terminaison API créés.

Différents utilisateurs ont été construit pour la "démonstration".
Voici la liste des utilisateurs, ayant tous le mot de passe : motdepasse2022 :

<ul>
<li>motdepasse2022@lioneltissier.fr</li>
<li>motdepasse2022@djangotest2.fr</li>
<li>motdepasse2022@djangotest3.fr</li>
</ul>
L'utilisateur 3 n'est intégré dans aucun projet.

---

## Utilisation du programme :

L'API SoftDesk permet :

<ul>
<li>La création de projet, ainsi que l'attribution de collaborateur (PROJECT)</li>
<li>La saisie de problème pour un projet donné, et l'atribution de la résolution du dit problème à un utilisateur précis (ISSUE)</li>
<li>Pour chaque problème, l'auteur du problème ou son utilisateur attribué peuvent ajouter des commentaires. (COMMENT)</li>
</ul>

---

## Respect PEP8 :

Après avoir activé l'environnement virtuel, vous pouvez entrez la commande suivante :

```
flake8 --format=html --htmldir=flake_rapport --config=flake8.ini
```

Un rapport sous format HTML sera généré dans le dossier "flake_rapport", avec comme argument "max-line-length" défini par défaut à 79 caractères par ligne si non précisé.
Dans le fichier de configuration "flake8.ini", est exclu le dossier env/, settings.py, manage.py, ainsi que les dossiers migrations générés par Django.

---

## Points de terminaison API :

La documentation PostMan présente à l'adresse : [https://documenter.getpostman.com/view/16769688/UVXdQegN](https://documenter.getpostman.com/view/16769688/UVXdQegN) permettra à tous utilisateurs enregistrés et connectés de façon sécurisée avoir accès aux différentes méthodes CRUD des liens associés.

Une fonctionnalité de TEST de tous les points de terminaisons a été conçue dans Django sous la requete :

```shell
python manage.py test
Found 20 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
[...]
Ran 20 tests in 15.971s
OK
Destroying test database for alias 'default'...
```

qui testera l'ensemble des points de terminisons, utilisateurs refusés puis autorisés à l'accès des données.

Des tests précis peuvent être réalisés via les commandes terminales suivantes :

```shell
python manage.py test softDeskApi.tests.Test_A_Users
```

```shell
python manage.py test softDeskApi.tests.Test_B_Projects
```

```shell
python manage.py test softDeskApi.tests.Test_C_ProjectDetails
```

```shell
python manage.py test softDeskApi.tests.Test_D_ContributorProject
```

```shell
python manage.py test softDeskApi.tests.Test_E_IssuesProject
```

```shell
python manage.py test softDeskApi.tests.Test_F_CommentProject
```
