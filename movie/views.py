from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django_filters.views import FilterView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.contrib import messages
from django.urls import reverse

from movie.filters import MovieFilter
from movie.forms import CommentForm, ProfileForm, ReviewForm 
from movie.models import Comment, Movie, Review
from myauth.models import User

# Create your views here.
class IndexView(FilterView, ListView):
    template_name =  "movie/index.html"
    model = Movie
    filterset_class = MovieFilter
    paginate_by = 9
    context_object_name = 'movies'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['movie'] = Movie.objects.last()
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-average_rating').prefetch_related('genre')
        return queryset
    
class DetailMovie(DetailView):
    model = Movie
    context_object_name = 'movie'
    pk_url_kwarg = 'uid'

    def get_object(self):
        return Movie.objects.get(uid=self.kwargs.get('uid'))
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.prefetch_related('genre', 'cast', 'review_movie')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        movie = self.get_object()
        user = request.user
        
        if form.is_valid():
            content = form.cleaned_data['content']
            rating = form.cleaned_data['rating']
            
            if content == '' and rating is None:
                messages.error(request, "Vous devez soit mettre une critique ou une note")
            else:
                review_user = Review.objects.filter(movie=movie, user=user)
                
                if review_user.exists():
                    messages.error(request, "Vous ne pouvez pas laisser deux critiques ou notes")
                else:
                    review = form.save(commit=False)
                    review.movie = movie
                    review.content = content
                    review.rating = rating
                    review.user = user
                    review.save()

                    # Calcul de la moyenne des notes
                    average_rating = Review.objects.filter(movie=movie).aggregate(avg_rating=Avg('rating'))['avg_rating']
                    
                    # Mettre a jour la colonne average_rating
                    movie.average_rating = average_rating if average_rating else 0
                    movie.save()

                    messages.success(request, "Critique ou note effectuée avec succès")
                    return redirect('detail_movie', uid=self.get_object().uid)
        
        else:
            messages.error(request, "Échec lors de l'enregistrement")
            print(form.errors)
        
        return redirect('detail_movie', uid=self.get_object().uid)

class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'movie/movie_detail.html'

    def form_valid(self, form):
        # User connecter a User de comment
        form.instance.user = self.request.user
        self.object = form.save()
        movie_uid = form.instance.review.movie.uid
        return redirect('detail_movie', uid=movie_uid)

    
class EditReviewView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'movie/movie_detail.html'

    def form_valid(self, form):
        review = form.save(commit=False)
        movie = review.movie

        # Mettre à jour la critique avec les nouvelles données
        review.content = form.cleaned_data['content']
        review.rating = form.cleaned_data['rating']
        review.save()

        # Recalculer la moyenne des notes après la modification
        movie.average_rating = Review.objects.filter(movie=movie).aggregate(avg_rating=Avg('rating'))['avg_rating']
        movie.save()

        messages.success(self.request, "Votre critique ou note a été modifiée avec succès")
        return redirect('detail_movie', uid=movie.uid)

class DeleteReviewView(DeleteView):
    model = Review

    def get_success_url(self):
        return reverse('detail_movie', kwargs={'uid': self.get_object().movie.uid})

    def delete(self, request, *args, **kwargs):
        review = self.get_object()
        movie = review.movie
        review.delete()

        # Recalculer la moyenne des notes après suppression
        movie.average_rating = Review.objects.filter(movie=movie).aggregate(avg_rating=Avg('rating'))['avg_rating']
        movie.save()

        messages.success(request, "Votre critique a été supprimée avec succès")
        return redirect('detail_movie', uid=movie.uid)

class MyProfileView(LoginRequiredMixin, DetailView):
    template_name = 'movie/profile.html'
    model = User
    context_object_name = 'profile'

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('movie_user', 'review_user', 'comment_user')

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.get_object())

        if form.is_valid():
            user = form.save(commit=True)  # Enregistre l'utilisateur avec les nouvelles informations
            password = form.cleaned_data.get('password')  # Récupère le mot de passe du formulaire

            if password:  # Vérifie si un mot de passe a été soumis
                # Authentifie l'utilisateur avec le nouveau mot de passe
                user = authenticate(email=user.email, password=password)
                if user is not None:
                    login(request, user)  # Connecte l'utilisateur
                    messages.success(request, "Profil modifié avec succès")
                else:
                    messages.error(request, "Échec de la connexion après la mise à jour")
            else:
                messages.success(request, "Profil modifié avec succès")  # Message de succès sans changement de mot de passe

            return redirect('profile')
        else:
            messages.error(request, "Échec lors de la modification du profil")
            print(form.errors)
            return redirect('profile')

