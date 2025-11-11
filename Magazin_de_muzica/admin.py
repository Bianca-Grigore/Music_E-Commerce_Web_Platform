from django.contrib import admin
from .models import Categorie, Campanie_Promo, Produs, Produs_Artist, Artist

admin.site.site_header = "Magazin Muzical Admin"
admin.site.site_title = "Magazin Muzical"
admin.site.index_title = "Bine ați venit în Panoul de Administrare!"

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

