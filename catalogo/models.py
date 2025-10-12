from django.db import models
from django.contrib.auth.models import User #serve per sapere chi ha caricato cosa
from django.utils.text import slugify
import re #serve per manipolare i pattern di testo -> nel nostro caso per la funzionare che padda i numeri
from pathlib import Path #manipola nomi file e percorsi (estraiamo il nome file senza estensione)
import os # gestione file sul SO lousiamo per rinominare i file con timestamp
from django.utils import timezone #per generare timestamp sui nomi file
from filer.fields.file import FilerFileField 

#metodo che genera il percordo dove salvare il file caricato
#Struttura: Struttura: cataloghi/{slug_catalogo}/{filename_timestamp}
#Esempio: cataloghi/componenti-a1-a114/A31 Perle_20251012_143520.jpg

def cartella_upload_path(instance, filename):
    # Input: filename = "A31 Perle.jpg"
    
    # 1. Estrai nome senza estensione
    nome_cartella = Path(filename).stem  # "A31 Perle"
    
    # 2. Timestamp corrente
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')  # "20251012_143520"
    
    # 3. Estensione
    ext = os.path.splitext(filename)[1]  # ".jpg"
    
    # 4. Rimuovi caratteri speciali
    nome_safe = re.sub(r'[^\w\s-]', '', nome_cartella)  # "A31 Perle"
    
    # 5. Nuovo nome con timestamp
    new_filename = f"{nome_safe}_{timestamp}{ext}"  # "A31 Perle_20251012_143520.jpg"
    
    # 6. Percorso finale
    return os.path.join('file_catalogo', new_filename)  # "file_catalogo/A31 Perle_20251012_143520.jpg"

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
    
# Modello per gestire file del catalogo
# Supporta upload diretto o selezione da Filer
class CartelleCatalogo(models.Model):

    nome_cartella = models.CharField(
        max_length=250,
        verbose_name='Nome Cartella',
        help_text='Es: A31 Perle in plastica, FS46 Materiali'
    )

    #nome cartella per ordinamento, non modificabile
    nome_cartella_sort = models.CharField(
        max_length=250,
        editable=False,
        blank=True,
        verbose_name='Nome Cartella Sort'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='cartelle',
        verbose_name='Categoria'
    )

    # Upload Diretto
    file_upload_diretto = models.FileField(
        upload_to=cartella_upload_path, #usa la funziona create per salvare il file con timestamp
        null=True,
        blank=True,
        verbose_name='Upload Diretto',
        help_text='Per aggiornamenti veloci: carica file direttamente qui'
    )
    
    # Selezione file per Cartella da Filer
    file_da_filer = FilerFileField(
        null=True,
        blank=True,
        related_name="cartelle_catalogo",
        on_delete=models.CASCADE,
        verbose_name='Seleziona da Media Manager',
        help_text='Per upload massivi: prima carica su Filer, poi seleziona qui'
    )

    #campo che rivela il tipo di file nel momento in cui salvi
    tipo_file = models.CharField(
        max_length=10,
        editable=False,
        blank=True,
        verbose_name='Tipo File'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Attivo'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data Creazione'
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultima Modifica'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cartelle_create',
        verbose_name='Creato da'
    )
    
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cartelle_modificate',
        verbose_name='Modificato da'
    )

    class Meta:
        verbose_name = 'Cartella Catalogo'
        verbose_name_plural = 'Cartelle Catalogo'
        ordering = ['categoria__catalogo', 'categoria', 'nome_cartella_sort']

    # stampa il percorso completo della cartella   
    def __str__(self):
        return f"{self.categoria.catalogo.nome_it} > {self.categoria.nome_it} > {self.nome_cartella}"   
    
    #Metodo che ritorna il file effettivo, che sia upload diretto o da filer
    def get_file(self):
        return self.file_upload_diretto or (self.file_da_filer.file if self.file_da_filer else None)
    
    #Metodo che ritorna il nome del file effettivo
    def get_filename(self):
        file = self.get_file()
        return os.path.basename(file.name) if file else 'Nessun file'
    
    #Metodo che ritorna l'estensione del file effettivo
    def get_file_extension(self):
        file = self.get_file()
        return os.path.splitext(file.name)[1].lower() if file else ''
    
    #Metodo che ritorna il tipo di file in base all'estensione
    def get_file_type(self):
        ext = self.get_file_extension()
        if ext in ['.pdf']:
            return 'PDF'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            return 'Immagine'
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
            return 'Video'
        elif ext in ['.doc', '.docx', '.odt']:
            return 'Documento Word'
        elif ext in ['.xls', '.xlsx', '.ods']:
            return 'Foglio Excel'
        elif ext in ['.ppt', '.pptx', '.odp']:
            return 'Presentazione PowerPoint'
        else:
            return 'Altro'
        
    #Metodo che ordina le cartelle in base al nome cartella sort e all'import re per paddare numeri
    def save(self, *args, **kwargs):
        # Genera nome_cartella_sort paddando numeri per ordinamento corretto
        def pad_numbers(text):
            return re.sub(r'(\d+)', lambda m: m.group(1).zfill(10), text)
        
        self.nome_cartella_sort = pad_numbers(self.nome_cartella.lower())
        
        # Determina tipo_file
        self.tipo_file = self.get_file_type()
        
        super().save(*args, **kwargs)