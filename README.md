# <center> ***Projet : Prédiction de la Demande de Vélos en Libre-Service (Bike Sharing Demand)***</center>


## -- Le Contexte

Dans les métropoles modernes, les systèmes de vélos en libre-service (comme le Vélib' à Paris) sont devenus des piliers de la mobilité urbaine. Cependant, pour qu'un tel système soit efficace, il nécessite une logistique précise : une station vide crée de la frustration chez les usagers qui cherchent un vélo, tandis qu'une station pleine empêche ceux qui arrivent de se garer. L'optimisation de la répartition des vélos est donc un défi majeur pour les opérateurs de transport urbain.

## -- L'Objectif du Projet

L'objectif de cette étude est de concevoir un modèle d'apprentissage automatique (Machine Learning) capable de prédire avec précision la demande horaire de location de vélos. Il s'agit d'un problème de Régression, où l'algorithme doit apprendre à estimer une valeur continue (le nombre exact de vélos loués) en se basant sur des données historiques, météorologiques et calendaires.

## -- Le Jeu de Données 

Les données utilisées proviennent de la célèbre compétition Kaggle "Bike Sharing Demand". Le jeu de données rassemble deux années d'historique de location (2011-2012) du programme Capital Bikeshare de Washington D.C., échantillonnées heure par heure.

Le jeu d'entraînement *(train.csv*) contient 10 886 observations nettoyées (aucune valeur manquante), réparties sur les variables suivantes :

### La variable cible (Target) :

- ***count*** : Le nombre total de vélos loués au cours de cette heure spécifique (c'est ce que notre modèle devra deviner).
**Note:** *casual* et *registered* détaillent ce total entre les utilisateurs non-abonnés et abonnés.

### Les caractéristiques temporelles (Features) :

- *datetime* : La date et l'heure exactes de l'observation (ex: 2011-01-01 08:00:00).
- *season*: La saison (1 = Printemps, 2 = Été, 3 = Automne, 4 = Hiver).
- *holiday* : Indique si le jour est un jour férié (1) ou non (0).
- *workingday* : Indique si le jour est un jour de semaine ouvrable (1) ou un week-end/jour férié (0).
  
### Les caractéristiques météorologiques (Features) : 

- *weather* : Une évaluation catégorielle de la météo (1 = Dégagé, 2 = Nuageux/Brouillard, 3 = Pluie légère/Neige, 4 = Fortes intempéries)
- *temp*: La température réelle en degrés Celsius.
- *atemp* : La température "ressentie" en degrés Celsius.
- *humidity* : Le taux d'humidité relative de l'air (en %).
- *windspeed* : La vitesse du vent en Km/h.
- 
## 🚲 CityBike AI : Dashboard de Pilotage Logistique

Ce projet est doté d'une application web B2B développée avec **Streamlit**. Elle permet aux gestionnaires de flottes de vélos en libre-service d'analyser les tendances historiques et de prédire la demande future grâce au Machine Learning.

## ✨ Fonctionnalités
* **Mode Dark SaaS :** Interface UI/UX optimisée.
* **Analytique Historique :** KPIs avec Sparklines et graphiques interactifs (Plotly).
* **Simulateur IA :** Prédiction de la demande en temps réel basée sur un modèle Random Forest.
* **Alerte Logistique :** Détection automatique des risques de rupture de stock.
* **Forecast 24h :** Génération d'une courbe prédictive pour la journée entière avec export CSV.

##  Comment lancer l'application en local

1. Clonez ce dépôt :
`git clone https://github.com/TonPseudo/citybike-ai.git`

2. Installez les dépendances :
`pip install -r requirements.txt`

3. Lancez l'application Streamlit :
`streamlit run app_pro.py`