from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from .models import Catalogo, Categoria, Cartelle, CatalogoCartella, CategoriaCartella

# Filtro custom per Cataloghi
class CatalogoFilter(SimpleListFilter):
    title = 'catalogo'
    parameter_name = 'catalogo'
    
    def lookups(self, request, model_admin):
        cataloghi = Catalogo.objects.all().order_by('nome_it')
        return [(c.id, c.nome_it) for c in cataloghi]
    
    def queryset(self, request, queryset):
        if self.value():
            from django.db.models import Q
            # Filtra cartelle che sono:
            # 1. Associate direttamente al catalogo (root)
            # 2. Associate a categorie di quel catalogo (incluse sottocategorie)
            return queryset.filter(
                Q(cataloghi__id=self.value()) |  # Root del catalogo
                Q(categorie__catalogo_id=self.value())  # Categorie del catalogo
            ).distinct()
        return queryset

# Filtro custom per Categorie (dipendente dal Catalogo selezionato)
class CategoriaFilter(SimpleListFilter):
    title = 'categoria'
    parameter_name = 'categoria'
    
    def lookups(self, request, model_admin):
        # Prende il catalogo selezionato dal parametro URL
        catalogo_id = request.GET.get('catalogo')
        
        if catalogo_id:
            # Se c'è un catalogo selezionato, mostra solo le sue categorie
            categorie = Categoria.objects.filter(catalogo_id=catalogo_id).order_by('nome_it')
        else:
            # Altrimenti mostra tutte le categorie
            categorie = Categoria.objects.all().order_by('nome_it')
        
        return [(c.id, c.nome_it) for c in categorie]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categorie__id=self.value()).distinct()
        return queryset

#creamo un inline admin per mostrare le cartelle associate a catalogo
class CatalogoCartellaInline(admin.TabularInline):
    model = CatalogoCartella
    extra = 1  # Numero di form vuoti aggiuntivi
    fields = ['cartella', 'ordine']  # Campi da mostrare
    autocomplete_fields = ['cartella']  # Usa l'autocomplete per il campo cartella

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
    inlines = [CatalogoCartellaInline]  # Aggiunge l'inline per le cartelle -> dice a Django mostra questi inline nel form del catalogo

    #sovrascrivo save per settare created_by e updated_by con l'User correntemente loggato
    def save_model(self, request, obj, form, change):
        if not change:  # Solo se è nuova creazione
            obj.created_by = request.user
        
        # Sempre (sia creazione che modifica)
        obj.updated_by = request.user
        
        super().save_model(request, obj, form, change)  

# inline admin per mostrare le cartelle associate a categoria
class CategoriaCartellaInline(admin.TabularInline):
    model = CategoriaCartella
    extra = 1  # Numero di form vuoti aggiuntivi
    fields = ['cartella', 'ordine']  # Campi da mostrare
    autocomplete_fields = ['cartella']  # Usa l'autocomplete per il campo cartella

# Inline inverso per mostrare in quali cataloghi appare la cartella
class CatalogoCartellaInlineInverso(admin.TabularInline):
    model = CatalogoCartella
    fk_name = 'cartella'  # Specifica il campo ForeignKey che punta a Cartelle
    extra = 1
    fields = ('catalogo', 'ordine')
    verbose_name = 'Catalogo Root'
    verbose_name_plural = 'Cataloghi Root'

# Inline inverso per mostrare in quali categorie appare la cartella
class CategoriaCartellaInlineInverso(admin.TabularInline):
    model = CategoriaCartella
    fk_name = 'cartella'  # Specifica il campo ForeignKey che punta a Cartelle
    extra = 1
    fields = ('categoria', 'ordine')
    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorie'

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

    inlines = [CategoriaCartellaInline]  # Aggiunge l'inline per le cartelle -> dice a Django mostra questi inline nel form della categoria

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


from django import forms
from filer.models import File

# Form Custom per Cartelle (semplice, senza multipli)
class CartelleForm(forms.ModelForm):
    class Meta:
        model = Cartelle
        fields = '__all__'


