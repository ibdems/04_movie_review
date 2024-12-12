from django.db.models import Avg
from rest_framework import serializers

from movie.models import Cast, Comment, Genre, Movie, Review


class CastSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ["name"]


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name"]


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment", "user", "date_published"]
        read_only_fields = ["date_published"]


class ReviewSerializers(serializers.ModelSerializer):
    comment_review = CommentSerializers(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ["movie", "content", "rating", "user", "comment_review", "created_at"]
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        movie = validated_data["movie"]
        review = super().create(validated_data)

        average_rating = Review.objects.filter(movie=movie).aggregate(avg_rating=Avg("rating"))[
            "avg_rating"
        ]

        movie.average_rating = average_rating if average_rating else 0
        movie.save()

        return review

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class MovieSerializers(serializers.ModelSerializer):
    cast = CastSerializers(many=True)
    genre = GenreSerializers(many=True)
    user = serializers.StringRelatedField()
    review_movie = ReviewSerializers(many=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "titre",
            "synopsis",
            "release_date",
            "genre",
            "cast",
            "poster_url",
            "average_rating",
            "review_movie",
            "user",
        ]
        read_only_fields = ["id", "average_rating"]


class MovieListSerializers(serializers.ModelSerializer):
    genre = GenreSerializers(many=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "titre",
            "synopsis",
            "release_date",
            "genre",
            "poster_url",
            "average_rating",
        ]
        read_only_fields = ["id", "average_rating"]
