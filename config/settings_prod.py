import os

import dj_database_url
import environ

from .settings import *  # Importer les configurations de base

# Initialisation d'Environ
env = environ.Env(DEBUG=(bool, False))  # DEBUG est par défaut False

# Définition du répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Lecture des variables d'environnement depuis le fichier .env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Clé secrète pour sécuriser Django
SECRET_KEY = env("SECRET_KEY")

# Mode DEBUG (doit rester False en production)
DEBUG = env("DEBUG")

# Hôtes autorisés à accéder à l'application
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

# Configuration de la base de données
DATABASES = {
    "default": dj_database_url.config(conn_health_checks=True)  # Vérifications de santé activées
}

# Configuration AWS S3
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = "eu-west-3"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# Static and Media settings
STATICFILES_LOCATION = "static"
MEDIAFILES_LOCATION = "media"

# Static and Media URLs
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/movie/{STATICFILES_LOCATION}/"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/movie/{MEDIAFILES_LOCATION}/"

# Cache control for static files
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",  # Cache pour 1 jour
}

# File Overwrite
AWS_S3_FILE_OVERWRITE = False  # Ne pas écraser les fichiers existants

# Storage backend configuration
STORAGES = {
    "default": {
        "BACKEND": "movie.storages.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        "OPTIONS": {
            "location": STATICFILES_LOCATION,
        },
    },
}

# collectstatic configuration for S3
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

# Configuration des logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

# Configuration CSRF et HTTPS
CSRF_TRUSTED_ORIGINS = ["https://movie.devibrahima.online"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Paramètres de sécurité HTTPS renforcés
SECURE_HSTS_SECONDS = 31536000  # Active HSTS pendant 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applique HSTS aux sous-domaines
SECURE_HSTS_PRELOAD = True  # Indique aux navigateurs de précharger HSTS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Empêche la détection MIME par le navigateur
SECURE_BROWSER_XSS_FILTER = True  # Active le filtre XSS intégré au navigateur
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Configuration des administrateurs
ADMINS = [("Ibrahima", "ibrahima882001@gmail.com")]

# Paramètre facultatif : Configuration des e-mails (exemple avec SMTP Gmail)
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
# EMAIL_PORT = env("EMAIL_PORT", default=587)
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
