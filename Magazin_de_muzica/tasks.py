import logging
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.conf import settings
import random
from .models import Produs 

logger = logging.getLogger('django')

def sterge_useri_neconfirmati():

    timp_limita = timezone.now() - timedelta(minutes=settings.TASK_K_MINUTES)

    useri_de_sters = User.objects.filter(
        profil__email_confirmat=False, 
        date_joined__lt=timp_limita
    )

    numar = useri_de_sters.count()
    if numar > 0:
        for user in useri_de_sters:

            logger.warning(f"TASK AUTOMAT: S-a sters utilizatorul neconfirmat: {user.username} (ID: {user.id})")
            user.delete()
        print(f"Au fost șterși {numar} utilizatori neconfirmați.")
    else:
        print("Niciun utilizator neconfirmat de sters.")

def trimite_newsletter():


    timp_limita = timezone.now() - timedelta(minutes=settings.TASK_X_MINUTES_OLD)
    destinatari = User.objects.filter(
        date_joined__lt=timp_limita, 
        profil__email_confirmat=True,
        email__isnull=False
    ).exclude(email='')

    if not destinatari.exists():
        print("Nu există destinatari pentru newsletter.")
        return

    produse = list(Produs.objects.all())
    if len(produse) >= 3:
        produse_alese = random.sample(produse, 3)
    else:
        produse_alese = produse
    
    nume_produse = ", ".join([p.denumire for p in produse_alese])
    
    subiect = f"Noutățile zilei de {timezone.now().strftime('%A')}!"
    mesaj = f"""
    Salut!
    
    Nu rata ofertele noastre speciale de astăzi. 
    Uite ce ți-am pregătit: {nume_produse}.
    
    Intră pe site să le vezi!
    """


    mesaje_email = []
    for user in destinatari:
        mesaje_email.append((subiect, mesaj, settings.EMAIL_HOST_USER, [user.email]))
    
    try:
        send_mass_mail(tuple(mesaje_email), fail_silently=False)
        logger.info(f"TASK AUTOMAT: Newsletter trimis la {len(destinatari)} utilizatori.")
    except Exception as e:
        logger.error(f"TASK AUTOMAT ERROR: Nu s-a putut trimite newsletter-ul: {e}")


def verificare_stocuri_scazute():

    produse_critice = Produs.objects.filter(stoc__lt=5)
    cnt = produse_critice.count()
    
    if cnt > 0:
        nume_critice = ", ".join([p.denumire for p in produse_critice[:3]])

        logger.warning(f"ALERTA STOC: {cnt} produse au stoc limitat! (Ex: {nume_critice}...)")
    else:
        print("Stocul este ok.")


def raport_saptamanal_admin():
    nr_useri = User.objects.count()
    nr_produse = Produs.objects.count()
    
    subiect = "Raport Săptămânal"
    mesaj = f"""
    Salut Admin,
    
    Situația la zi:
    - Total Utilizatori: {nr_useri}
    - Total Produse: {nr_produse}
    """

    from django.core.mail import mail_admins
    try:
        mail_admins(subiect, mesaj, fail_silently=True)
        logger.info("TASK AUTOMAT: Raport saptamanal trimis administratorilor.")

    except Exception as e:
        logger.error(f"Eroare trimitere raport admin: {e}")