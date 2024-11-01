from django.forms import Select, TextInput
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, ChoiceFilter
from movie.models import Genre, Movie

class MovieFilter(FilterSet):
    genre = ModelChoiceFilter(
        queryset=Genre.objects.all(),   
        widget=Select(attrs={'class': 'select-genre'})
    )
    titre = CharFilter(
        field_name='titre', lookup_expr='icontains',
        widget=TextInput(attrs={'class': 'txt-search', 'placeholder': 'Rechercher un film...'})
    )

    average_rating = ChoiceFilter(
        field_name='average_rating',
        widget=Select(attrs={'class': 'select-genre',}),
        choices=[(i, str(i)) for i in range(0, 6)],
    )

    class Meta:
        model = Movie
        fields = ['genre', 'titre']
