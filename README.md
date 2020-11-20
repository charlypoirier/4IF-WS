# 4IF-WS
Projet 4IF - Web sémantique - Moteur de recherche sémantique sur le thème de la littérature


## Prérequis

L'application nécessite python >= 3.8 .

## Installation avec un environnement virtuel

Clonez le repot :  
`git clone https://github.com/charlypoirier/4IF-WS.git `

Déplacez vous deans la racine du projet, puis créez un environnement virtuel  
```python3 -m venv env```    
Lancez l'environnement virtuel  
``` source env/bin/activate ```  

Une indication visuelle doit apparaître dans votre terminal, par exemple avec bash le nom de l'environnement entre parenthèse au début de la ligne.

Installez les packages Flask et SPARQLWrapper :  
` pip install Flask `  
` pip install SPARQLWrapper `

Lorques vous aurez fini d'utiliser l'application, tapez ` deactivate ` pour sortir de l'environnement virtuel.


## Installation sans environnement virtuel

Installez les packages SPARQLWrapper et FLASK :   
` pip install Flask `  
` pip install SPARQLWrapper `

## Lancement  

Pour lancer l'application, vous pouvez simplement exécuter le script **runserver** depuis la racine du projet :
`./runserver`

Si pour une raison quelquonque cela ne marque pas : 

- Exportez les variables d'environnement FLASK_APP et FLASK_ENV.  
` export FLASK_APP=run.py `  
` export FLASK_ENV=development `  

- Lancez l'application avec la commande suivante :  
`flask run` 

## Voir aussi 
- [FLask (Création d'un environnement virtuel, téléchargement de Flask)](https://flask.palletsprojects.com/en/1.1.x/installation/): 
- [SPARQLWrapper](https://sparqlwrapper.readthedocs.io/en/latest/main.html)

## Contact
Hexanome 4414 :
- Lucie Clémenceau
- Sylvain de Verclos
- Jérôme Hue
- Yohan Meyer
- Charly Poirier
- Quentin Regaud



