from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Produs, Categorie, Artist

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):

        return ['index', 'contact_page', 'despre']

    def location(self, item):
        return reverse(item)


class ProdusSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Produs.objects.all()

    def lastmod(self, obj):
        return obj.data_adaugare


class CategorieSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Categorie.objects.all()
    
    def lastmod(self, obj):
        return obj.data_actualizare


class ArtistSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Artist.objects.all()

    def lastmod(self, obj):
        return obj.data_adaugare