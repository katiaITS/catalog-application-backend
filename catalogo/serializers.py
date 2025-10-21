from rest_framework import serializers
from .models import Catalogo, Categoria, Cartelle
from easy_thumbnails.files import get_thumbnailer
from easy_thumbnails.exceptions import InvalidImageFormatError

# Serializer per il modello Catalogo genera automaticamente i campi basandosi sul modello
class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalogo

        # Campi da includere nella risposta JSON
        fields = [
            'id',
            'nome_it',
            'nome_en', 
            'nome_fr',
            'nome_es',
            'slug',
            'immagine_copertina',
            'is_active',
            'created_at',
            'updated_at',
        ] 

        #Campi visibili in lettura (GET) ma non in scrittura (POST, PUT, PATCH) poichè generati automaticamente
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

# Serializer per il modello Categoria genera automaticamente i campi basandosi sul modello
class CategoriaSerializer(serializers.ModelSerializer):
    # Include nome catalogo e path completo
    # Campi da aggiungere alla risposta
    # Prende il nome del catalogo associato e del parent per una visualizzazione più leggibile
    catalogo_nome = serializers.CharField(source='catalogo.nome_it', read_only=True)
    parent_nome = serializers.CharField(source='parent.nome_it', read_only=True, allow_null=True)
    
    class Meta:
        model = Categoria

        fields = [
            'id',
            'nome_it',
            'nome_en',
            'nome_fr', 
            'nome_es',
            'slug',
            'catalogo',
            'catalogo_nome',  # Nome leggibile catalogo
            'parent',
            'parent_nome',    # Nome leggibile parent
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'catalogo_nome', 'parent_nome']

# Serializer per il modello Cartelle genera automaticamente i campi basandosi sul modello
class CartelleSerializer(serializers.ModelSerializer):
    # Include URL file e info relazioni many-to-many
    cataloghi_list = serializers.SerializerMethodField()
    categorie_list = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    file_nome = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = Cartelle
        fields = [
            'id',
            'nome_cartella',
            'cataloghi_list',
            'categorie_list',
            'file_url',
            'file_nome',
            'thumbnail_url',  # Nuovo campo
            'tipo_file',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tipo_file', 'cataloghi_list', 'categorie_list', 'file_url', 'file_nome', 'thumbnail_url']
    
    # Metodo per ottenere lista cataloghi
    def get_cataloghi_list(self, obj):
        """Restituisce lista nomi cataloghi associati"""
        return [catalogo.nome_it for catalogo in obj.cataloghi.all()]
    
    # Metodo per ottenere lista categorie
    def get_categorie_list(self, obj):
        """Restituisce lista nomi categorie associate"""
        return [categoria.nome_it for categoria in obj.categorie.all()]
    
    # Metodi per campi calcolati
    def get_file_url(self, obj):
        """Restituisce URL del file protetto tramite autenticazione"""
        file = obj.get_file() # Usa il metodo del modello per ottenere il file
       
        if file:
            request = self.context.get('request')
            # Estrai il percorso relativo del file
            file_path = file.name
            
            # Costruisci URL protetto
            protected_url = f'/api/protected-media/{file_path}'
            
            if request:
                return request.build_absolute_uri(protected_url)
            return protected_url
        return None
    
    # Metodo per ottenere il nome del file
    def get_file_nome(self, obj):
        return obj.get_filename()
    
    # Metodo per ottenere l'URL della thumbnail
    def get_thumbnail_url(self, obj):
        """
        Genera thumbnail (300x300px) per file immagine.
        Supporta sia FilerFileField che FileField normale.
        Restituisce None per file non-immagine (PDF, video, etc.)
        """
        # Solo per immagini
        if obj.tipo_file != 'Immagine':
            return None
        
        try:
            request = self.context.get('request')
            
            # File da Filer (FilerFileField)
            if obj.file_da_filer:
                # Verifica che sia un'immagine Filer
                if hasattr(obj.file_da_filer, 'file') and obj.file_da_filer.file:
                    # Usa easy_thumbnails integrato in filer
                    thumbnailer = get_thumbnailer(obj.file_da_filer.file)
                    thumbnail = thumbnailer.get_thumbnail({
                        'size': (300, 300),
                        'crop': True,
                        'quality': 85,
                        'upscale': False  # Non ingrandire immagini piccole
                    })
                    
                    if thumbnail:
                        protected_url = f'/api/protected-media/{thumbnail.name}'
                        return request.build_absolute_uri(protected_url) if request else protected_url
            
            # File upload diretto (FileField)
            elif obj.file_upload_diretto:
                # Usa easy_thumbnails per FileField normale
                thumbnailer = get_thumbnailer(obj.file_upload_diretto)
                thumbnail = thumbnailer.get_thumbnail({
                    'size': (300, 300),
                    'crop': True,
                    'quality': 85,
                    'upscale': False
                })
                
                # Verifica se la thumbnail è stata generata
                if thumbnail:
                    protected_url = f'/api/protected-media/{thumbnail.name}'
                    return request.build_absolute_uri(protected_url) if request else protected_url
        
        except (InvalidImageFormatError, IOError, AttributeError, ValueError):
            # File corrotto, formato non valido, o non è un'immagine
            return None
        
        return None