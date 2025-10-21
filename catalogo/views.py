from rest_framework import viewsets #importa classe base ViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly #Permessi

from .models import Catalogo, Categoria, Cartelle
from .serializers import CatalogoSerializer, CategoriaSerializer, CartelleSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CatalogoFilter, CategoriaFilter

from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.http import FileResponse, Http404
from django.conf import settings
import os

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
     permission_classes=[IsAuthenticatedOrReadOnly] #Lettura pubblica, scrittura solo autenticati
     # Filtri
     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
     filterset_class = CatalogoFilter
     search_fields = ['nome_it', 'nome_en', 'nome_fr', 'nome_es', 'slug']
     ordering_fields = ['nome_it', 'created_at', 'is_active']
     ordering = ['-created_at']  # Ordinamento default

     @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
     def cartelle(self, request, pk=None):
         """
         Endpoint custom per ottenere tutte le cartelle di un catalogo specifico.
         
         GET /api/cataloghi/{id}/cartelle/
         
         Restituisce le cartelle associate al catalogo, ordinate per campo 'ordine'
         della tabella intermedia CatalogoCartella.
         """
         catalogo = self.get_object()
         
         # Filtra cartelle attive associate al catalogo, ordinate per CatalogoCartella.ordine
         cartelle = catalogo.cartelle_root.filter(
             is_active=True
         ).order_by('cataloghi_root__ordine')
         
         serializer = CartelleSerializer(cartelle, many=True, context={'request': request})
         
         return Response({
             'count': cartelle.count(),
             'results': serializer.data
         })

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
        permission_classes = [IsAuthenticatedOrReadOnly] #Lettura pubblica, scrittura solo autenticati
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_class = CategoriaFilter
        search_fields = ['nome_it', 'nome_en', 'nome_fr', 'nome_es', 'slug']
        ordering_fields = ['nome_it', 'created_at']

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
        permission_classes = [IsAuthenticatedOrReadOnly] #Lettura pubblica, scrittura solo autenticati


# View per servire file media protetti
@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def serve_protected_media(request, file_path):
    """
    Serve file media protetti da autenticazione.
    
    GET /protected-media/file_catalogo/nome_file.pdf
    
    Solo utenti autenticati possono scaricare file.
    Supporta tutti i tipi di file (PDF, immagini, video, etc.)
    """
    # Costruisci il percorso completo del file
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    # Verifica che il file esista
    if not os.path.exists(full_path):
        raise Http404("File non trovato")
    
    # Verifica che il percorso sia sicuro (previene path traversal attacks)
    if not os.path.abspath(full_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
        raise Http404("Accesso negato")
    
    # Restituisci il file con il content-type appropriato
    return FileResponse(open(full_path, 'rb'))