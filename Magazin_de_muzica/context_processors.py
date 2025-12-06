# Magazin_de_muzica/context_processors.py
from .models import Categorie  # Asigură-te că modelul tău se numește exact 'Categorie'

def categorii_context(request):
    """
    Această funcție returnează un dicționar cu toate categoriile,
    care va fi disponibil în TOATE template-urile.
    """
    return {
        'categorie': Categorie.objects.all()
    }