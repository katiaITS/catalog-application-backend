from rest_framework import serializers
from .models import Catalogo, Categoria, Cartelle

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

# Serializer per il modello CartelleCatalogo genera automaticamente i campi basandosi sul modello
class CartelleCatalogoSerializer(serializers.ModelSerializer):
    # Include URL file e info categoria

    categoria_nome = serializers.CharField(source='categoria.nome_it', read_only=True)
    catalogo_nome = serializers.CharField(source='categoria.catalogo.nome_it', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_nome = serializers.SerializerMethodField()

    class Meta:
        model = Cartelle
        fields = [
            'id',
            'nome_cartella',
            'categoria',
            'categoria_nome',
            'catalogo_nome',
            'file_url',
            'file_nome',
            'tipo_file',
            'is_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'tipo_file', 'categoria_nome', 'catalogo_nome', 'file_url', 'file_nome']
    
    # Metodi per campi calcolati
    def get_file_url(self, obj):
        """Restituisce URL del file attivo"""
        file = obj.get_file() # Usa il metodo del modello per ottenere il file
       
        # Se c'è request nel contestet, costruisce URL assoluto altrimenti ritorna URL relativo
        if file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(file.url)
            return file.url
        return None
    
    # Metodo per ottenere il nome del file
    def get_file_nome(self, obj):
        return obj.get_filename()