@admin.register(Cartelle)
class CartelleAdmin(admin.ModelAdmin):
    form = CartelleForm
    
    list_display = ('nome_cartella', 'tipo_file', 'posizione', 'is_active', 'created_at', 'updated_by')
    list_display_links = ('nome_cartella',)
    list_filter = ('tipo_file', 'is_active', CatalogoFilter, CategoriaFilter)
    search_fields = ('nome_cartella',)
    
    # Fieldsets per organizzare il form
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('nome_cartella', 'is_active')
        }),
        ('Upload File (scegli UN metodo)', {
            'fields': ('file_upload_diretto', 'file_da_filer'),
            'description': 'Carica un file diretto OPPURE seleziona da Filer. Non entrambi!'
        }),
    )
    
    inlines = [CatalogoCartellaInlineInverso, CategoriaCartellaInlineInverso]
    
    # URL Custom per import multiplo
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('import-multipli/', 
                 self.admin_site.admin_view(self.import_multipli_view),
                 name='catalogo_cartelle_import_multipli'),
        ]
        return custom_urls + urls
    
    def changelist_view(self, request, extra_context=None):
        """Override per aggiungere pulsante custom nella toolbar"""
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        return super().changelist_view(request, extra_context)
    
    def import_multipli_view(self, request):
        """
        View custom per import multiplo da Filer
        """
        from django.shortcuts import render, redirect
        from django.contrib import messages
        from filer.models import File
        import json
        
        if request.method == 'POST':
            # L'utente ha confermato l'import
            file_ids = request.POST.getlist('file_ids')
            catalogo_id = request.POST.get('catalogo_id')
            categoria_id = request.POST.get('categoria_id')
            
            if not catalogo_id:
                messages.error(request, '❌ Devi selezionare un Catalogo!')
                return redirect('admin:catalogo_cartelle_changelist')
            
            if file_ids:
                count = 0
                for file_id in file_ids:
                    try:
                        file_obj = File.objects.get(pk=file_id)
                        from pathlib import Path
                        nome = Path(file_obj.name).stem
                        
                        # Crea la cartella
                        cartella = Cartelle.objects.create(
                            nome_cartella=nome,
                            file_da_filer=file_obj,
                            is_active=True,
                            created_by=request.user,
                            updated_by=request.user
                        )
                        
                        # Collega a Catalogo
                        CatalogoCartella.objects.create(
                            catalogo_id=catalogo_id,
                            cartella=cartella,
                            ordine=count
                        )
                        
                        # Collega a Categoria se selezionata
                        if categoria_id:
                            CategoriaCartella.objects.create(
                                categoria_id=categoria_id,
                                cartella=cartella,
                                ordine=count
                            )
                        
                        count += 1
                    except Exception as e:
                        messages.error(request, f'❌ Errore con file {file_id}: {str(e)}')
                
                messages.success(request, f'✅ {count} file importati con successo!')
            else:
                messages.warning(request, '⚠️ Nessun file selezionato!')
            
            return redirect('admin:catalogo_cartelle_changelist')
        
        # Mostra la pagina intermedia con la lista file
        files = File.objects.select_related('folder').all().order_by('-uploaded_at')
        cataloghi = Catalogo.objects.filter(is_active=True)
        
        # Prepara categorie raggruppate per catalogo
        categorie_by_catalogo = {}
        for catalogo in cataloghi:
            cats = Categoria.objects.filter(catalogo=catalogo, is_active=True)
            categorie_by_catalogo[str(catalogo.id)] = [
                {'id': cat.id, 'nome': cat.nome_it} for cat in cats
            ]
        
        context = {
            **self.admin_site.each_context(request),  # Contesto admin standard
            'title': 'Importa Multipli File da Filer',
            'files': files,
            'cataloghi': cataloghi,
            'categorie_json': json.dumps(categorie_by_catalogo),
            'opts': self.model._meta,
            'action_checkbox_name': admin.helpers.ACTION_CHECKBOX_NAME,
        }
        
        # Django cerca il template: templates/admin/catalogo/import_multipli_action.html
        return render(request, 'admin/catalogo/import_multipli_action.html', context)
    
    # Colonna unica che mostra dove si trova la cartella
    def posizione(self, obj):
        posizioni = []
        
        # Controllo categorie
        categorie = obj.categorie.all()
        if categorie:
            for cat in categorie:
                posizioni.append(f"{cat.nome_it}")
        
        # Controllo cataloghi root
        cataloghi = obj.cataloghi.all()
        if cataloghi:
            for cat in cataloghi:
                posizioni.append(f"{cat.nome_it}")
        
        return " | ".join(posizioni) if posizioni else "Non assegnata"
    
    posizione.short_description = 'Posizione'
    
    def save_model(self, request, obj, form, change):
        # Imposta chi ha creato/modificato
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
            obj.updated_by = request.user
        
        # Salva normalmente
        super().save_model(request, obj, form, change)
    
    # Mostra in quali cataloghi appare il file
    def cataloghi_list(self, obj):
        cataloghi = obj.cataloghi.all()
        if cataloghi:
            return ", ".join([c.nome_it for c in cataloghi])
        return "-"
    cataloghi_list.short_description = 'Cataloghi'

    # Mostra in quali categorie appare il file
    def categorie_list(self, obj):
        categorie = obj.categorie.all()
        if categorie:
            return ", ".join([c.nome_it for c in categorie])
        return "-"
    categorie_list.short_description = 'Categorie'