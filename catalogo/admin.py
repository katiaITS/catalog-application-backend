from django.contrib import admin
from .models import Catalogo, Categoria, Cartelle

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


from django import forms
from filer.models import File

# Form Custom con selezione multipla
class CartelleForm(forms.ModelForm):
    # Campo per selezione multipla file da Filer
    files_da_filer = forms.ModelMultipleChoiceField(
        queryset=File.objects.all(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple('Files', False),
        label='Seleziona File da Filer (Multipli)',
        help_text='Seleziona più file per creare multiple cartelle contemporaneamente'
    )
    
    class Meta:
        model = Cartelle
        fields = '__all__'

@admin.register(Cartelle)
class CartelleAdmin(admin.ModelAdmin):
    form = CartelleForm  # ← USA FORM CUSTOM
    
    list_display = ('nome_cartella', 'tipo_file', 'is_active', 'created_at', 'updated_by')
    list_display_links = ('nome_cartella',)
    list_filter = ('tipo_file', 'is_active',)
    search_fields = ('nome_cartella',)
    
    def save_model(self, request, obj, form, change):
        # Se è modifica
        if change:
            obj.updated_by = request.user
            super().save_model(request, obj, form, change)
        else:
            # È creazione nuova
            files_multipli = form.cleaned_data.get('files_da_filer')
            
            if files_multipli and files_multipli.count() > 0:
                # CREAZIONE MULTIPLA
                categoria = form.cleaned_data['categoria']
                is_active = form.cleaned_data.get('is_active', True)
                count = 0
                
                for file_obj in files_multipli:
                    from pathlib import Path
                    nome = Path(file_obj.name).stem
                    
                    Cartelle.objects.create(
                        nome_cartella=nome,
                        categoria=categoria,
                        file_da_filer=file_obj,
                        is_active=is_active,
                        created_by=request.user,
                        updated_by=request.user
                    )
                    count += 1
                
                self.message_user(
                    request,
                    f'Create {count} CartelleCatalogo con successo!'
                )
            else:
                # CREAZIONE SINGOLA
                obj.created_by = request.user
                obj.updated_by = request.user
                super().save_model(request, obj, form, change)
    
    def response_add(self, request, obj, post_url_continue=None):
        # Redirect alla lista dopo creazione multipla
        if 'files_da_filer' in request.POST:
            from django.http import HttpResponseRedirect
            from django.urls import reverse
            return HttpResponseRedirect(reverse('admin:catalogo_cartellecatalogo_changelist'))
        return super().response_add(request, obj, post_url_continue)