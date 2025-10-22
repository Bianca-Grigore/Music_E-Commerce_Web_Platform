from django.contrib import admin
from .models import Categorie, Campanie_Promo, Produs, Produs_Artist, Artist

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Campanie_Promo)
admin.site.register(Produs)
admin.site.register(Produs_Artist)
admin.site.register(Artist)