from time import time
from django.shortcuts import render, redirect, get_object_or_404 
from django.http import HttpResponse
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter
from .models import Produs
from .forms import ProductFilterForm
from django.core.paginator import Paginator
from .models import Produs_Artist
from .models import Campanie_Promo
from .models import Categorie
import django.forms as forms
import os 
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings
from datetime import date
import re
import json
import time
from django.urls import reverse 

accesari = []

class Accesare:
    counter = 0  

    def __init__(self, ip_client=None, url=None, data=None, pagina_nume=None):
        Accesare.counter += 1
        self.id = Accesare.counter
        self.ip_client = ip_client
        self.url = url
        self.data = data
        self.pagina_nume = pagina_nume 

    def pagina(self):
        if self.pagina_nume:
            return self.pagina_nume
        if self.url:
            parsed = urlparse(self.url)
            return parsed.path
        return None

    def data_formatata(self, fstring="%Y-%m-%d %H:%M:%S"):
        if self.data is None:
            return None
        if isinstance(self.data, datetime):
            return self.data.strftime(fstring)
        try:
            return datetime.strptime(self.data, fstring).strftime(fstring)
        except ValueError:
            return None


#laborator 1 tema 

def afis_data(parametru):
    luni=['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']
    zile=['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
    
    prezent = datetime.now()
    zi_saptamana = zile[prezent.weekday()]
    zi_luna = prezent.day
    nume_luna = luni[prezent.month-1]
    an = prezent.year 
    ora = prezent.strftime("%H:%M:%S")
    
    if parametru=="zi":
        de_afisat=f"{zi_saptamana}, {zi_luna} {nume_luna} {an}"
    elif parametru=="timp":
        de_afisat=ora
    else:
        de_afisat=f"{zi_saptamana}, {zi_luna} {an}, {ora}"
    return f"""
        <section>
            <h2>Data si ora</h2>
            <p>{de_afisat}</p>
        </section>
    """

def index(request):
    salvare_accesari(request, "prima pagina")
    return HttpResponse("""
        <html>
        <body>
        <p><b>Descrierea proiectului</b></p>
        <p><i><b>Proiectul constă într-un site comercial dedicat iubitorilor de muzică, unde utilizatorii pot explora și achiziționa produse muzicale variate, precum CD-uri, viniluri, casete și articole de merch (tricouri, postere, accesorii). Fiecare produs va fi însoțit de detalii esențiale, precum denumirea, prețul, stocul disponibil și o descriere scurtă. Utilizatorii vor putea adăuga produse în coș, plasa comenzi și vizualiza istoricul achizițiilor. Site-ul va include filtre și categorii pentru a facilita căutarea produselor, iar administratorii vor putea gestiona stocurile și informațiile despre produse. Scopul proiectului este de a crea o experiență intuitivă și atractivă pentru clienți, combinând funcționalități comerciale cu o prezentare vizuală atractivă a produselor muzicale.
</b></i></p>
        </body>
        </html>
    """)

def test_accesare(request):
    a1= Accesare(
        ip_client="127.0.0.1",
        url=request.build_absolute_uri() + "?data=timp",
        data="2025-10-06 16:45:00"
    )
    a2=Accesare(
        ip_client="192.168.1.10",
        url="https://example.com/info?data=zi",
        data=datetime.now()
    )
    rezultat = ""
    for x in [a1, a2]:
        data_obj = x.data_formatata("%Y-%m-%d %H:%M:%S")
        pagina = x.pagina()
        url = x.url
        rezultat += f"""
            <p>
                ID {x.id} — IP: {x.ip_client} — Pagina: {pagina} — 
                URL complet: {url} — Data (datetime): {data_obj} — Tip: {type(data_obj).__name__}
            </p>
        """
    return HttpResponse(f"""
        <html>
        <body>
        <h2>Test pentru clasa Accesare</h2>
        {rezultat}
        </body>
        </html>
    """)





def info(request):
    salvare_accesari(request, "Pagina info")
    parametru = request.GET.get("data") 
    afisat = ""
    
    if parametru:
        afisat = afis_data(parametru)
        
    parametri = request.GET 
    numar_param = len(parametri.keys())
    nume_param = ",".join(parametri.keys())
    sectiune_parametri = f"""
        <section>
            <h2>Parametri</h2>
            <p>Numar parametri: {numar_param}</p>
            <p>Nume parametri: {nume_param}</p>
        </section>
    """

    return render(request, "Magazin_de_muzica/info.html", {"continut": afisat, "sectiune_parametri": sectiune_parametri })

def salvare_accesari(request,nume_pagina):
    a = Accesare(
        ip_client =request.META.get("REMOTE_ADDR"), 
        url= request.build_absolute_uri(), 
        data= datetime.now(),
        pagina_nume=nume_pagina
    )
    accesari.append(a)



#LABORATOR 2 TEMA

def log(request):
    
    salvare_accesari(request, "log")
    
    continut = ""

    # accesari=nr sau detalii
    
    nr_accesari = request.GET.get("accesari")
    if nr_accesari:
        if nr_accesari.lower() == "nr":
            total = len(accesari)
            continut += f"<h2>Numarul total de accesari curente este {total}.</h2>"
            
        elif nr_accesari.lower() == "detalii":
            continut += "<h1>Detalii accesari:</h1><ul>"
            for a in accesari:
                continut += f"<li>ID {a.id} — Pagina: {a.pagina()} — Data: {a.data_formatata()}</li>"
            continut += "</ul>"

    # iduri si dubluri 
    iduri = request.GET.getlist("iduri")
    dubluri = request.GET.get("dubluri", "false").lower() == "true"
    lista_id = []
    for id_ in iduri:
        lista_id.extend(id_.split(','))

    if lista_id:
        if not dubluri:
            lista_id_finala = []
            aux = set()
            for id_ in lista_id:
                if id_ not in aux:
                    lista_id_finala.append(id_)
                    aux.add(id_)
        else:
            lista_id_finala = lista_id

        continut += "<h1>Accesari dupa id-uri:</h1><ul>"
        for id_ in lista_id_finala:
            try:
                idx = int(id_) - 1
                continut += f"<li>{accesari[idx].pagina()}</li>"
            except (ValueError, IndexError):
                continut += f"<li>ID invalid: {id_}</li>"
        continut += "</ul>"



    #  tabel 
    parametru_tabel = request.GET.get("tabel")
    if parametru_tabel:
        proprietati = [p.strip() for p in parametru_tabel.split(',')]
        if "tot" in proprietati:
            proprietati = ["id", "ip_client", "url", "data"]

        continut += "<h1>Accesari in tabel:</h1><table border='1'><tr>"
        for prop in proprietati:
            continut += f"<th>{prop}</th>"
        continut += "</tr>"

        for a in accesari:
            continut += "<tr>"
            for prop in proprietati:
                valoare = getattr(a, prop, "N/A")
                if prop == "data" and valoare:
                    valoare = a.data_formatata()
                elif callable(valoare):
                    valoare = valoare()
                continut += f"<td>{valoare}</td>"
            continut += "</tr>"
        continut += "</table>"

        # Frecventa pagini
        frecventa = Counter([a.pagina() for a in accesari])
        if frecventa:
            pagina_max = max(frecventa, key=frecventa.get)
            pagina_min = min(frecventa, key=frecventa.get)
            continut += f"<p>Cea mai accesata pagina: <b>{pagina_max}</b></p>"
            continut += f"<p>Cea mai putin accesata pagina: <b>{pagina_min}</b></p>"

    # ultimele
    ultimele_accesari = request.GET.get("ultimele")
    
    if ultimele_accesari is not None:
        try:
            n = int(ultimele_accesari)
            if n < 0:
                raise ValueError
        except ValueError:
            continut += "<h2 style='color:purple'>Mesaj de eroare: parametrul nu este un numar intreg pozitiv</h2>"
        else:
            total_accesari = len(accesari)
            if n > total_accesari:
                continut += "<h1>Toate accesarile:</h1><ul>"
                for a in accesari:
                    continut += f"<li>{a.pagina()}</li>"
                continut += f"</ul><p style='color:purple'>Exista doar {total_accesari} fata de {n} accesari cerute.</p>"
            else:
                continut += f"<h1>Ultimele {n} accesari sunt:</h1><ul>"
                for a in accesari[-n:]:
                    continut += f"<li>{a.pagina()}</li>"
                continut += "</ul>"

    if not request.GET:
        continut += "<h2>Cererile catre paginile din site:</h2><ul>"
        for a in accesari:
            continut += f"<p>ID {a.id} — Pagina: {a.pagina()} — Data: {a.data_formatata()}</p>"
        continut+= "</ul>"
    return render(request, "Magazin_de_muzica/log.html", {"continut": continut})












def afis_template(request):
    context = {
        "nume": "Nume Paragraf",
        "user_ip": get_client_ip(request)
    }
    return render(request, "Magazin_de_muzica/exemplu.html", context)

#afisarea produselor pentru utilizatori

def afis_produse(request):
    salvare_accesari(request, "Pagina produselor")
    produse=Produs.objects.all()
    return render(request, "Magazin_de_muzica/produse.html",
        {          
            "produse": produse[0], 
        }
    )


#TASK 2 LAB 2

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def despre(request):
    salvare_accesari(request, "Pagina despre")
    context = {'user_ip': get_client_ip(request)}
    return render(request, 'Magazin_de_muzica/despre.html', context)
    
# def contact(request):
#     salvare_accesari(request, "Pagina de contact")
#     context = {'user_ip': get_client_ip(request)}
#     return render(request, "Magazin_de_muzica/in_lucru.html", context)

def cos_virtual(request):
    salvare_accesari(request, "Pagina cosului virtual")
    context = {'user_ip': get_client_ip(request)}
    return render(request, "Magazin_de_muzica/in_lucru.html", context)

def in_lucru(request):
    salvare_accesari(request, "Pagina in lucru")
    context = {'user_ip': get_client_ip(request)}
    return render(request, "Magazin_de_muzica/in_lucru.html", context) 

def baza(request):
    salvare_accesari(request, "Pagina de baza")
    return render(request, "Magazin_de_muzica/baza.html")

def comenzi(request):
    salvare_accesari(request, "Pagina comenzilor")
    context = {'user_ip': get_client_ip(request)}
    return render(request, "Magazin_de_muzica/in_lucru.html", context)

def social(request):
    salvare_accesari(request, "Pagina de social media")
    context = {'user_ip': get_client_ip(request)}
    return render(request, "Magazin_de_muzica/in_lucru.html", context)


#Curs 5 pentru laborator 5

# def contact_view(request):
#     if request.method == 'POST':
#         form = ContactForm(request.POST)
#         if form.is_valid():  
#             nume = form.cleaned_data['nume']
#             email = form.cleaned_data['email']
#             mesaj = form.cleaned_data['mesaj']
#             return redirect('mesaj_trimis')
#     else:
#         form = ContactForm()
#     return render(request, 'aplicatie_exemplu/contact.html', {'form': form})



#Task admin laborator 4

def lista_produse(request):
    sort = request.GET.get('sort', 'a')
    
    if sort == 'd':
        produse = Produs.objects.all().order_by('-denumire')  
    else:
        produse = Produs.objects.all().order_by('denumire')  


    paginator = Paginator(produse, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categorie=Categorie.objects.all()
    
    
    return render(request, 'Magazin_de_muzica/produse.html', {
        'page_obj': page_obj, 'sort': sort,
        'categorie': categorie,
        'categorie_selectata': None
        })

def detalii_produs(request, produs_id):
    produs = get_object_or_404(Produs, id=produs_id)
    
    produs_artist = get_object_or_404(Produs_Artist, produs=produs)
    campanii = Campanie_Promo.objects.filter(produs=produs)
    
    return render(request, 'Magazin_de_muzica/Detalii_produs.html', {
        'produs': produs,
        'produs_artist': produs_artist,
        'campanii': campanii
    })

#Task QuerySets laborator 4 

def produse_dupa_categorie(request, nume_categorie):
    cat=get_object_or_404(Categorie, nume_categorie=nume_categorie)
    
    
    sort =request.GET.get('sort', 'a')
    if sort =='a':
        produse=Produs.objects.filter(categorie=cat).order_by('denumire')
    else:
        produse=Produs.objects.filter(categorie=cat).order_by('-denumire')  
        
    paginator=Paginator(produse, 5)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    
    
    categorie=Categorie.objects.all()
    
    return render(request, 'Magazin_de_muzica/produse.html', {
        'page_obj': page_obj,
        'sort': sort,
        'categorie': categorie,
        'categorie_selectata': cat
    })






#Task 1 Laborator 5 

# def filtre_produse(request):

#     produse = Produs.objects.all()
#     categorie_selectata = None
#     sort_param = request.GET.get('sort', 'denumire') 
#     #preluarea datelor pentru formular
#     filter_form = ProductFilterForm(request.GET)
#     items_per_page=5
#     repaginare_warning=False 

    
#     if filter_form.is_valid():
#         data = filter_form.cleaned_data
#         selected_items_per_page = data.get('produse_per_pagina')
#         if selected_items_per_page:
#             new_items_per_page = int(selected_items_per_page)
#             if new_items_per_page != items_per_page:
#                 repaginare_warning = True
                
#             items_per_page = new_items_per_page


#         categorie = data.get('categorie')
#         if categorie:
#             produse = produse.filter(categorie=categorie)
#             categorie_selectata = categorie # Păstrează obiectul pentru a fi afișat în titlu

#         denumire = data.get('denumire')
#         if denumire:
#             produse = produse.filter(denumire__icontains=denumire)


#         pret_min = data.get('pret_min')
#         if pret_min is not None:
#             produse = produse.filter(pret__gte=pret_min)
#         pret_max = data.get('pret_max')
#         if pret_max is not None:
#             produse = produse.filter(pret__lte=pret_max)
            

#         stoc_min = data.get('stoc_min')
#         if stoc_min is not None:
#             produse = produse.filter(stoc__gte=stoc_min)
#         stoc_max = data.get('stoc_max')
#         if stoc_max is not None:
#             produse = produse.filter(stoc__lte=stoc_max)
            
#         campanii = data.get('campanii')
#         if campanii:
            
#             produse = produse.filter(campanii__in=campanii).distinct() 
            
        
#         data_adaugare_min = data.get('data_adaugare_min')
#         if data_adaugare_min:
#             produse = produse.filter(data_adaugare__gte=data_adaugare_min)
#         data_adaugare_max = data.get('data_adaugare_max')
#         if data_adaugare_max:
#             produse = produse.filter(data_adaugare__lte=data_adaugare_max)
            
        
#         are_imagine = data.get('are_imagine')
#         if are_imagine:
#             produse = produse.filter(imagine__isnull=False).exclude(imagine='')


    
#     if sort_param == 'a': 
#         produse = produse.order_by('pret')
#     elif sort_param == 'd': 
#         produse = produse.order_by('-pret')



#     paginator = Paginator(produse, items_per_page)
#     page_number=request.GET.get('page')
    
#     try: 
#         page_obj = paginator.get_page(page_number)
#     except Exception:
#         page_obj = paginator.get_page(1)

#     context = {
#         'filter_form': filter_form,
#         'page_obj': page_obj, 
#         'repaginare_warning': repaginare_warning,
#         'sort': sort_param, 
#         'categorie_selectata': categorie_selectata, 
#     }
    
#     return render(request, 'Magazin_de_muzica/produse.html', context)





def product_list_view(request, categorie_slug=None):
    produse = Produs.objects.all()
    categorie_selectata =None 
    items_per_page =5
    repaginare_warning =False
    
    if categorie_slug :
        categorie_selectata=get_object_or_404(Categorie, nume_categorie=categorie_slug)
        produse =produse.filter(categorie=categorie_selectata)
        
        initial_data =request.GET.copy()
        initial_data['categorie'] =categorie_selectata.pk 
        filter_form =ProductFilterForm(initial_data)
        
        if request.GET.get('categorie') and str(categorie_selectata.pk) != request.GET.get('categorie'):
            filter_form.add_error('categorie', "Valoarea categoriei nu poate fi modificata pe aceasta pagina.")
            produse =Produs.objects.none()
        
        filter_form.fields['categorie'].widget =forms.HiddenInput()
        
    else:
        filter_form =ProductFilterForm(request.GET)
        
    if filter_form.is_valid():
        data=filter_form.cleaned_data 
        
        selected_items_per_page =data.get('produse_per_pagina')
        if selected_items_per_page:
            new_items_per_page =int(selected_items_per_page)
            if new_items_per_page != 5:
                repaginare_warning =True
            items_per_page =new_items_per_page
            
        denumire =data.get('denumire')
        if denumire:
            produse =produse.filter(denumire__icontains=denumire)
        
        pret_min =data.get('pret_min')
        if pret_min is not None:
            produse =produse.filter(pret__gte=pret_min)
        pret_max =data.get('pret_max')
        if pret_max is not None:
            produse =produse.filter(pret__lte=pret_max)
        stoc_min =data.get('stoc_min')
        if stoc_min is not None:
            produse =produse.filter(stoc__gte=stoc_min)
        stoc_max =data.get('stoc_max')
        if stoc_max is not None:
            produse =produse.filter(stoc__lte=stoc_max)
        campanii =data.get('campanii')
        if campanii:
            produse =produse.filter(campanii__in=campanii).distinct()
        are_imagine =data.get('are_imagine')
        if are_imagine:
            produse =produse.filter(imagine__isnull=False).exclude(imagine='')
        data_adaugare_min =data.get('data_adaugare_min')
        if data_adaugare_min:
            produse =produse.filter(data_adaugare__gte=data_adaugare_min)
        data_adaugare_max =data.get('data_adaugare_max')
        if data_adaugare_max:
            produse =produse.filter(data_adaugare__lte=data_adaugare_max)
    sort_param =request.GET.get('sort', 'pret')
    if sort_param == 'a':
        produse =produse.order_by('pret')
    elif sort_param == 'd':
        produse =produse.order_by('-pret')
        
    paginator =Paginator(produse, items_per_page)
    page_number =request.GET.get('page')
    try: 
        page_obj=paginator.get_page(page_number)
    except Exception:
        page_obj=paginator.get_page(1)
    context ={
        'filter_form': filter_form,
        'page_obj': page_obj,
        'categorie_selectata': categorie_selectata,
        'repaginare_warning': repaginare_warning,
        'sort': sort_param,
        

    }     
    return render(request, 'Magazin_de_muzica/produse.html', context)



#lab 5 task 2 ex 4 


def calculate_age_months(birth_date):
    """Calculează vârsta exactă în format 'X ani și Y luni'."""
    today = date.today()
    
    years = today.year - birth_date.year
    
    months = today.month - birth_date.month
    
    if today.day < birth_date.day:
        months -= 1
        
    if months < 0:
        months += 12
        years -= 1
        
    return f"{years} ani și {months} luni"


def preprocess_message_text(text):
    """
    Înlocuiește linii noi cu spații, comasează spațiile multiple 
    și capitalizează literele de după terminatorii de frază.
    """
    
    # 1. Linii noi -> Spații
    text = text.replace('\n', ' ').replace('\r', ' ')
    
    # 2. Comasare spații multiple într-unul singur
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 3. Capitalizare după terminatori de frază (".", "?", "!", "...")
    def capitalize_match(match):
        # Grupul 1: terminatorul; Grupul 2: spațiile; Grupul 3: litera mică
        return match.group(1) + match.group(2) + match.group(3).upper()

    # Pattern: [Terminatori de frază] + [spații] + [literă mică]
    text = re.sub(r'([.?!]|\.\.\.)(\s*)([a-z])', capitalize_match, text)
    
    return text


def get_min_zile_asteptare_cerut(tip_mesaj):
    """Returnează minimul de zile de așteptare cerut de regulile de validare."""
    if tip_mesaj in ['review', 'cerere']:
        return 4
    elif tip_mesaj == 'intrebare':
        return 2
    else:
        
        return 1


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            
            data_nastere = data.pop('data_nastere')
            
            data['varsta_ani_luni'] = calculate_age_months(data_nastere)
            
            data['mesaj'] = preprocess_message_text(data['mesaj'])
            
            
            tip_mesaj = data['tip_mesaj']
            zile_asteptare_utilizator = data['min_zile_asteptare']
            
            min_cerut = get_min_zile_asteptare_cerut(tip_mesaj)
            

            is_urgent = (zile_asteptare_utilizator == min_cerut)
            data['urgent'] = is_urgent 

            data.pop('confirmare_email', None) 

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_utilizator = x_forwarded_for.split(',')[0]
            else:
                ip_utilizator = request.META.get('REMOTE_ADDR')
    
            data_ora_sosire = datetime.now()

            data['ip_utilizator'] = ip_utilizator
            data['data_ora_sosire'] = data_ora_sosire.strftime("%Y-%m-%d %H:%M:%S")



            save_dir = os.path.join(settings.BASE_DIR, 'Mesaje')
            os.makedirs(save_dir, exist_ok=True) 


            timestamp = int(time.time()) 


            urgent_tag = "_urgent" if is_urgent else ""
            nume_fisier = f"mesaj_{timestamp}{urgent_tag}.json"
            file_path = os.path.join(save_dir, nume_fisier) 


            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
    
                messages.success(request, f"Mesajul a fost trimis cu succes! Fișier JSON salvat ca: {nume_fisier}")
    
            except Exception as e:
                messages.error(request, f"A apărut o eroare la salvarea fișierului JSON: {e}")
    else:
        form =ContactForm()
    return render(request, 'Magazin_de_muzica/contact.html', {'form': form})



#lab 5 tesk 3 

from .forms import ProdusForm 

def introducere_produs(request):
    # 1. GESTIONAREA DATELOR TRIMISE (POST)
    if request.method == 'POST':
        # Instanțierea formularului cu datele trimise de utilizator
        form = ProdusForm(request.POST, request.FILES) 
        
        # 2. RULAREA VALIDĂRILOR
        if form.is_valid():
            try:
                # 3. SALVAREA OBIECTULUI
                # Apelarea metodei save() din formular, care include logica cu commit=False,
                # calcularea prețului final, setarea descrierii, și salvarea finală în baza de date.
                produs = form.save(commit=True) 
                
                # 4. REDIRECȚIONARE DUPĂ SUCCES
                # Exemplu: Redirecționare către o pagină de succes sau o listă de produse.
                return redirect(reverse('lista_produse')) 

            except Exception as e:
                # Gestiune de erori la salvarea efectivă în baza de date (dacă există)
                print(f"Eroare la salvarea produsului: {e}")
                # Poți adăuga un mesaj de eroare formularului
                form.add_error(None, "A apărut o eroare la salvarea în baza de date.")
    
    # 5. GESTIONAREA CERERILOR NOI (GET)
    else:
        # Instanțierea unui formular gol pentru afișare
        form = ProdusForm() 

    # 6. AFIȘAREA FORMULARULUI
    context = {
        'form': form,
        'titlu': 'Adaugă un Produs Nou'
    }
    return render(request, 'Magazin_de_muzica/adaugare_produs.html', context)

