import django_filters
from django.db.models import Q
from .models import Catalogo, Categoria

class CatalogoFilter(django_filters.FilterSet):
    """Filtri avanzati per Catalogo"""
    
    # Ricerca testuale in tutti i campi nome multilingua
    search = django_filters.CharFilter(method='search_filter')
    
    # Filtri esatti
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    # Filtri di range per data creazione
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
        fields = ['is_active']
    
    def search_filter(self, queryset, name, value):
        """Ricerca in tutti i campi nome multilingua"""
        return queryset.filter(
            Q(nome_it__icontains=value) |
            Q(nome_en__icontains=value) |
            Q(nome_fr__icontains=value) |
            Q(nome_es__icontains=value) |
            Q(slug__icontains=value)
        )


class CategoriaFilter(django_filters.FilterSet):
    """Filtri per Categoria"""
    
    # Ricerca testuale in tutti i campi nome multilingua
    search = django_filters.CharFilter(method='search_filter')
    
    # Filtro per catalogo
    catalogo = django_filters.NumberFilter(field_name='catalogo__id')
    
    # Filtro per categorie con/senza parent
    has_parent = django_filters.BooleanFilter(method='filter_has_parent')
    
    # Filtro per categorie attive
    is_active = django_filters.BooleanFilter(field_name='is_active')
    
    class Meta:
        model = Categoria
        fields = ['catalogo', 'parent', 'is_active']
    
    def search_filter(self, queryset, name, value):
        """Ricerca in tutti i campi nome multilingua"""
        return queryset.filter(
            Q(nome_it__icontains=value) |
            Q(nome_en__icontains=value) |
            Q(nome_fr__icontains=value) |
            Q(nome_es__icontains=value) |
            Q(slug__icontains=value)
        )
    
    def filter_has_parent(self, queryset, name, value):
        """Filtra categorie con/senza parent (top-level o sottocategorie)"""
        if value:
            return queryset.exclude(parent__isnull=True)
        return queryset.filter(parent__isnull=True)