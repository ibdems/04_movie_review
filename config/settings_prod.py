import os

import dj_database_url
import environ
from settings import *
env = environ.Env(
    DEBUG=(bool, False)  # Par défaut, DEBUG est défini comme un booléen et désactivé (False)
)

# Définition du répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Lecture des variables d'environnement à partir du fichier .env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Clé secrète pour sécuriser Django
SECRET_KEY = env("SECRET_KEY")

# Mode DEBUG (désactivé en production pour des raisons de sécurité)
DEBUG = env("DEBUG")
# Hôtes autorisés à accéder à l'application
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

# Configuration de la base de données
DATABASES = {"default": dj_database_url.config(conn_health_checks=True)}
