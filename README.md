# oc_1_scrapping

Utilisez les bases de Python pour l'analyse de marché

# Suivez les étapes ci-dessous pour mettre en place le projet sur votre poste de travail personnel

1. Clonnez le projet sur votre poste de travail personnel : # git clone lien_vers_le_repository
2. Créez un environnement virtuel : # python -m venv nom_environnement_virtuel
3. Activez l'environnement virtuel (sous Windows) : # .\venv\Scripts\activate
4. Installez les packages depuis le fichier "requirements.txt" : # pip install -r requirements.txt
5. Exécutez le script : # python main.py

# Fonctionnement du Script

Le rôle du script est d'extraire les informations de tous les livres présents sur le site : http://books.toscrape.com/index.html

Un répertoire "data" sera automatiquement créé lors du lancement du script. Ce répertoire contiendra toutes les données extraites depuis le site mentionné ci-dessus.

Dans le répertoire "data" d'autres sous-dossiers seront créé, pour chaque catégorie avec le contenu suivant : un fichier .csv contenant les données de chaque livre d'une catégorie, un répertoire "img" contenant les images de chaque livre.
