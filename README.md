# 4IF-WS
Projet 4IF - Web sémantique - Moteur de recherche sémantique sur le thème de la littérature


### Installation d'un environnement virtuel
Placez vous dans 4IF-WS.

Créer un environnement virtuel  
```python -m venv env```   
Lancer l'environnement virtuel  
``` source env/bin/activate ```  

Une indication visuelle doit apparaître dans votre terminal.

Tapez ``` deactivate ``` pour sortir de l'environnement virtuel.

### Lancement  
## Méthode 1
Une fois l'environnement vrituel activé,
exporter les variables d'environnement suivantes :  
` export FLASK_APP=run.py `  
` export FLASK_ENV=development `  

Lancer depuis le répertoire parent de app avec la commande :  
`flask run` 

## Méthode 2
Une fois l'environnement vrituel activé,
exécutez le script *runserver* : 
``` ./runserver ```

