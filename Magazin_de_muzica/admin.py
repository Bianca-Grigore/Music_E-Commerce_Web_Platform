from django.contrib import admin
from .models import Categorie, Campanie_Promo, Produs, Produs_Artist, Artist
from .models import Profil
admin.site.site_header = "Magazin Muzical Admin"
admin.site.site_title = "Magazin Muzical"
admin.site.index_title = "Bine ați venit în Panoul de Administrare!"

from. models import Rating, Review, Comanda, DetaliiComanda
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Comanda)
admin.site.register(DetaliiComanda)

from .models import Vizualizare 
admin.site.register(Vizualizare)

from .models import Promotii
admin.site.register(Promotii)

class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefon', 'tara', 'judet', 'oras', 'strada', 'cod', 'email_confirmat')
    
    search_fields = ('user__username', 'telefon', 'tara', 'judet', 'oras', 'strada', 'cod')  
    fieldsets = (
        ('Informații Utilizator', {
            'fields': ('user',)
        }),
        ('Informații Contact', {
            'fields': ('telefon', 'tara', 'judet', 'oras', 'strada')
        }),
        ('Verificare Email', {
            'fields': ('cod', 'email_confirmat')
        }),
    )
admin.site.register(Profil, ProfilAdmin)

class ProdusAdmin(admin.ModelAdmin):
    ordering = ['pret']
    list_per_page = 5
    list_filter = ('categorie', 'denumire') 
    
    search_fields = ('denumire', 'categorie') 
    fieldsets = (
        ('Informații Generale', {
            'fields': ('denumire', 'categorie', 'pret', 'stoc', 'imagine')
        }),
        ('Campanii Promotionale', {
            'fields': ('campanii',),
            'classes': ('collapse',),  
        }),
    )

admin.site.register(Produs, ProdusAdmin)

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('nume', 'gen_muzical')
    
    search_fields = ('nume', 'gen_muzical')  
    fieldsets = (
        ('Informații Generale', {
            'fields': ('ani_activitate', 'tip_activitate')
        }),
    )

admin.site.register(Artist, ArtistAdmin)

class CategorieAdmin(admin.ModelAdmin):
    search_fields = ('nume_categorie', 'tip_categorie') 
    list_display=('nume_categorie', 'culoare') 
    
admin.site.register(Categorie, CategorieAdmin)

class Campanie_PromoAdmin(admin.ModelAdmin):
    search_fields = ('nume_campanie', 'data_inceput')  
    
admin.site.register(Campanie_Promo, Campanie_PromoAdmin)

class Produs_ArtistAdmin(admin.ModelAdmin):
    search_fields = ('descriere', 'colaborare_speciala')  
    
admin.site.register(Produs_Artist, Produs_ArtistAdmin)

