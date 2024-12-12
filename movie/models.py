import uuid

from django.db import models
from django.utils import timezone

from myauth.models import User

# Create your models here.


class Cast(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    titre = models.CharField(max_length=200)
    synopsis = models.TextField(max_length=300, null=True, blank=True)
    release_date = models.DateField(verbose_name="Date de sortie")
    genre = models.ManyToManyField(Genre, related_name="movies")
    cast = models.ManyToManyField(Cast, related_name="movies")
    image = models.ImageField(upload_to="film/", null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    average_rating = models.IntegerField(verbose_name="Note", default=0)
    tmbd_id = models.IntegerField(unique=True, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="movie"
    )


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="review_movie")
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} ({self.rating}/5)"


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comment_review")
    comment = models.CharField(max_length=255)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_user"
    )
    date_published = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Commenter par {self.user} pour {self.review}"
