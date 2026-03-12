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

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profil

#laborator 8 task 4
from django.contrib.auth.admin import UserAdmin

class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'Profil Utilizator'
    
    def get_readonly_fields(self, request, obj=None):

        if request.user.groups.filter(name='Moderatori').exists() and not request.user.is_superuser:


            return ['telefon', 'tara', 'judet', 'oras', 'strada', 'cod', 'email_confirmat']

        return []


class CustomUserAdmin(UserAdmin):
    inlines = (ProfilInline,)
    
    def get_readonly_fields(self, request, obj=None):

        if request.user.is_superuser:
            return super().get_readonly_fields(request, obj)


        if request.user.groups.filter(name='Moderatori').exists():

            readonly_fields = set([f.name for f in self.model._meta.fields])

            allowed_fields = ['first_name', 'last_name', 'email']
            
            for field in allowed_fields:
                if field in readonly_fields:
                    readonly_fields.remove(field)


            extra_readonly = [
                'password', 'username', 'last_login', 'date_joined',
                'user_permissions', 'groups', 'is_superuser', 'is_staff', 'is_active'
            ]
            readonly_fields.update(extra_readonly)

            return list(readonly_fields)

        return super().get_readonly_fields(request, obj)

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

