# Installation du projet


*Note : Cette procédure **devrait** fonctionner sur Linux et Mac. Il faut la tester et la compléter pour Windows.*

Nous détaillons 2 étapes d'installation 

1. La première étape utilise uniquement Docker. L'installation est simplifiée.
2. La seconde étape permet d'éxécuter le code Python sans Docker. Le développement est alors simplifié. 

## 1- Installation pure Docker

Cette installation utilise Docker pour exécuter le code Python, 
ainsi que d'autres services tels que PostgreSQL et SchemaCrawler.

**Dépendances**

- [Docker](https://docs.docker.com/engine/installation/) 
simplifie l'installation de services, indépendamment du système d'exploitation. 

- [Docker-Compose](https://docs.docker.com/compose/install/) 
simplifie la configuration et la composition de services Docker.

- [git](https://git-scm.com/book/fr/v1/D%C3%A9marrage-rapide-Installation-de-Git)
est le système de gestion de versions du code

- Pour windows, on recommande le terminal [gitbash](https://gitlab.com/DREES/tutoriels/blob/master/tutos/INSTALLATION_GIT_EXE.md) pour utiliser git et docker. **Il faut ajouter `winpty` devant chaque commande Docker pour l'utiliser.**


**Installation**

0- Copier le projet en local


    git clone https://gitlab.com/SNDS/schema-snds.git
    cd database-schema


1- Installer et démarrer les services

*Note: cette étape télécharge des images Docker volumineuses.*


    docker-compose up -d
    

**Usage**

Pour lancer un service en particulier, par exemple SchemaCrawler

    docker-compose up schemacrawler

Pour arrêter tous les services
    
    docker-compose stop

Pour tester des modifications du code python, on peut rentrer dans l'image docker:

    docker-compose run --rm python bash


Pour le reste, se référer à la documentation de Docker-Compose.

## 2- Installation permettant d'exécuter le code Python sans Docker

Cette deuxième étape permet d'exécuter le code Python sur votre système hôte, sans Docker.
Les autres services sont toujours executés via Docker.

**Dépendances**

Le projet utilise `Python3` et des librairies listées dans le fichier [requirements](requirements.txt). 

Nous recommendons d'installer ces dépendances dans un environnement virtuel.

Tester l'installation de `Python3` et `virtualenv` avec ces commandes

    python3 --version
    pip3 --version
    virtualenv --version

Installer `virtualenv` si besoin avec la commande :  `pip3 install virtualenv`

**Installation**

1- Créer un environnement virtuel et l'activer


    virtualenv venv --python=python3
    source venv/bin/activate

2- Installer les dépendances Python 


    pip3 install -r requirements.txt

3- Lancer les tests du projet


    python -m pytest tests

**Usage**

Utiliser le point d'entrée du programme


    python ./main.py
