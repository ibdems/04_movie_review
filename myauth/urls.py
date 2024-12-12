from django.urls import include, path

from myauth.views import CustomSignupView

urlpatterns = [
    path("signup/", CustomSignupView.as_view(), name="account_signup"),
    path("", include("allauth.urls")),
]
