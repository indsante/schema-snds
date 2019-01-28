# Installation du projet

Note : Cette procédure devrait fonctionner sur Linux et Mac. Il faut la tester et la compléter pour Windows.

## Dépendances

Le projet utilise `Python3` et des librairies listées dans le fichier [requirements](requirements.txt). 

Nous recommendons d'installer ces dépendances dans un environnement virtuel.

Tester l'installation de `Python3` et `virtualenv` avec ces commandes

    python3 --version
    pip3 --version
    virtualenv --version

Installer `virtualenv` si besoin avec la commande :  `pip3 install virtualenv`

## Installation 

Cloner le projet en local

    git clone https://gitlab.com/SNDS/database-schema.git
    cd database-schema

Créer un environnement virtuel et l'activer

    virtualenv venv --python=python3
    source venv/bin/activate

Installer les dépendances python 

    pip3 install -r requirements.txt

Tester l'installation

    python -m pytest tests

## Docker et Docker-Compose

Docker simplifie l'installation de services, indépendamment de votre système d'exploitation. 
Nous l'utilisons notamment pour démarrer rapidement des bases de données.

Docker-Compose simplifie la configuration et la composition de services Docker.

Une fois installé, installer et démarrer les services avec la commande `docker-compose up`
