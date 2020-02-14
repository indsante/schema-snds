# Installation du projet

## Copier le projet en local

**Dépendance**

[git](https://git-scm.com/book/fr/v1/D%C3%A9marrage-rapide-Installation-de-Git)
est le système de gestion de versions du code.

Pour windows, on recommande le terminal `gitbash` pour utiliser git et docker. 

Commande

    git clone https://gitlab.com/healthdatahub/schema-snds.git 
    

## Activation d'un environnement virtuel Python avec les dépendances installées

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
    
    Sur Linux : source venv/bin/activate
    Sur Windows : venv/Scripts/activate
    

2- Installer les dépendances Python 


    pip3 install -r requirements.txt

3- Lancer les tests du projet


    python -m pytest tests

**Usage**

Utiliser le point d'entrée du programme


    ./main.py -h

## Installation de la librairie javascript


1- Installation de npm

    https://nodejs.org/en/

2- Installation des dépendances 

    npm install -g @opendataschema/table-schema-to-markdown 


## Installation Docker

Docker permet d'utiliser PostgreSQL et SchemaCrawler pour générer un diagramme relationnel. 

Il est également possible d'exécuter tout le code Python dans une image Docker, évitant d'éventuels problèmes sur Windows. 

**Dépendances**

- [Docker](https://docs.docker.com/engine/installation/) 
simplifie l'installation de services, indépendamment du système d'exploitation. 

- [Docker-Compose](https://docs.docker.com/compose/install/) 
simplifie la configuration et la composition de services Docker.


**Installer et démarrer les services**

*Note: cette étape télécharge des images Docker volumineuses.*


    docker-compose up -d
    

**Usage**

Pour lancer un service en particulier, par exemple SchemaCrawler

    docker-compose up schemacrawler

Pour arrêter tous les services
    
    docker-compose stop

Pour tester des modifications du code python, on peut rentrer dans l'image docker

    docker-compose run --rm python bash


Pour le reste, se référer à la documentation de Docker-Compose.
