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

## Docker

Docker permet d'installer et de lancer rapidement des bases de données. 

Une fois Docker installé, la commande suivante démarre une base PostgreSQL.
 `docker run --rm -p 5432:5432 postgres` 
 
Cette base est accessible en local (adresse `localhost:5432/postgres`), sans mot de passe, avec l'utilisateur `postgres`.  