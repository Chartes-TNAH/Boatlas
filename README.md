
# Boatlas
Gazetteer produit dans le cadre du cours Python de l'Ecole Nationales des Chartes
3 personnes maximum

Il s'agira de modifier l'application Gazetteer développée pendant le cours afin de

1. Ajouter des connexions entre les lieux et les gérer
2. Ajouter la capacité de lier des articles ou des ressources bibliographiques à des lieux
3. Ajouter des tests et une documentation

Compléter l'API :
- Avec les nouvelles données
- Ajouter à la fonction de navigation API places la capacité de rechercher sur un rectangle de coordonnées latmin, latmax,longmin, longmax

(Optionnel)
- Ajoutez la capacité de chercher X kilomètres autour d'une longitude / latitude (Lien et Article sur la question)
- Ajouter une page A propos où vous décrirez l'API

## Installation
Pré-requis: Python 3 et MySQL.

### OS X
### python 3 et MySQL
Vous devez avoir installé Python et Mysql sur votre poste. Avant l’installation de Python, vous devez installer le gestionnaire de paquets HomeBrew (équivalent apt-get sous linux)

Installation de HomeBrew Pour installer Homebrew, ouvrez le Terminal et exécutez
`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)`

Pour installer Python 3:
` brew install python3`

Pour lancer un environnement virtuel:

`pip install virtualenv`

Installation Mysql:
 ` brew install mysql`

###Première utilisation
Téléchargez le dossier Boatlas depuis Github.
Placez vous dans le dossier Boatlas dans un terminal et tapez :
`virtualenv ~/.Boatlas -p python3`
Cela crée un environnement virtuel. Pour l'activez, tapez la commande :
`source activate Boatlas`

Tapez ensuite
`pip install -r requirements.txt`
pour installer les packages nécessaires au fonctionnement de l'application.

Lancez l'application avec
`python3 run.py`

###Utilisations suivantes:

A partir du terminal, lancez l'environnement virtuel puis lancez l'application:
`source activate Boatlas`
et
`python3 run.py`


### Linux (Ubuntu/Debian)
###Première utilisation  
Pour installer Python3 et l'environnement virtuel, ouvrez un terminal et tapez :  
`sudo apt-get install python3 python3-pip python3-virtualenv python3-dev libmysqlclient-dev libfreetype6-dev`  
et  
`sudo apt install virtualenv`  

Téléchargez les dossiers de l'application sur Github.
Depuis son dossier dans un terminal, tapez :  
`virtualenv ~/.dicoproso -p python3`  pour initialiser l'environnement virtuel.
Pour l'activer, utilisez:
`source ~/.dicoproso/bin/activate`  

Dans le même terminal, tapez :  
`pip install -r requirements.txt` pour installer les différents packages nécessaires pour faire tourner l'application.  

Pour lancer l'application, tapez :  
`python3 run.py`  

### Utilisations ultérieures :
A partir du terminal, lancez l'environnement virtuel puis lancez l'application:
`source ~/.dicoproso/bin/activate`  
et
`python3 run.py`

## Pour chargez la base de données sql
Nous avons déjà installé MySQL, créez-vous un compte administrateur si ça n'est pas déjà fait.
Deux possibilités s'offrent à vous:
Utilisez MySQL Workbench: y ouvrir le fichier datamodel.sql et exécutez-le. La base est installée.

ou

dans le terminal
mysql -uroot -p < gazetteer/donnees_sql/datamodel.sql

### Pour tester la fonction de reception des mails d'erreurs:
Ce mettre dans une nouvelle fenêtre du terminal toujours dans l'environnement virtuel en utilisant le *SMTP debugging server* de Python. Il s'agit d'un faux service de serveur mail qui les imprime en fait sur le terminal.
 `python -m smtpd -n -c DebuggingServer localhost:8025`

Dans la première fenêtre du terminal:
`export FLASK_DEBUG=0`
`export MAIL_SERVER=localhost`
`MAIL_PORT=8025`
Provoquez une erreur SQL pour recevoir un message d'erreur!
