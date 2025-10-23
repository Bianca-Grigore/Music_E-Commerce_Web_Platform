from django.contrib import admin
from .models import Categorie, Campanie_Promo, Produs, Produs_Artist, Artist

# Register your models here.
admin.site.register(Categorie)
admin.site.register(Campanie_Promo)
#admin.site.register(Produs)
admin.site.register(Produs_Artist)
#admin.site.register(Artist)

class ProdusAdmin(admin.ModelAdmin):
    #list_display = ('titlu', 'autor', 'data_publicarii') 
    list_filter = ('categorie', 'denumire')
    #search_fields = ('titlu', 'autor')  
    fieldsets = (
        ('Informații Generale', {
            'fields': ('categorie', 'pret', 'stoc')
        }),
        ('Campanii', {
            'fields': ('campanii',),
            'classes': ('collapse',),  # secțiune pliabilă
        }),
    )

admin.site.register(Produs, ProdusAdmin)

#relatii intre produse de admin

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('nume', 'gen_muzical') 
    search_fields = ('nume', 'gen_muzical')  
    fieldsets = (
        ('Informații Generale', {
            'fields': ('ani_activitate', 'tip_activitate')
        }),
    )

admin.site.register(Artist, ArtistAdmin)