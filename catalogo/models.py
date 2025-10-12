from django.db import models
from django.contrib.auth.models import User #serve per sapere chi ha caricato cosa
from django.utils.text import slugify
import re #serve per manipolare i pattern di testo -> nel nostro caso per la funzionare che padda i numeri
from pathlib import Path #manipola nomi file e percorsi (estraiamo il nome file senza estensione)
import os # gestione file sul SO lousiamo per rinominare i file con timestamp
from django.utils import timezone #per generare timestamp sui nomi file

#metodo che genera il percordo dove salvare il file caricato
#Struttura: Struttura: cataloghi/{slug_catalogo}/{filename_timestamp}
#Esempio: cataloghi/componenti-a1-a114/A31 Perle_20251012_143520.jpg

def cartella_upload_path(instance, filename): #instance oggetto che stai salvando, filename il nome del file originale
    # Estrai nome cartella dal filename (senza estensione)
    nome_cartella= Path(filename).stem #stem prende solo il nome del filename senza estensione
    
    #Creo il timestamp
    timestamp=timezone.now().strftime('%Y%m%d_%H%M%S') 
    
    #Separa il nome dall'estensione e prende quest'ultima
    ext = os.path.splitext(filename)[1] 
    
    #Rimuove caratteri problematici per il filesystem
    nome_safe = re.sub(r'[^\w\s-]', '', nome_cartella) 
    
    #Combina nome, timestamp e estensione
    new_filename = f"{nome_safe}_{timestamp}{ext}" 

    # Risali al catalogo tramite categoria
    if instance.categoria and instance.categoria.catalogo:
        catalogo_slug = instance.categoria.catalogo.slug
    else:
        catalogo_slug = 'senza-catalogo'
    
    # Ritorna percorso: cataloghi/{catalogo_slug}/{filename}
    return os.path.join('cataloghi', catalogo_slug, new_filename)


class Catalogo(models.Model):
    #Campi per il nome in 4 lingue diverse
    nome_it = models.CharField(
        max_length=200,
        verbose_name='Nome (Italiano)'
    )
    nome_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Inglese)'
    )
    nome_fr = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Francese)'
    )
    nome_es = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Spagnolo)'
    )

    #per URL tipo /catalogo/componenti-a1-a114 per ora lo generiamo manualmente nell'admin
    slug=models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
        verbose_name='Slug URL',
        help_text='Lascia vuoto per generazione automatica dal nome italiano'
    )

    #immagine rappresentativa del catalogo
    immagine_copertina= models.ImageField( #campo per caricare immagine
        upload_to='cataloghi/copertine/', #dove salva i file caricati
        null=True,
        blank=True,
        verbose_name='Immagine  Copertina'
    )

    #Campo per decidere l'ordine di visualizzazione - l'ordine lo decidiamo noi in base al numero - valutare autoincremente con riordinamento a posteriori)
    #order = models.IntegerField(
       # default=0,
     #   verbose_name='Ordine',
     #   help_text='Numero per ordinamento (dal più basso al più alto)'
    #)

    #nascondere catalogo quando non più attivo (per storico o eventuale riattivazione)
    is_active = models.BooleanField(
    default=True,
    verbose_name='Attivo'
    )

    #Campi per sapere quando è stato creato/modificato e da chi
    created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Data Creazione'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cataloghi_creati',
        verbose_name='Creato da'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultima Modifica'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cataloghi_modificati',
        verbose_name='Modificato da'
    )

    #Per i nomi nell'admin e per l'ordinamento alfabetico
    class Meta:
        verbose_name = 'Catalogo'
        verbose_name_plural = 'Cataloghi'
        ordering = ['slug']

    #Restituisce il nome italiano del catalogo
    def __str__(self):
        return self.nome_it

    #Metodo che in base alla lingua restituisce il nome corretto, se non specificato di default da italiano
    def get_nome(self, lingua='it'):
        nomi = {
            'it': self.nome_it,
            'en': self.nome_en or self.nome_it,  # Fallback su italiano
            'fr': self.nome_fr or self.nome_it,
            'es': self.nome_es or self.nome_it,
        }
        return nomi.get(lingua, self.nome_it)
    
    #Ovverride del metodo save per creare in automatico lo slug in italiano
    def save(self, *args, **kwargs):
        if not self.slug: #se slug è vuoto
            #prende il nome in italiano e genera slug
            self.slug = slugify(self.nome_it)

            #Gestione duplicati - inserisce numero
            original_slug = self.slug
            counter = 1
            while Catalogo.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

class Categoria(models.Model):
    nome_it = models.CharField(
    max_length=200,
    verbose_name='Nome (Italiano)'
    )
    nome_en = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Inglese)'
    )
    nome_fr = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Francese)'
    )
    nome_es = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nome (Spagnolo)'
    )

    #slug generato automaticamente da nome italiano
    slug = models.SlugField(
    unique=True,
    max_length=100,
    blank=True,
    verbose_name='Slug URL'
    )

    is_active = models.BooleanField(
    default=True,
    verbose_name='Attivo'
    )

    #realzione con modello Catalogo
    catalogo = models.ForeignKey(
    Catalogo,
    on_delete=models.PROTECT,
    related_name='categorie',
    verbose_name='Catalogo'
    )

    #
    parent = models.ForeignKey(
    'self',
    on_delete=models.PROTECT,
    null=True,
    blank=True,
    related_name='sottocategorie',
    verbose_name='Categoria Padre'
    )

    created_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='categorie_create',
    verbose_name='Creato da'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data Creazione'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categorie_modificate',
        verbose_name='Modificato da'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultima Modifica'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorie'
        ordering = ['catalogo', 'nome_it']

    #Mostra il percorso completo della categoria
    def __str__(self):
        if self.parent:
            return f"{self.catalogo.nome_it} > {self.parent.nome_it} > {self.nome_it}"
        return f"{self.catalogo.nome_it} > {self.nome_it}"
    
    def get_nome(self, lingua='it'):
        nomi = {
            'it': self.nome_it,
            'en': self.nome_en or self.nome_it,  # Fallback su italiano
            'fr': self.nome_fr or self.nome_it,
            'es': self.nome_es or self.nome_it,
        }
        return nomi.get(lingua, self.nome_it)
    
    #Genera slug automaticamente da nome italiano che mostri la gerarchia
    def save(self, *args, **kwargs):
        if not self.slug: # Solo se slug è vuoto
            # Genera slug base del nome italiano
            base_slug = slugify(self.nome_it)
            
            # Se ha parent, lo mette come prefisso dello slug
            if self.parent:
                self.slug = f"{self.parent.slug}-{base_slug}"
            else:
                self.slug = base_slug
            
            # Gestisce duplicati
            original_slug = self.slug
            counter = 1
            while Categoria.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)

    # Ritorna path completo della categoria -Es: "Swarovski > Catena strass > Catena oro"
    def get_full_path(self, lingua='it'):

        # Lista per raccogliere i nomi
        path_parts = [self.get_nome(lingua)]

        # Risale la gerarchia parent
        current = self.parent
        while current:
            path_parts.insert(0, current.get_nome(lingua))
            current = current.parent
        
        # Aggiungi catalogo all'inizio
        path_parts.insert(0, self.catalogo.get_nome(lingua))
        
        # Unisci con " > "
        return " > ".join(path_parts)
    

#class CartelleCatalogo(models.Model):
    