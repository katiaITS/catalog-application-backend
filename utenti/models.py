from django.db import models
from django.contrib.auth.models import User #Importa il modello User di Django
#Import che ci permette di creare automaticamente un ProfileUtente quando viene creato un Utente
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProfiloUtente(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE) #creo una relazione uno a uno tra ProfiloUtente e User di Django
    nome_azienda= models.CharField(
        max_length=200,
        null=True, #nel database può essere valore vuoto
        blank=True, #nel form può essere valore vuoto     
    )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #Classe che serve per i nomi del modello
    class Meta:
        verbose_name = 'Profilo Utente'
        verbose_name_plural = 'Profili Utente'

    #Metodo che restituisce nome e cognome in formato stringa(senza di esso sarebbe resistuito solo l'oogetto)
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
# Ascolta e quando viene salvato un User se è nuovo crea un nuovo ProfiloUtente
@receiver(post_save, sender=User) #sender dice a Django quale modello ascoltare
def crea_profilo_utente(sender, instance, created, **kwargs): #**kwargs è un dizionario python che indica tutti gli altri argomenti che non ho specificato
    if created:
        try:
            ProfiloUtente.objects.create(user=instance)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Errore creazione profilo per {instance.email}: {e}")

@receiver(post_save, sender=User)
def salva_profilo_utente(sender, instance, **kwargs):
    try:
        instance.profiloutente.save()
    except Exception as e:
        print(f"Errore durante il salvataggio del profilo: {e}")


# Create your models here.
