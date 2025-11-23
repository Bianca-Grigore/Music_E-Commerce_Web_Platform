from django import forms
from .models import Categorie, Campanie_Promo, Produs
from django.core.exceptions import ValidationError
from datetime import date, timedelta
import re
from django.core.validators import MinValueValidator
from decimal import Decimal
#-------------------------------------------------------------
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil # Presupunând că ai importat corect modelul Profil

#LABORATOR 6 EX 3
class ProfilUserCreationForm(UserCreationForm):
    # Câmpurile User pe care UserCreationForm nu le cere automat, dar le vrem
    email = forms.EmailField(required=True, label='E-mail') # Email-ul nu e obligatoriu în UserCreationForm, dar e cerut în task
    first_name = forms.CharField(max_length=150, required=False, label='Prenume') # Adăugat pentru a folosi în save()
    last_name = forms.CharField(max_length=150, required=False, label='Nume') # Adăugat pentru a folosi în save()

    # Câmpurile suplimentare din modelul Profil
    telefon = forms.CharField(max_length=15, required=True, label='Telefon') # Setat pe True pentru a se aplica validările
    tara = forms.CharField(max_length=100, required=True, label='Țara')
    judet = forms.CharField(max_length=100, required=False, label='Județ')
    oras = forms.CharField(max_length=100, required=False, label='Oraș')
    strada = forms.CharField(max_length=255, required=False, label='Strada')

    class Meta(UserCreationForm.Meta):
        model = User
        # Lăsăm doar câmpurile pe care le gestionează modelul User, 
        # plus câmpurile noi adăugate la nivel de clasă (telefon, tara, etc. vor fi preluate automat)
        fields = ('username', 'email', 'first_name', 'last_name') # Doar câmpurile din modelul User standard
    
    # --- Validările sunt corecte și rămân ca atare ---
    def clean_telefon(self):
        telefon = self.cleaned_data.get('telefon')
        if not telefon.isdigit():
            raise forms.ValidationError("Telefonul trebuie să conțină doar cifre.")
        if len(telefon) < 10:
            raise forms.ValidationError("Numărul de telefon este prea scurt.")
        return telefon

    def clean_tara(self):
        tara = self.cleaned_data.get('tara')
        if tara.lower() not in ["romania", "românia"]:
            raise forms.ValidationError("Momentan acceptăm doar utilizatori din România.")
        return tara

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Această adresă de e-mail este deja folosită.")
        return email

    def save(self, commit=True):
        # 1. Salvarea User-ului
        user = super().save(commit=False) 
        
        # Corectat: Folosim get() pe cleaned_data pentru a evita erorile 
        # (deși first_name/last_name ar trebui să fie deja acolo)
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        
        if commit:
            user.save()
            
        # 2. Salvarea Profilului
        profil = Profil(
            user=user,
            telefon=self.cleaned_data.get('telefon'),
            tara=self.cleaned_data.get('tara'),
            judet=self.cleaned_data.get('judet'),
            oras=self.cleaned_data.get('oras'),
            strada=self.cleaned_data.get('strada')
        )
        
        if commit:
            profil.save()
            
        return user

#-----------------------------------------------------------------------------------------------------------------------------
#Laborator 6 exercitiul 4 formular de login si logout 
from django.contrib.auth.forms import AuthenticationForm
class CustomAuthenticationForm(AuthenticationForm):
    ramane_logat = forms.BooleanField(
        required=False,
        initial=False,
        label='Ramaneti logat 1 zi?'
    )

    def clean(self):        
        cleaned_data = super().clean()
        ramane_logat = self.cleaned_data.get('ramane_logat')
        return cleaned_data

