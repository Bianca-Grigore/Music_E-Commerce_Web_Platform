from django.db import models
from django.utils import timezone

# Create your models here.
# class Organizator(models.Model):
#     nume = models.CharField(max_length=100)
#     email = models.EmailField()
#     def __str__(self):
#         return self.nume
    
# class Locatie(models.Model):
#     adresa = models.CharField(max_length=255)
#     oras = models.CharField(max_length=100)
#     judet = models.CharField(max_length=100)
#     cod_postal = models.CharField(max_length=10)
    
#     def __str__(self):
#         return f"{self.adresa}, {self.oras}"


#CERINTE TASK 1 LABORATOR 3 

# In descrierea modelelor trebuie sa aveti toate aceste tipuri de restrictii, dar nu neaparat aplicate pe acelasi model (pot fi si modele care nu au deloc restrictii sau doar o parte)
# un camp care admite si valori null
# un camp unic (altul decat id-ul)
# un camp cu choices (un camp text care admite doar anumite valori)
# un camp cu valoare default
# un camp de tip datetime, care are imiplicit data adaugarii


# Introduceti minim 5 randuri in tabele (in special tabelul cu produsele)


class Categorie(models.Model):
    nume_categorie = models.CharField(max_length=100, unique=True)  # camp unic
    data_creare = models.DateTimeField(default=timezone.now)        # datetime implicit
    data_actualizare = models.DateTimeField(auto_now=True)          # update automat
    
    TIP_CATEGORIE = [
        ('C', 'CD-uri'),
        ('K', 'Casete'),
        ('V', 'Vinyl'), 
        ('M', 'Merch')
    ]
    tip_categorie = models.CharField(max_length=1, choices=TIP_CATEGORIE, default='C')  # choices + default

    def __str__(self):
        return self.nume_categorie


class Campanie_Promo(models.Model):
    nume_campanie = models.CharField(max_length=100, unique=True)      # camp unic
    data_inceput = models.DateTimeField(default=timezone.now)           # datetime implicit
    data_sfarsit = models.DateField()
    reducere = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # default

    TIP_CAMPANIE = [
        ('S', 'Seasonal'),
        ('F', 'Flash'),
        ('B', 'BlackFriday')
    ]
    tip_campanie = models.CharField(max_length=1, choices=TIP_CAMPANIE, default='S')  # choices + default

    def __str__(self):
        return self.nume_campanie


class Produs(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    denumire = models.TextField()
    pret = models.PositiveIntegerField(default=0)       # default
    stoc = models.FloatField(default=0.0)              # default
    campanii = models.ManyToManyField(Campanie_Promo, blank=True)
    data_adaugare = models.DateTimeField(default=timezone.now)  # datetime implicit

    def __str__(self):
        return self.denumire


class Produs_Artist(models.Model):
    produs = models.ForeignKey('Produs', on_delete=models.CASCADE, null=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE, null=True)

    rol_artist = models.CharField(max_length=300, null=True, blank=True)
    colaborare_speciala = models.CharField(max_length=200, null=True, blank=True)
    descriere = models.TextField(blank=True)

    TIP_ROL = [
        ('S', 'Solist'),
        ('B', 'Background'),
        ('P', 'Producer')
    ]
    tip_rol = models.CharField(max_length=1, choices=TIP_ROL, default='S')
    data_adaugare = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['produs', 'artist'], name='unique_produs_artist')
        ]

    def __str__(self):
        return f"{self.rol_artist} ({self.tip_rol}) - {self.artist} / {self.produs}"
    


class Artist(models.Model):
    nume = models.CharField(max_length=100, unique=True)  # camp unic
    gen_muzical = models.CharField(max_length=100)
    ani_activitate = models.IntegerField(null=True, blank=True)  # camp null

    TIP_ACTIVITATE = [
        ('S', 'Solo'),
        ('B', 'Band'),
        ('D', 'Duo')
    ]
    tip_activitate = models.CharField(max_length=1, choices=TIP_ACTIVITATE, default='S')  # choices + default
    data_adaugare = models.DateTimeField(default=timezone.now)  # datetime implicit

    def __str__(self):
        return self.nume
