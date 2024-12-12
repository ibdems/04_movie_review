from allauth.account.forms import SignupForm
from django import forms

from myauth.models import User


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=70, min_length=3, required=True)
    last_name = forms.CharField(max_length=40, min_length=2, required=True)

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user

    def clean_email(self):
        email = super().clean_email()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email existe deja")

        return email
