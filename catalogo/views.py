from rest_framework import viewsets #importa classe base ViewSet
from rest_framework.permissions import IsAuthenticated #Permesso che richiede autenticazione

from .models import Catalogo, Categoria, Cartelle
from .serializers import CatalogoSerializer, CategoriaSerializer, CartelleSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CatalogoFilter, CategoriaFilter

class CatalogoViewSet(viewsets.ModelViewSet): #ViewSet per gestire operazioni CRUD su Catalogo
     """
     Endpoint generati:
    - GET    /api/cataloghi/       → Lista tutti i cataloghi
    - POST   /api/cataloghi/       → Crea nuovo catalogo
    - GET    /api/cataloghi/{id}/  → Dettaglio catalogo
    - PUT    /api/cataloghi/{id}/  → Modifica completa catalogo
    - PATCH  /api/cataloghi/{id}/  → Modifica parziale catalogo
    - DELETE /api/cataloghi/{id}/  → Elimina catalogo
    """

     queryset = Catalogo.objects.all() #Recupera tutti gli oggetti Catalogo
     serializer_class= CatalogoSerializer #Specifica il serializer da usare per convertire Model in JSON e viceversa
     permission_classes=[IsAuthenticated] #Solo utenti loggati possono accedere a queste API
     # Filtri
     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
     filterset_class = CatalogoFilter
     search_fields = ['nome', 'descrizione']
     ordering_fields = ['nome', 'created_at', 'is_active']
     ordering = ['-created_at']  # Ordinamento default

class CategoriaViewSet(viewsets.ModelViewSet):
        """
        Endpoint generati:
        - GET    /api/categorie/       → Lista tutte le categorie
        - POST   /api/categorie/       → Crea nuova categoria
        - GET    /api/categorie/{id}/  → Dettaglio categoria
        - PUT    /api/categorie/{id}/  → Modifica completa categoria
        - PATCH  /api/categorie/{id}/  → Modifica parziale categoria
        - DELETE /api/categorie/{id}/  → Elimina categoria

        Include filtro per catalogo tramite query param:
        - GET /api/categorie/?catalogo=1 → Filtra categorie per catalogo con id=1
        """
        #Fa una sola query ottimizzata per recuperare catalogo e parent associati
        #Fa un SQL JOIN e prende anche i dati del catalogo e del parent
        queryset = Categoria.objects.select_related('catalogo', 'parent').all()
        serializer_class = CategoriaSerializer
        permission_classes = [IsAuthenticated]
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_class = CategoriaFilter
        search_fields = ['nome']
        ordering_fields = ['nome', 'ordine']

class CartelleViewSet(viewsets.ModelViewSet):
        """
        Endpoint generati:
        - GET    /api/cartelle/       → Lista tutte le cartelle
        - POST   /api/cartelle/       → Crea nuova cartella
        - GET    /api/cartelle/{id}/  → Dettaglio cartella
        - PUT    /api/cartelle/{id}/  → Modifica completa cartella
        - PATCH  /api/cartelle/{id}/  → Modifica parziale cartella
        - DELETE /api/cartelle/{id}/  → Elimina cartella

        Include filtro per categoria e tipo_file. 
        Ottimizzazione: prefetch delle relazioni many-to-many.
        """
        # Ottimizza query prefetchando le relazioni ManyToMany con cataloghi e categorie
        queryset = Cartelle.objects.prefetch_related(
            'cataloghi',      # Relazione M2M con Catalogo
            'categorie',      # Relazione M2M con Categoria
            'categorie__catalogo'  # Catalogo associato alle categorie
        ).all()
        serializer_class = CartelleSerializer
        permission_classes = [IsAuthenticated]