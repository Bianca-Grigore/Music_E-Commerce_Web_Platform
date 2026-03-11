from django.urls import path
from . import views
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from .models import Campanie_Promo
from .sitemaps import ProdusSitemap, StaticViewSitemap, CategorieSitemap, ArtistSitemap
#laborator 9 task 2
info_campanii = {
    'queryset': Campanie_Promo.objects.all(),
    'date_field': 'data_inceput',
}

sitemaps = {
    'static': StaticViewSitemap,
    'produse': ProdusSitemap,
    'categorii': CategorieSitemap,
    'artisti': ArtistSitemap,
    'campanii': GenericSitemap(info_campanii, priority=0.6, changefreq='monthly'),
}

urlpatterns = [
	path("", views.index, name="index"),
    path("info/", views.info, name="info"), 
    path('test_accesare/', views.test_accesare),
    path("exemplu/", views.afis_template, name="exemplu"),
    path("log/", views.log, name="log"),
    path('produse/', views.lista_produse, name='lista_produse'),
    path("despre/", views.despre, name="despre"),
    path("cos_virtual/", views.in_lucru, name="cos_virtual"),
    path("in_lucru/", views.in_lucru, name="in_lucru"),
    path("baza/", views.baza, name="baza"),
    path("comenzi/", views.in_lucru, name="comenzi"),
    path("social/", views.in_lucru, name="social"),
    path("produse/<int:produs_id>/", views.detalii_produs, name="Detalii_produs"),
    path('categorii/<str:nume_categorie>/', views.produse_dupa_categorie, name='produse_dupa_categorie'),
    path("product_list_view/", views.product_list_view, name="product_list_view"),
    path("contact/", views.contact_view, name="contact_page"),
    #path('adaugare/', views.introducere_produs, name='adaugare_produs'),
    path('adaugare_produs/', views.introducere_produs, name='adaugare'),
    path('inregistrare/', views.register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profil/', views.pagina_profil_view, name='profil'),
    path('schimba_parola/', views.change_password_view, name='schimbare_parola'),
    path('confirma_mail/<str:cod>/', views.confirma_email_view, name='confirma_mail'),
    path('promotii/', views.pagina_promotii, name='pagina_promotii'),
    path('trimite_alerta_admin', views.trimite_alerta_admin, name='trimite_alerta_admin'),
    path('revendica-oferta/', views.revendica_oferta, name='revendica_oferta'),
    path('oferta-speciala/', views.afisare_oferta, name='pagina_oferta'),
    path('logout/', views.custom_logout, name='custom_logout'),



    path('produs/<int:pk>/', views.vizualizare_produs, name='Detalii_produs'),

    path('categorii/<str:nume_categorie>/', views.produse_dupa_categorie, name='produse_dupa_categorie'),

    path('artist/<int:pk>/', views.detalii_artist, name='detaliu_artist'),
    
    path('campanie/<int:pk>/', views.detalii_campanie, name='detaliu_campanie'),

    path('inregistrare/', views.register_view, name='register'),
    path('login/', views.custom_login_view, name='login'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
