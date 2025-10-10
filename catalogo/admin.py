from django.contrib import admin
from .models import Catalogo, Categoria

#creaimo una classe admin personalizzata che configura l'admin per il modello catalogo
#Registra Catalogo nell'admin
@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    #Colonne mostrate nella lista
    list_display= ('nome_it', 'slug', 'is_active', 'created_at', 'created_by', 'updated_at', 'updated_by')
    list_display_links = ('nome_it',) #definisce cosa è cliccabile
    list_filter = ('is_active', 'updated_by',)
    #barra di ricerca
    search_fields = ('nome_it',)
    # Raggruppamento visivo con fieldsets
    fieldsets = (
        ('Nome Multilingua', {
            'fields': ('nome_it', 'nome_en', 'nome_fr', 'nome_es'),
            'description': 'Il nome italiano è obbligatorio. Le altre lingue sono opzionali.'
        }),
        ('Impostazioni', {
            'fields': ('slug', 'immagine_copertina', 'is_active')
        }),
    )

    #sovrascrivo save per settare created_by e updated_by con l'User correntemente loggato
    def save_model(self, request, obj, form, change):
        if not change:  # Solo se è nuova creazione
            obj.created_by = request.user
        
        # Sempre (sia creazione che modifica)
        obj.updated_by = request.user
        
        super().save_model(request, obj, form, change)  

#Registra Categoria nell'admin
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):

    #Colonne mostrate nella lista
    list_display= ('nome_it', 'slug', 'is_active', 'catalogo_nome','parent_nome', 'created_at', 'created_by', 'updated_at', 'updated_by')
    list_display_links = ('nome_it',) #definisce cosa è cliccabile
    list_filter = ('is_active', 'updated_by', 'catalogo')
    
    #barra di ricerca
    search_fields = ('nome_it','catalogo__nome_it')
    
    # Raggruppamento visivo con fieldsets
    fieldsets = (
        ('Nome Multilingua', {
            'fields': ('nome_it', 'nome_en', 'nome_fr', 'nome_es'),
            'description': 'Il nome italiano è obbligatorio. Le altre lingue sono opzionali.'
        }),
        ('Impostazioni', {
            'fields': ('slug', 'is_active', 'catalogo','parent')
        }),
    )

    #sovrascrivo save per settare created_by e updated_by con l'User correntemente loggato
    def save_model(self, request, obj, form, change):
        if not change:  # Solo se è nuova creazione
            obj.created_by = request.user
        
        # Sempre (sia creazione che modifica)
        obj.updated_by = request.user
        
        super().save_model(request, obj, form, change)  

    # Metodo custom per mostrare nome catalogo nella lista
    def catalogo_nome(self, obj):
        return obj.catalogo.nome_it
    catalogo_nome.short_description = 'Catalogo'
    catalogo_nome.admin_order_field = 'catalogo'  # Permette ordinamento cliccando colonna

    # Metodo custom per mostrare nome parent nella lista
    def parent_nome(self, obj):
        return obj.parent.nome_it if obj.parent else '-'
    parent_nome.short_description = 'Categoria Padre'      