#-----------------------------------------------------------------------------------------------------------------------------
PAGINATION_CHOICES = [
    (5, '5 pe pagină (Implicit)'), 
    (10, '10 pe pagină'),
    (30, '30 pe pagină'),
    (50, '50 pe pagină'),
]
class ProductFilterForm(forms.Form):
    
    categorie_id =forms.IntegerField(
        label = "Id categorie",
        required=False,
        widget=forms.HiddenInput()
    )
    
    categorie = forms.ModelChoiceField(
        queryset=Categorie.objects.all(), 
        label='Categorie', 
        required=False,
        empty_label="Toate Categoriile" 
    )
    denumire = forms.CharField(
        max_length=200, 
        label='Căutare Denumire', 
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Căutare parțială...'})
    )

    pret_min = forms.IntegerField(
        label='Preț Min.', 
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    pret_max = forms.IntegerField(
        label='Preț Max.', 
        required=False, 
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )

    stoc_min = forms.FloatField(
        label='Stoc Min.', 
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Min'})
    )
    stoc_max = forms.FloatField(
        label='Stoc Max.', 
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Max'})
    )
    campanii = forms.ModelMultipleChoiceField(
        queryset=Campanie_Promo.objects.all(), 
        label='Campanii Incluse', 
        required=False,
        help_text="Filtrează produsele care fac parte din oricare dintre campaniile selectate."
    )
    data_adaugare_min = forms.DateTimeField(
        label='Adăugat după',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    data_adaugare_max = forms.DateTimeField(
        label='Adăugat înainte',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    are_imagine = forms.BooleanField(
        label='Doar produse cu imagine',
        required=False
    )
    
    produse_per_pagina = forms.ChoiceField(
        choices=PAGINATION_CHOICES,
        label='Produse afișate',
        required=False,
        initial=PAGINATION_CHOICES[0][0] 
    )
    
    
    
    def clean(self):
        cleaned_data = super().clean()
        pret_min = cleaned_data.get('pret_min')
        pret_max = cleaned_data.get('pret_max')
        
        if pret_min is not None and pret_max is not None and pret_min > pret_max:
            raise forms.ValidationError('Prețul minim nu poate fi mai mare decât prețul maxim.')

        stoc_min = cleaned_data.get('stoc_min')
        stoc_max = cleaned_data.get('stoc_max')
        
        if stoc_min is not None and stoc_max is not None and stoc_min > stoc_max:
            raise forms.ValidationError('Stocul minim nu poate fi mai mare decât stocul maxim.')

        data_adaugare_min = cleaned_data.get('data_adaugare_min')
        data_adaugare_max = cleaned_data.get('data_adaugare_max')
        
        if data_adaugare_min and data_adaugare_max and data_adaugare_min > data_adaugare_max:
            raise forms.ValidationError('Data adăugării minime nu poate fi după data maximă.')

        return cleaned_data


#-----------------------------------------------------------------------------------------------------------------------------

TIP_MESAJ_CHOICES = [
    ('neselectat', '--- Neselectat ---'),
    ('reclamatie', 'Reclamație'),
    ('intrebare', 'Întrebare'),
    ('review', 'Review'),
    ('cerere', 'Cerere'),
    ('programare', 'Programare'),
]
    
#2.i)
def validare_format_text(value):
    if not value:
        return 
    if not value[0].isupper():
        raise ValidationError('Textul trebuie să înceapă cu literă mare.', code = 'incepe_litera_mare')
    if not re.fullmatch(r'^[A-Za-z\s-]+$', value):
        raise ValidationError('Textul poate conține doar litere, spații și cratime.', code='caractere_invalide')
    
#2.j)
def validare_caps_after_separator(value):
    
    if not value:
        return
    if re.search(r'[ -][a-z]', value):
        raise ValidationError('După spațiu sau cratimă trebuie să urmeze literă mare.', code='litera_mica_dupa_separator')
    
#2.d)
def validare_no_links(value):
    if re.search(r'https?://\S+', value, re.IGNORECASE):
        raise ValidationError('Mesajul nu trebuie să conțină link-uri.', code='contine_link')
    
#2.f) g)
def validare_cnp_format(value):
    if not value:
        return
    if len(value) != 13 or not value.isdigit():
        raise ValidationError('CNP-ul trebuie să conțină exact 13 cifre.', code='cnp_format_invalid')
    
    
    year = int(value[1:3])
    month = int(value[3:5])
    day = int(value[5:7])
    
    if value[0] not in ('1', '2'):
        raise ValidationError('CNP-ul trebuie să înceapă cu 1 sau 2.', code='cnp_start_invalid')
    else:
        full_year=year + 1900


    if month < 1 or month > 12:
        raise ValidationError('Luna din CNP este invalidă.', code='cnp_luna_invalida')
    if day < 1 or day > 31:
        raise ValidationError('Ziua din CNP este invalidă.', code='cnp_zi_invalida')
    
    if full_year > date.today().year:
        raise ValidationError('Anul din CNP este în viitor.', code='cnp_an_viitor')
    
    try:
        date(full_year, month, day) 
    except ValueError:
        raise ValidationError('Data din CNP este invalidă.', code='cnp_data_invalida')  

#2.h)
def validare_no_temp_email(value):
    temp_domains=['guerillamail.com', 'yopmail.com']
    try:
        domain=value.split('@')[1].lower()
    except IndexError:
        return
    if domain in temp_domains:
        raise ValidationError('Adresa de email nu trebuie să fie de tip temporar.', code='email_temporar')

#2. b)
def validate_word_count(value):
    words = re.findall(r'[A-Za-z0-9]+', value) 
    count = len(words)
    
    if count < 5 or count > 100:
        raise ValidationError(f'Mesajul trebuie să conțină între 5 și 100 de cuvinte (curente: {count}).', code='numar_cuvinte_invalid')

#2.c)
def validate_word_length(value):
    words = re.findall(r'[A-Za-z0-9]+', value)
    
    for word in words:
        if len(word) > 15:
            raise ValidationError(f'Cuvântul "{word[:10]}..." depășește limita de 15 caractere.', code='lungime_cuvant_depasita')

#2.a)
def validate_age_over_18(value):
    today = date.today()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    if age < 18:
        raise ValidationError('Expeditorul trebuie să aibă minim 18 ani (să fie major).', code='nu_este_major')

#----------------------------------------------------------------------------------------------------------------------------------------

class ContactForm(forms.Form):
    nume= forms.CharField(max_length=10, label='Nume', required=True,
    validators=[validare_format_text, validare_caps_after_separator]
    )
    prenume= forms.CharField(max_length=10, label='Prenume', required=False, 
        validators=[validare_format_text, validare_caps_after_separator]
        )
    CNP= forms.CharField(max_length=13, label='CNP', required=False,
        validators=[validare_cnp_format]                 
        )
    data_nastere= forms.DateField(label='Data Nasterii', required=True, 
        validators=[validate_age_over_18]
        )
    email= forms.EmailField(label='Email', required=True, 
        validators=[validare_no_temp_email]
        )
    confirmare_email= forms.EmailField(label='Confirmare Email', required=True, 
        validators=[validare_no_temp_email]
        )
    tip_mesaj= forms.ChoiceField(
        choices=TIP_MESAJ_CHOICES,
        label='Tip Mesaj',
        initial='neselectat',
        required=True,
    )
    subiect= forms.CharField(max_length=100, label='Subiect', required=True, 
        validators=[validare_format_text, validare_no_links]
        )
    min_zile_asteptare= forms.IntegerField(
        label='Număr minim de zile de așteptare pentru răspuns',
        required=False,
        min_value=1,
        max_value=30,
        help_text="Pentru review-uri/cereri minimul de zile de așteptare trebuie setat de la 4 încolo, iar pentru cereri/întrebări de la 2 încolo. Maximul e 30."
    )
    mesaj= forms.CharField(
        label= "Mesajul tău (te rugăm să te și semnezi)",
        required=True,
        widget=forms.Textarea(attrs={'rows': 5}),
        validators=[validare_no_links, validate_word_count, validate_word_length]
    )




def clean_tip_mesaj(self):
        tip_mesaj = self.cleaned_data.get('tip_mesaj')
        if tip_mesaj == 'neselectat':
            raise ValidationError("Te rugăm să selectezi un tip de mesaj valid și diferit de 'neselectat'.", code='tip_neselectat')
        return tip_mesaj
    
def clean(self):
        cleaned_data = super().clean()
        nume = cleaned_data.get('nume')
        cnp = cleaned_data.get('CNP')
        data_nastere = cleaned_data.get('data_nastere')
        email = cleaned_data.get('email')
        confirmare_email = cleaned_data.get('confirmare_email')
        tip_mesaj = cleaned_data.get('tip_mesaj')
        zile_asteptare = cleaned_data.get('min_zile_asteptare')
        mesaj = cleaned_data.get('mesaj')


        if email and confirmare_email and email != confirmare_email:
            self.add_error('confirmare_email', "Adresele de e-mail nu se potrivesc.", code='email_mismatch')



        if tip_mesaj and zile_asteptare:
            
            if tip_mesaj in ['review', 'cerere'] and zile_asteptare < 4:
                self.add_error(
                    'min_zile_asteptare', 
                    f"Pentru tipul '{tip_mesaj}', minimul de zile de așteptare trebuie să fie de la 4 încolo."
                )
            
            elif tip_mesaj == 'intrebare' and zile_asteptare < 2:
                self.add_error(
                    'min_zile_asteptare', 
                    "Pentru 'întrebare', minimul de zile de așteptare trebuie să fie de la 2 încolo."
                )



        if nume and mesaj:
            import re
            
            match = re.search(r'([A-Za-z]+)\W*$', mesaj)
            
            if match:
                ultimul_cuvant = match.group(1)
                
                if ultimul_cuvant.lower() != nume.lower():
                    self.add_error('mesaj', 
                "Mesajul trebuie să se încheie cu numele dumneavoastră (semnătura).", code='semnatura_invalida')
            else:
                self.add_error('mesaj', "Mesajul trebuie să conțină o semnătură la final.", code='lipsa_semnatura')




        if cnp and data_nastere:
            try:
                
                cnp_start_digit = int(cnp[0])
                cnp_an = int(cnp[1:3])
                cnp_luna = int(cnp[3:5])
                cnp_zi = int(cnp[5:7])

                
                an_complet = cnp_an + (1900 if cnp_start_digit in (1, 2) else 0) 
                
                
                data_nastere_cnp = date(an_complet, cnp_luna, cnp_zi)
                
                if data_nastere_cnp != data_nastere:
                    self.add_error('data_nastere', 
                        f"Data nașterii ({data_nastere.strftime('%d.%m.%Y')}) nu corespunde cu data extrasă din CNP ({data_nastere_cnp.strftime('%d.%m.%Y')}).", code='cnp_data_mismatch')
                    
            except ValueError:

                self.add_error('CNP', "Eroare la extragerea datei din CNP. Vă rugăm verificați ambele câmpuri.", code='cnp_extract_fail_internal')

        return cleaned_data













#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def validator_fara_cifre(value):
    if value.isdigit():
        raise ValidationError('Denumirea produsului nu poate conține doar cifre.', code='doar_cifre')
    

def validator_lungime_minima(value):
    if isinstance(value, str):
        if len(value) < 5:
            raise ValidationError('Acest câmp (text) necesită minim 5 caractere.', code='lungime_mica')
            
    elif isinstance(value, Decimal):
        if value < Decimal('1'):
            raise ValidationError('Prețul de cumpărare trebuie să fie minim 1.00.', code='valoare_minima_pret')


def validator_multiplu_zece(value):
    if value % 10 != 0:
        raise ValidationError('Stocul inițial trebuie să fie un multiplu de 10.', code='nu_multiplu_zece')

class ProdusForm(forms.ModelForm):
    pret_cumparare = forms.DecimalField(
        max_digits= 10,
        decimal_places=2,
        required= True,
        validators=[validator_lungime_minima],
        error_messages={'required': "Vă rugăm introduceți prețul de achiziție al produsului."},
        help_text="Introduceți prețul inițial de achiziție (de la furnizor)."
    )
    
    procent_adaos = forms.IntegerField(
        required= True, 
        validators=[MinValueValidator(10, message="Adaosul minim este 10%")],
        error_messages={'required': "Vă rugăm introduceți procentul de adaos comercial."},
    )
    class Meta:
        model = Produs 
        fields = ['categorie', 'denumire', 'stoc', 'campanii', 'imagine']
        labels ={
            'denumire' : 'Denumirea Produsului',
            'stoc': 'Cantitatea valabila care poate fi achizitionată',
            'campanii': 'Produsul poate sau nu poate fi eligibil pentru o campanie'
        }
        help_text ={
            'denumire': 'Introduceti un nume unic și descriptiv pentru produs.',
            'categorie': 'Fiecare produs are cel putin o categorie din care face parte.'
        }
        errors_messages={
            'stoc': {
                'required': 'Stocul initial este obligatoriu',
                'min_value': 'Valoarea minima trebuie sa fie un numar pozitiv'
            },

        }
        
    def clean_denumire(self):
        denumire=self.cleaned_data.get('denumire')
        validator_lungime_minima(denumire)
        validator_fara_cifre(denumire)
        if len(denumire.split()) <2:
            raise forms.ValidationError("Denumirea trebuie sa contina minim 2 cuvinte.", code = 'cuvinte_putine')
        return denumire 

    def clean_stoc(self):
        stoc=self.cleaned_data.get('stoc')
        validator_multiplu_zece(stoc)
        return stoc

    def clean(self):
            cleaned_data = super().clean()
            pret_cumparare = cleaned_data.get('pret_cumparare')
            procent_adaos = cleaned_data.get('procent_adaos')

            
            if pret_cumparare and procent_adaos:
                
                if pret_cumparare > Decimal('1000') and procent_adaos < 20:
                    
                    raise forms.ValidationError(
                        "Pentru produsele scumpe (peste 1000 RON), adaosul comercial minim este 20%.",
                        code='adaos_prea_mic'
                    )

            return cleaned_data
    def save(self, commit=True):
            
            produs = super().save(commit=False)
            
            pret_cumparare = self.cleaned_data.get('pret_cumparare')
            procent_adaos = self.cleaned_data.get('procent_adaos')
            
            
            if pret_cumparare is not None and procent_adaos is not None:
                adaos = pret_cumparare * (Decimal(procent_adaos) / Decimal('100'))
                produs.pret = int(pret_cumparare + adaos)
            
            produs.pret_baza = int(pret_cumparare)
            
            produs.descriere = f"Produs adăugat în categoria {produs.categorie} cu un preț final de {produs.pret} RON."

            if commit:
                produs.save()
                self.save_m2m() 
                
            return produs