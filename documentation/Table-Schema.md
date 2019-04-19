# Table Schema

## Spécification

[Table Schema](https://frictionlessdata.io/specs/table-schema/) est une spécification 
qui permet de décrire formellement le schéma de données tabulaires.

Une table est décrite principalement par 
- une liste de `fields` (champ, colonne)
- une [primaryKey](https://fr.wikipedia.org/wiki/Cl%C3%A9_primaire) (optionnelle)
- des [foreignKeys](https://fr.wikipedia.org/wiki/Cl%C3%A9_%C3%A9trang%C3%A8re) (optionnelles)

Un `field` est principalement décrit par 
- un `name` (seul champ obligatoire)
- un `title` plus lisible
- une `description`
- un `type`, parmi une liste extensible [string, number, integer, boolean, date, etc.]
- un `format`, qui précise le type (ex : format de la date)
- des `constraints`, telles que valeurs min et max, listes de modalités autorisées, etc.
 
Cette spécification est extensible librement. 
Ils est donc possible d'ajouter des catégories d'informations spécifiques aux données considérées.

Un schema qui suit la spécification Table Schema est enregistré au format
[json](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation).

## Intérêt

La spécification Table Schema est facilement lisible par des humains, **et** manipulable informatiquement.
 
Ce standard est indépendant de tout logiciel ou langage, il est donc extrêmement portable.

Des outils génériques existent pour manipuler les schémas suivant cette spécification, par exemple
- [tableschema-py](https://github.com/frictionlessdata/tableschema-py) est un outil Python (ou CLI), 
qui permet d'inférer, manipuler et valider des schémas
- [tableschema-r](https://github.com/frictionlessdata/tableschema-r) est un outil R similaire 
- [goodtables-py](https://github.com/frictionlessdata/goodtables-py) est un outil Python (ou web), 
qui permet de valider qu'un fichier de données respecte un schéma
- [table-schema-to-markdown](https://github.com/AntoineAugusti/table-schema-to-markdown)
permet de créer un fichier de documentation Markdown à partir d'un fichier Table Schema.

Nous souhaitons par ailleurs développer des outils permettant de
- créer les objets correspondants dans des bases relationnelles 
(via l'outil [sqlalchemy](https://docs.sqlalchemy.org/)) 
- créer des diagrammes relationels entre tables 
(a priori en utilisant la brique précédente + [schemacrawler](https://www.schemacrawler.com/))
- générer des données synthétiques

Plus généralement, l'adoption de la spécification Table Schema est encouragée pour améliorer la qualité des données publiées en open-data.

Etalab référence ainsi quelques schemas de données publiques sur [GitHub](https://github.com/etalab/schema.data.gouv.fr).

## Descripteur type d'une table

```json
{
  // 'fields' est une liste ordonnée de descripteurs de colonnes
  "fields": [ 
    {
      "name": "Nom de la colonne", // OBLIGATOIRE 
      "title": "Titre plus lisible",
      "description": "Description de la colonne",
      "type": "Chaîne de caractères spécifiant le type",
      "format": "Chaîne de caratères spécifiant le format",
      "constraints": {
        // descripteurs de contraintes sur la colonne (ex: unicité des valeurs)
      }
    }
    // Autres descripteurs de colonnes
  ],
  // Spécification (optionnelle) de la clé primaire
  "primaryKey": "Nom de la colonne, ou liste de nom de colonnes séparées par des virgules",
  // Spécification (optionnelle) des clés étrangères
  "foreignKeys": [
    {
      "fields": "Nom (ou liste) de la colonne  de la table",
      "reference": {
        "resource": "Nom de la table référencée",
        "fields": "Nom (ou liste) de la colonne de la table référencée"
      }
    }
  ]
}
```

