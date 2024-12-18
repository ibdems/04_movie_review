from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = "movie/media"  # Dossier "media" dans le bucket S3
    file_overwrite = False  # Empêche l'écrasement des fichiers ayant le même nom
