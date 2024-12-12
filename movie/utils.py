import requests
from django.utils.dateparse import parse_date

from .models import Cast, Genre, Movie

API_KEY = "ca7dd52bf278eb5d9a4f9fc2ec1bc8c6"
BASE_URL = "https://api.themoviedb.org/3"


def get_movie_data(movie_id):
    """
    Récupère les détails d'un film spécifique, y compris les genres et le casting.
    """
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY, "append_to_response": "credits", "language": "fr-Fr"}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_movies(page=1):
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "fr-Fr", "page": page}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_all_movies(max_pages=5):
    page = 1
    total_pages = 1
    all_movies = []

    while page <= total_pages and page <= max_pages:
        data = get_movies(page)
        all_movies.extend(data["results"])  # Ajouter les résultats de chaque page
        total_pages = data["total_pages"]
        page += 1

    return all_movies


def save_all_movies():
    all_movies_data = get_all_movies()
    movies_to_create = []
    genres_to_create = {}
    casts_to_create = {}
    movie_genres = []
    movie_casts = []

    for movie_data in all_movies_data:
        # Vérifier si le film existe déjà dans la base
        if not Movie.objects.filter(tmbd_id=movie_data["id"]).exists():
            movie_detail = get_movie_data(movie_data["id"])
            poster_path = movie_detail.get("poster_path")
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

            # Préparer les films pour un bulk_create
            movie = Movie(
                titre=movie_detail["title"],
                synopsis=movie_detail["overview"],
                release_date=parse_date(movie_detail.get("release_date", None)),
                tmbd_id=movie_detail["id"],
                poster_url=poster_url,  # Utilisation de poster_url pour stocker l'URL de l'image
            )
            movies_to_create.append(movie)

            # Préparer les genres pour un bulk_create
            for genre_data in movie_detail["genres"]:
                genre_name = genre_data["name"]
                if genre_name not in genres_to_create:
                    genres_to_create[genre_name] = Genre(name=genre_name)
                movie_genres.append((movie, genre_name))  # Stocker la relation film-genre

            # Préparer les casts pour un bulk_create
            for cast_data in movie_detail["credits"]["cast"]:
                cast_name = cast_data["name"]
                if cast_name not in casts_to_create:
                    casts_to_create[cast_name] = Cast(name=cast_name)
                movie_casts.append((movie, cast_name))  # Stocker la relation film-cast

    # Sauvegarder les films en une seule requête
    Movie.objects.bulk_create(movies_to_create, ignore_conflicts=True)

    # Sauvegarder les genres en une seule requête
    Genre.objects.bulk_create(genres_to_create.values(), ignore_conflicts=True)

    # Sauvegarder les casts en une seule requête
    Cast.objects.bulk_create(casts_to_create.values(), ignore_conflicts=True)

    # Maintenant que les films sont créés, récupérer les films en base
    movies_in_db = {
        movie.tmbd_id: movie
        for movie in Movie.objects.filter(tmbd_id__in=[m.tmbd_id for m in movies_to_create])
    }
    genres_in_db = {genre.name: genre for genre in Genre.objects.all()}
    casts_in_db = {cast.name: cast for cast in Cast.objects.all()}

    # Associer les genres aux films
    for movie, genre_name in movie_genres:
        movie_in_db = movies_in_db[movie.tmbd_id]
        genre_in_db = genres_in_db[genre_name]
        movie_in_db.genre.add(genre_in_db)

    # Associer les casts aux films
    for movie, cast_name in movie_casts:
        movie_in_db = movies_in_db[movie.tmbd_id]
        cast_in_db = casts_in_db[cast_name]
        movie_in_db.cast.add(cast_in_db)

    return f"{len(movies_to_create)} films importés."
