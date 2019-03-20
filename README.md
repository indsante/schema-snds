# Schema du SNDS

Ce projet cherche à formaliser le schéma relationnel du 
[SNDS](https://www.snds.gouv.fr/SNDS/Qu-est-ce-que-le-SNDS), 
en suivant la spécification [Table Schema](documentation/Table-Schema.md).

Il est développé et maintenu par le Lab Santé à la [DREES](https://drees.solidarites-sante.gouv.fr/etudes-et-statistiques/). 

- Pour installer le projet, se référer au fichier [INSTALL.md](INSTALL.md)
- Pour nous contacter, écrire à [ld-lab-github@sante.gouv.fr](mailto:ld-lab-github@sante.gouv.fr) 
- Les contributions sont bienvenues. Vous pouvez remplir une issue ou ouvrir une pull-request

## Intérêt

Le SNDS est une collection de base de données, difficile à documenter et à manipuler.

Ce schéma du SNDS **centralise** les informations sous un format **standard**, ce qui permet de 
- générer des documentations dans plusieurs formats,
- configurer des codes qui manipulent les données.

## Création 

Le schéma est actuellement généré par le code Python du dossier [src/build_tableschema](src/build_tableschema), 
à partir de la description des tables et variables du dossier [data/sources](data/sources). 

Ces fichiers proviennent d'un travail 
[archivé ici](https://github.com/indsante/dico-snds-creation-archive), 
basé sur des documents de la [Caisse Nationale d'Assurance Maladie](https://assurance-maladie.ameli.fr/qui-sommes-nous). 

À terme, le schéma ne sera plus généré, mais versionné dans le projet et édité à la main.

## Produits dérivés

Deux projets de documentations exploitent actuellement ce schéma :
- un [dictionnaire interactif](https://github.com/indsante/dico-snds) des variables et des liens entre tables, après conversion dans des fichiers csv
- une [documentation collaborative](https://github.com/indsante/Documentation-SNDS), après conversion dans des fichiers markdown

Nous générons également les tables du SNDS dans une base PostgreSQL, puis créons avec 
[SchemaCrawler](http://schemacrawler.com/) un diagramme relationnel au format pdf.

D'autres supports de documentation pourraient être générés selon les besoins. 

Nous projetons notamment d'ajouter des valeurs exemples pour chaque variable, 
puis de générer des jeu de données synthétiques respectant la structure formelle du SNDS.  


## Mentions

Ce projet a été initié dans le cadre du programme 
[« Entrepreneurs d'intérêt général »](https://entrepreneur-interet-general.etalab.gouv.fr/), 
pour le projet [Open Chronic](https://entrepreneur-interet-general.etalab.gouv.fr/defis/2019/openchronic.html).
