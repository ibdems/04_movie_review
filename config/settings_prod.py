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

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")  # Région par défaut
AWS_QUERYSTRING_AUTH = False  # Désactive les URL signées pour les fichiers publics

# Configuration des fichiers statiques
STATIC_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/movie/static/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Configuration des fichiers médias (facultatif)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/movie/media/"
