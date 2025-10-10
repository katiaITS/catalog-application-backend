from django.db import models
from django.contrib.auth.models import User #serve per sapere chi ha caricato cosa
from django.utils.text import slugify

class Catalogo(models.Model):
    nome=models.JSONField(
        verbose_name='Nome Catalogo',
        help_text='Formato: {"it": "...", "en": "...", "fr": "...", "es": "..."}'
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

    #Campi per sapere quando è stato creato/modificato
    created_at = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Data Creazione'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Ultima Modifica'
    )

    #Per i nomi nell'admin e per l'ordinamento alfabetico
    class Meta:
        verbose_name = 'Catalogo'
        verbose_name_plural = 'Cataloghi'
        ordering = ['slug']

    #Restituisce il nome italiano del catalogo
    def __str__(self):
        return self.nome.get('it', 'Senza nome')

    #Metodo che in base alla lingua restituisce il nome corretto, se non specificato di default da italiano
    def get_nome(self, lingua='it'):
        return self.nome.get(lingua, self.nome.get('it', 'N/D')) #cerca la lingua richiesta se non esiste cerca it sennò N/D

    #Ovverride del metodo save per creare in automatico lo slug in italiano
    def save(self, *args, **kwargs):
        if not self.slug: #se slug è vuoto
            #prende il nome in italiano e genera slug
            nome_italiano=self.nome.get('it','')
            self.slug= slugify(nome_italiano)

            #Gestione duplicati - inserisce numero
            original_slug = self.slug
            counter = 1
            while Catalogo.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        super().save(*args, **kwargs)