from .models import Categorie  

def categorii_context(request):
    return {
        'categorie': Categorie.objects.all()
    }