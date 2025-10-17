import django_filters
from .models import Catalogo, Categoria

class CatalogoFilter(django_filters.FilterSet):
    """Filtri avanzati per Catalogo"""
    
    # Ricerca testuale
    search = django_filters.CharFilter(method='search_filter')
    
    # Filtri esatti
    is_active = django_filters.BooleanFilter(field_name='is_active')
    lingua = django_filters.ChoiceFilter(
        field_name='lingua',
        choices=Catalogo.LINGUE_CHOICES
    )
    
    # Filtri di range
    created_after = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gte'
    )
    created_before = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='lte'
    )
    
    class Meta:
        model = Catalogo
        fields = ['is_active', 'lingua']
    
    def search_filter(self, queryset, name, value):
        """Ricerca in nome e descrizione"""
        return queryset.filter(
            Q(nome__icontains=value) |
            Q(descrizione__icontains=value)
        )


class CategoriaFilter(django_filters.FilterSet):
    """Filtri per Categoria"""
    
    catalogo = django_filters.NumberFilter(field_name='catalogo__id')
    has_parent = django_filters.BooleanFilter(method='filter_has_parent')
    
    class Meta:
        model = Categoria
        fields = ['catalogo', 'parent']
    
    def filter_has_parent(self, queryset, name, value):
        """Filtra categorie con/senza parent"""
        if value:
            return queryset.exclude(parent__isnull=True)
        return queryset.filter(parent__isnull=True)