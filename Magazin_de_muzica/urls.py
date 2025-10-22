from django.urls import path
from . import views
urlpatterns = [
	path("", views.index, name="index"),
    path("info/", views.info, name="info"), 
    path('test_accesare/', views.test_accesare),
    path("exemplu", views.afis_template, name="exemplu"),
    path("log/", views.log, name="log"),
]
