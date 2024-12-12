from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet,CastViewSet, ReviewViewSet, CommentViewSet, CreateListMovieView, RetrieveUpdateDestroyMovieView

router = DefaultRouter()
router.register(r"genre", GenreViewSet)
router.register(r"cast", CastViewSet)
router.register(r"review", ReviewViewSet)
router.register(r"comment", CommentViewSet)


urlpatterns = [
    # Url de l'api
    path("movie/", CreateListMovieView.as_view(), name="api_movie"),
    path("movie/<int:id>/", RetrieveUpdateDestroyMovieView.as_view(), name="api_detail_movie"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        staff_member_required(SpectacularSwaggerView.as_view(url_name="schema")),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + router.urls
