from django import forms

from movie.models import Comment, Review
from myauth.models import User


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["content", "rating"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ["review", "comment"]


class ProfileForm(forms.ModelForm):
    password = forms.CharField(required=False)
    password_confirm = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile", "bio"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)  # Met à jour le mot de passe
        if commit:
            user.save()
        return user
