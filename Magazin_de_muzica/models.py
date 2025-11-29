from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Promotii(models.Model):
    nume=models.CharField(max_length=100)
    descriere=models.TextField()
    data_creare=models.DateTimeField(default=timezone.now)
    data_expirare=models.DateTimeField()
    procent_reducere=models.DecimalField(max_digits=5, decimal_places=2)
    subiect_email=models.CharField(max_length=255, help_text="Subiectul care va apărea în mail")
    categorii=models.ManyToManyField('Categorie', help_text="Categorii la care se aplică promoția")
    def __str__(self):
        return f"{self.nume} (-{self.procent_reducere}%)"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Vizualizare(models.Model):
    utilizator = models.ForeignKey(User, on_delete=models.CASCADE)
    produs=models.ForeignKey('Produs', on_delete=models.CASCADE)
    # Folosim auto_now=True pentru ca data să se actualizeze de fiecare dată 
    # când utilizatorul revede același produs (îl aduce în capul listei)
    data_vizualizarii = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-data_vizualizarii'] #cele mai recente primele
    def __str__(self):
        return f"{self.utilizator.username} a vizualizat {self.produs.denumire}"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=15, blank=True)
    tara = models.CharField(max_length=100, blank=True)
    judet = models.CharField(max_length=100, blank=True)
    oras = models.CharField(max_length=100, blank=True)
    strada = models.CharField(max_length=255, blank=True)

    cod=models.CharField(max_length=100, blank=True, null=True, unique=True)
    email_confirmat=models.BooleanField(max_length=255, default=False)

    def __str__(self):
        return f"Profil pentru {self.user.username}"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Comanda(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_comanda = models.DateTimeField(default=timezone.now)

    METODA_PLATA = [
        ('card', 'Card Online'),
        ('ramburs', 'Ramburs la livrare'),
        ('transfer', 'Transfer Bancar')
    ]
    metoda = models.CharField(max_length=20, choices=METODA_PLATA, default='ramburs')

    STATUS_COMANDA = [
        ('plasata', 'Plasată'),
        ('procesare', 'În procesare'),
        ('expediata', 'Expediată'),
        ('finalizata', 'Finalizată'),
        ('anulata', 'Anulată')
    ]
    status_comanda = models.CharField(max_length=20, choices=STATUS_COMANDA, default='plasata')
    
    status_livrare = models.CharField(max_length=50, blank=True, null=True)
    data_livrare = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Comanda #{self.id} - {self.user.username} ({self.get_status_comanda_display()})"


class DetaliiComanda(models.Model):

    comanda = models.ForeignKey(Comanda, on_delete=models.CASCADE, related_name='detalii')
    produs = models.ForeignKey('Produs', on_delete=models.CASCADE)
    cantitate = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.produs.denumire} x {self.cantitate} (Cmd {self.comanda.id})"


class Review(models.Model):

    produs = models.ForeignKey('Produs', on_delete=models.CASCADE, related_name='reviewuri')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    descriere = models.TextField()
    data_publicarii = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review de la {self.user.username} pentru {self.produs.denumire}"


class Rating(models.Model):

    produs = models.ForeignKey('Produs', on_delete=models.CASCADE, related_name='ratinguri')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    valoare = models.PositiveIntegerField()
    
    TIP_RATING = [
        ('produs', 'Calitate Produs'),
        ('livrare', 'Experiență Livrare'),
        ('pret', 'Raport Calitate/Preț')
    ]
    tip_rating = models.CharField(max_length=20, choices=TIP_RATING, default='produs')
    data_rating = models.DateTimeField(default=timezone.now)

    class Meta:

        constraints = [
            models.UniqueConstraint(fields=['produs', 'user', 'tip_rating'], name='unique_rating_user_produs')
        ]

    def __str__(self):
        return f"{self.valoare}* - {self.produs.denumire} ({self.user.username})"

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Categorie(models.Model):
    nume_categorie = models.CharField(max_length=100, unique=True)  
    data_creare = models.DateTimeField(default=timezone.now)        
    data_actualizare = models.DateTimeField(auto_now=True)          
    
    TIP_CATEGORIE = [
        ('C', 'CD-uri'),
        ('K', 'Casete'),
        ('V', 'Vinyl'), 
        ('M', 'Merch')
    ]
    tip_categorie = models.CharField(max_length=1, choices=TIP_CATEGORIE, default='C') 
    culoare =models.CharField(max_length=20, default='#6A5ACD')
    def __str__(self):
        return self.nume_categorie

class Campanie_Promo(models.Model):
    nume_campanie = models.CharField(max_length=100, unique=True)    
    data_inceput = models.DateTimeField(default=timezone.now)           
    data_sfarsit = models.DateField()
    reducere = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) 

    TIP_CAMPANIE = [
        ('S', 'Seasonal'),
        ('F', 'Flash'),
        ('B', 'BlackFriday')
    ]
    tip_campanie = models.CharField(max_length=1, choices=TIP_CAMPANIE, default='S')  

    def __str__(self):
        return self.nume_campanie

class Produs(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    denumire = models.TextField()
    pret = models.PositiveIntegerField()       
    stoc = models.FloatField(default=0.0)              
    campanii = models.ManyToManyField(Campanie_Promo, blank=True)
    data_adaugare = models.DateTimeField(default=timezone.now)  
    imagine = models.ImageField(upload_to='produse/', blank=True, null=True) 
    
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
    nume = models.CharField(max_length=100, unique=True)  
    gen_muzical = models.CharField(max_length=100)
    ani_activitate = models.IntegerField(null=True, blank=True)  

    TIP_ACTIVITATE = [
        ('S', 'Solo'),
        ('B', 'Band'),
        ('D', 'Duo')
    ]
    tip_activitate = models.CharField(max_length=1, choices=TIP_ACTIVITATE, default='S') 
    data_adaugare = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return self.nume

