from django.urls import path
from . import views
urlpatterns = [
	path("/", views.index, name="index"),
    path("info/", views.info, name="info"), 
    path('test_accesare/', views.test_accesare),
    path("exemplu/", views.afis_template, name="exemplu"),
    path("log/", views.log, name="log"),
    path('produse/', views.lista_produse, name='lista_produse'),
    path("despre/", views.despre, name="despre"),
    path("contact/", views.in_lucru, name="contact"),
    path("cos_virtual/", views.in_lucru, name="cos_virtual"),
    path("in_lucru/", views.in_lucru, name="in_lucru"),
    path("baza/", views.baza, name="baza"),
    path("comenzi/", views.in_lucru, name="comenzi"),
    path("social/", views.in_lucru, name="social"),
    path("produse/<int:produs_id>/", views.detalii_produs, name="Detalii_produs"),
    path('categorii/<str:nume_categorie>/', views.produse_dupa_categorie, name='produse_dupa_categorie'),
]