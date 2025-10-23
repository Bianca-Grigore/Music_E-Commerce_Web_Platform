from django.urls import path
from . import views
urlpatterns = [
	path("", views.index, name="index"),
    path("info/", views.info, name="info"), 
    path('test_accesare/', views.test_accesare),
    path("exemplu/", views.afis_template, name="exemplu"),
    path("log/", views.log, name="log"),
    path("produse", views.afis_produse, name="produse"),
    path("despre/", views.despre, name="despre"),
    path("contact/", views.contact, name="contact"),
    path("cos_virtual/", views.cos_virtual, name="cos_virtual"),
    path("in_lucru/", views.in_lucru, name="in_lucru"),
    path("baza/", views.baza, name="baza"),
]
