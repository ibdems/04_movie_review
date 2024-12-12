from django.urls import path

from .views import (
    CreateCommentView,
    DeleteReviewView,
    DetailMovie,
    EditReviewView,
    IndexView,
    MyProfileView,
)

urlpatterns = [
    path("edit-review/<int:pk>/", EditReviewView.as_view(), name="edit_review"),
    path("delete-review/<int:pk>/", DeleteReviewView.as_view(), name="delete_review"),
    path("", IndexView.as_view(), name="index"),
    path("profile/", MyProfileView.as_view(), name="profile"),
    path("detail/<uid>", DetailMovie.as_view(), name="detail_movie"),
    path("comment/", CreateCommentView.as_view(), name="comment"),
]
