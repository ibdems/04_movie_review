from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from movie.models import Cast, Comment, Genre, Movie, Review

from .serializers import (
    CastSerializers,
    CommentSerializers,
    GenreSerializers,
    MovieListSerializers,
    MovieSerializers,
    ReviewSerializers,
)


class CreateListMovieView(ListCreateAPIView):
    serializer_class = MovieListSerializers
    queryset = Movie.objects.defer("genre", "cast").all()
    pagination_class = LimitOffsetPagination


class RetrieveUpdateDestroyMovieView(RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    lookup_field = "id"
    serializer_class = MovieSerializers


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers


class CastViewSet(ModelViewSet):
    queryset = Cast.objects.all()
    serializer_class = CastSerializers


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
