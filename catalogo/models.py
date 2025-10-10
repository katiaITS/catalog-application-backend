from django.db import models
from django.contrib.auth.models import User #serve per sapere chi ha caricato cosa

class Catalogo(models.Model):
    nome=models.JSONField(
        verbose_name='Nome Catalogo',
        help_text='Formato: {"it": "...", "en": "...", "fr": "...", "es": "..."}'
    )

    #per URL tipo /catalogo/componenti-a1-a114 per ora lo generiamo manualmente nell'admin
    slug=models.SlugField(
        unique=True,
        max_length=100,
        verbose_name='Slug URL'
    )

    #immagine rappresentativa del catalogo
    immagine_copertina= models.ImageField( #campo per caricare immagine
        upload_to='cataloghi/copertine/', #dove salva i file caricati
        null=True,
        blank=True,
        verbose_name='Immagine  Copertina'
    )

    #Campo per decidere l'ordine di visualizzazione - l'ordine lo decidiamo noi in base al numero - valutare autoincremente con riordinamento a posteriori)
    order = models.IntegerField(
        default=0,
        verbose_name='Ordine',
        help_text='Numero per ordinamento (dal più basso al più alto)'
    )

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

    #Per i nomi nell'admin e per l'ordinamento
    class Meta:
        verbose_name = 'Catalogo'
        verbose_name_plural = 'Cataloghi'
        ordering = ['order', 'nome']

    #Restituisce il nome italiano del catalogo
    def __str__(self):
        return self.nome.get('it', 'Senza nome')

    #Metodo che in base alla lingua restituisce il nome corretto, se non specificato di default da italiano
    def get_nome(self, lingua='it'):
        return self.nome.get(lingua, self.nome.get('it', 'N/D')) #cerca la lingua richiesta se non esiste cerca it sennò N/D
