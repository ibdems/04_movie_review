from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.http import HttpRequest

from movie.utils import save_all_movies
from .models import Cast, Movie, Review, Genre, Comment


admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    actions = ['deactivate_users']

    @admin.action(description="Désactiver les utilisateurs sélectionnés")
    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('titre', 'release_date', 'average_rating')
    list_filter = ('release_date', 'genre')
    exclude = ['id', 'uid', 'average_rating', 'poster_url', 'tmbd_id']
    search_fields = ('titre', 'description')
    actions = ['import_movies_from_tmdb']

    # Afficher les actions même sans sélection
    actions_on_top = True
    actions_on_bottom = True

    # Fonction pour importer les films dans le admin
    def import_movies_from_tmdb(self, request, queryset):
        print("Appel de la fonction d'importation")
        result_message = save_all_movies()
        self.message_user(request, f"Importation terminée : {result_message}")
    
    import_movies_from_tmdb.short_description = 'Importer tous les films depuis TheMovieDB'
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('movie__titre', 'user__first_name')
    readonly_fields = ('created_at',) 

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment')
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        return queryset.filter(user=request.user)

# Personnalisation de l'affichage du modèle Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser 

@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
