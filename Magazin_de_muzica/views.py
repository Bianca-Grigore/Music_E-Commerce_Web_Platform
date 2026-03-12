
import json
import os
import re
import time
import uuid
from collections import Counter
from datetime import date, datetime
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, mail_admins, send_mail, send_mass_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
import django.forms as forms

from .forms import (
    ContactForm, 
    CustomAuthenticationForm, 
    ProductFilterForm,
    ProdusForm, 
    ProfilUserCreationForm, 
    PromotiiForm
)
from .models import (
    Artist, 
    Campanie_Promo, 
    Categorie, 
    Produs,
    Produs_Artist, 
    Profil, 
    Promotii, 
    Vizualizare
)

import logging
logger = logging.getLogger('django')

accesari = []

def trimite_alerta_admin(subiect, mesaj_text, mesaj_html_body):
    html_content = f'<h1 style="color: red;">{subiect}</h1>'
    html_content += f"<div>{mesaj_html_body}</div>"
    
    mail_admins(
        subject=subiect,
        message=mesaj_text,
        html_message=html_content, 
        fail_silently=False
    )

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
    is_admin_site = request.user.groups.filter(name='Administratori_site').exists()

    if not is_admin_site:
        
        counter = request.session.get('counter_403', 0)
        counter += 1
        request.session['counter_403'] = counter
        
        context_error = {
            'titlu': 'Acces Interzis',
            'mesaj_personalizat': 'Doar administratorii site-ului pot vedea pagina info.',
            'counter': counter,
            'n_max': getattr(settings, 'N_MAX_403', 5),
        }
        return HttpResponseForbidden(render(request, 'Magazin_de_muzica/eroare_403.html', context_error))

    else: 
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


def log(request):
    is_admin_site = request.user.groups.filter(name='Administratori_site').exists()

    if not is_admin_site:
        
        counter = request.session.get('counter_403', 0)
        counter += 1
        request.session['counter_403'] = counter
        
        context_error = {
            'titlu': 'Acces Interzis',
            'mesaj_personalizat': 'Doar administratorii site-ului pot vedea log-urile.',
            'counter': counter,
            'n_max': getattr(settings, 'N_MAX_403', 5),
        }
        return HttpResponseForbidden(render(request, 'Magazin_de_muzica/eroare_403.html', context_error))
    else :
        salvare_accesari(request, "log")

        continut = ""
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

            frecventa = Counter([a.pagina() for a in accesari])
            if frecventa:
                pagina_max = max(frecventa, key=frecventa.get)
                pagina_min = min(frecventa, key=frecventa.get)
                continut += f"<p>Cea mai accesata pagina: <b>{pagina_max}</b></p>"
                continut += f"<p>Cea mai putin accesata pagina: <b>{pagina_min}</b></p>"

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

def afis_produse(request):
    salvare_accesari(request, "Pagina produselor")

    logger.debug(f"DEBUG: S-a accesat lista de produse. IP User: {get_client_ip(request)}")
    messages.debug(request, "DEBUG: S-a accesat view-ul simplu 'afis_produse'.")

    produse = Produs.objects.all()
    context = {"produse": produse[0]} if produse.exists() else {"produse": None}
    return render(request, "Magazin_de_muzica/produse.html", context)

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

def cos_virtual(request):
    salvare_accesari(request, "Pagina cosului virtual")
    context = {'user_ip': get_client_ip(request)}
    return render(request, "Magazin_de_muzica/in_lucru.html", context)


def in_lucru(request):
    salvare_accesari(request, "Pagina in lucru")

    logger.info(f"INFO: Utilizator (IP: {get_client_ip(request)}) a accesat o pagină 'În Lucru'.")

    messages.info(request, "Această funcționalitate este momentan în dezvoltare. Te rugăm să revii mai târziu!")
    
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

    logger.debug(f"DEBUG: Detalii solicitate pentru produsul ID={produs_id} ({produs.denumire})")

    messages.debug(request, f"DEBUG: Se vizualizează detaliile pentru produsul ID: {produs_id}")
    
    if request.user.is_authenticated:

        Vizualizare.objects.update_or_create(
            utilizator=request.user,
            produs=produs
        )

        ultimele_ids = Vizualizare.objects.filter(
            utilizator=request.user
        ).order_by('-data_vizualizarii').values_list('id', flat=True)[:5]


        Vizualizare.objects.filter(
            utilizator=request.user
        ).exclude(id__in=ultimele_ids).delete()


    produs_artist = get_object_or_404(Produs_Artist, produs=produs)
    campanii = Campanie_Promo.objects.filter(produs=produs)
    return render(request, 'Magazin_de_muzica/Detalii_produs.html', {
        'produs': produs,
        'produs_artist': produs_artist,
        'campanii': campanii
    })

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



    if request.GET and not page_obj.object_list:

        logger.warning(f"WARNING: Filtrare fara rezultate. Parametrii: {request.GET}")

        messages.warning(request, "Nu au fost găsite produse care să corespundă filtrelor selectate.") 


    context ={
        'filter_form': filter_form,
        'page_obj': page_obj,
        'categorie_selectata': categorie_selectata,
        'repaginare_warning': repaginare_warning,
        'sort': sort_param,
    }    
    return render(request, 'Magazin_de_muzica/produse.html', context)

def calculate_age_months(birth_date):
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
    
    text = text.replace('\n', ' ').replace('\r', ' ')
    

    text = re.sub(r'\s+', ' ', text).strip()
    
    
    def capitalize_match(match):
        
        return match.group(1) + match.group(2) + match.group(3).upper()

    
    text = re.sub(r'([.?!]|\.\.\.)(\s*)([a-z])', capitalize_match, text)
    
    return text

def get_min_zile_asteptare_cerut(tip_mesaj):
    
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
                logger.error(f"ERROR: Nu s-a putut salva mesajul de contact in JSON. Eroare: {e}")

                messages.error(request, f"A apărut o eroare la salvarea fișierului JSON: {e}")
    else:
        form =ContactForm()
    return render(request, 'Magazin_de_muzica/contact.html', {'form': form})

def introducere_produs(request):
    if not request.user.has_perm('Magazin_de_muzica.add_produs'):

        counter = request.session.get('counter_403', 0)
        counter += 1
        request.session['counter_403'] = counter
        context_error = {
            'titlu': 'Eroare adaugare produse',
            'mesaj_personalizat': 'Nu ai voie să adaugi produse muzicale', 
            'counter': counter,
            'n_max': getattr(settings, 'N_MAX_403', 5),
        }
        return HttpResponseForbidden(render(request, 'Magazin_de_muzica/eroare_403.html', context_error))

    if request.method == 'POST':
        form = ProdusForm(request.POST, request.FILES) 
        if form.is_valid():
            try:
                produs = form.save(commit=True) 

                messages.success(request, f"Produsul '{produs.denumire}' a fost adăugat cu succes în baza de date!")
                return redirect(reverse('lista_produse')) 

            except Exception as e:
                print(f"Eroare la salvarea produsului: {e}")

                logger.error(f"ERROR: Esec salvare produs in DB. Detalii: {e}")

                messages.error(request, "A apărut o eroare critică la salvarea în baza de date.")
        else:

            messages.error(request, "Formularul conține erori. Verifică datele introduse.")
    else:
        form = ProdusForm() 

    context = {
        'form': form,
        'titlu': 'Adaugă un Produs Nou'
    }
    return render(request, 'Magazin_de_muzica/adaugare_produs.html', context)

def register_view(request):
    if request.method == 'POST':
        form = ProfilUserCreationForm(request.POST)
        username_input = request.POST.get('username', '').lower()
        email_input = request.POST.get('email', '')
        if username_input == 'bianca':
            subiect = "cineva incearca sa ne preia site-ul"
            mesaj_text = f"Email utilizat: {email_input}"
            detalii_html = f"<p>O tentativă de înregistrare cu userul 'admin' a fost detectată.</p><p>Email: {email_input}</p>"
            trimite_alerta_admin(subiect, mesaj_text, detalii_html)
            messages.error(request, "Acest username este interzis.")
            return render(request, 'Magazin_de_muzica/inregistrare.html', {'form': form})
        if form.is_valid():
            user = form.save()
            cod_unic = str(uuid.uuid4())
            if hasattr(user, 'profil'):
                user.profil.cod = cod_unic
                user.profil.email_confirmat = False 
                user.profil.save()
            else:
                Profil.objects.create(user=user, cod=cod_unic, email_confirmat=False)
            obj_site=Site.objects.get_current()
            domeniu=obj_site.domain
            url_imagine = f"http://{domeniu}{settings.STATIC_URL}imagini/Music.jpg"
            link_confirmare= f"http://{domeniu}/Magazin_de_muzica/confirma_mail/{cod_unic}/"
            context = {
                'nume': user.first_name,
                'prenume': user.last_name,
                'username': user.username,
                'link_confirmare': link_confirmare,
                'url_imagine': url_imagine,
            }
            html_message = render_to_string('email/confirmare_email.html', context)
            plain_message = strip_tags(html_message)
            send_mail(
                subject='Confirmare Adresă de E-mail',
                message=plain_message,
                from_email='biancagrigore208@gmail.com', 
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, 'Cont creat. Verifică-ți e-mailul pentru a-l confirma!')
            return redirect('login') 
    else:

        logger.info("INFO: Formularul de înregistrare a fost afișat unui vizitator.")

        messages.info(request, "Pentru siguranță, alege o parolă complexă și un email valid.")

        form = ProfilUserCreationForm()
    
    return render(request, 'Magazin_de_muzica/inregistrare.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)

        if form.is_valid():
            user = form.get_user()

            if user is not None:

                if hasattr(user, 'profil') and user.profil.blocat:
                    messages.error(request, "Contul tău a fost blocat. Contactează un administrator.")
                    return redirect('login')



                if hasattr(user, 'profil') and not user.profil.email_confirmat:
                    messages.error(request, 'Trebuie să-ți confirmi adresa de e-mail înainte de a te loga.')
                    return redirect('login') 


                if 'failed_login_attempts' in request.session:
                    del request.session['failed_login_attempts']


                login(request, user)

                request.session['username'] = user.username
                request.session['email'] = user.email
                request.session['first_name'] = user.first_name
                request.session['last_name'] = user.last_name

                try:
                    profil = user.profil 
                    request.session['telefon'] = profil.telefon
                    request.session['tara'] = profil.tara
                    request.session['judet'] = profil.judet
                    request.session['oras'] = profil.oras
                    request.session['strada'] = profil.strada
                except Profil.DoesNotExist:
                    pass 

                if form.cleaned_data.get('ramane_logat'):
                    request.session.set_expiry(24*60*60) 
                else:
                    request.session.set_expiry(0) 

                return redirect('profil')


        else:
            username_incercat = request.POST.get('username', 'necunoscut')
            ip = request.META.get('REMOTE_ADDR')
            acum = time.time()


            attempts = request.session.get('failed_login_attempts', [])


            attempts = [t for t in attempts if t > acum - 120]


            attempts.append(acum)
            request.session['failed_login_attempts'] = attempts


            if len(attempts) >= 3:
                subiect = "Logari suspecte"

                logger.critical(f"CRITICAL: POSIBIL ATAC. User: {username_incercat}, IP: {ip}")

                mesaj_text = f"Userul '{username_incercat}' a încercat să se logheze de 3 ori rapid de pe IP: {ip}"
                
                detalii_html = f"""
                    <p>S-au detectat încercări multiple de autentificare eșuate.</p>
                    <ul>
                        <li><strong>Username vizat:</strong> {username_incercat}</li>
                        <li><strong>IP Atacator:</strong> {ip}</li>
                        <li><strong>Număr încercări (ultimele 2 min):</strong> {len(attempts)}</li>
                    </ul>
                """


                trimite_alerta_admin(subiect, mesaj_text, detalii_html)


                request.session['failed_login_attempts'] = [] 

            messages.error(request, "Nume de utilizator sau parolă incorectă.")


    else:
        form = CustomAuthenticationForm()

    return render(request, 'Magazin_de_muzica/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def pagina_profil_view(request):

    context = {
        'username': request.session.get('username', 'N/A'),
        'email': request.session.get('email', 'N/A'),
        'first_name': request.session.get('first_name', 'N/A'),
        'last_name': request.session.get('last_name', 'N/A'),
        'telefon': request.session.get('telefon', 'N/A'),
        'tara': request.session.get('tara', 'N/A'),
        'judet': request.session.get('judet', 'N/A'),
        'oras': request.session.get('oras', 'N/A'),
        'strada': request.session.get('strada', 'N/A'),
    }
    
    return render(request, 'Magazin_de_muzica/profil.html', context)

def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user) 
            messages.success(request, 'Parola a fost actualizata')
            return redirect('profil') 
        else:
            messages.error(request, 'Exista erori.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'Magazin_de_muzica/schimba_parola.html', {'form': form})

def confirma_email_view(request, cod):
    try: 
        profil = get_object_or_404(Profil, cod=cod)
        if profil.email_confirmat:
            logger.warning(f"WARNING: Tentativă repetată de confirmare email pentru codul: {cod}")

            messages.warning(request, 'Adresa de e-mail a fost deja confirmată.')
        else:
            profil.email_confirmat = True
            profil.save()
            messages.success(request, 'Adresa de e-mail a fost confirmată cu succes! Te poți loga.')  
    except Exception as e:
        messages.error(request, 'Link de confirmare invalid.')
    return redirect('login')

def pagina_promotii(request):
    if request.method == 'POST':
        form = PromotiiForm(request.POST)
        if form.is_valid():
            promotie = form.save()
            categorii_alese = form.cleaned_data['categorii']
            K = 2 
            datatuple = [] 
            template_map = {
                'CD Rock': 'Magazin_de_muzica/email_promo_rock.txt',
                'CD Pop': 'Magazin_de_muzica/email_promo_pop.txt',
            }
            for categorie in categorii_alese:
                useri_targetati = User.objects.filter(
                    vizualizare__produs__categorie=categorie
                ).annotate(
                    nr_vizualizari=Count('vizualizare')
                ).filter(nr_vizualizari__gte=K).distinct()
                nume_cat = categorie.nume_categorie
                fisier_template = template_map.get(nume_cat, 'Magazin_de_muzica/email_promo_pop.txt')
                for user in useri_targetati:
                    context = {
                        'subiect': promotie.subiect_email,
                        'nume_promotie': promotie.nume,
                        'nume_categorie': nume_cat,
                        'data_expirare': promotie.data_expirare.strftime('%d-%m-%Y'),
                        'procent': promotie.procent_reducere,
                        'mesaj_extra': form.cleaned_data['mesaj'] 
                    }
                    mesaj_text = render_to_string(fisier_template, context)
                    email_obj = (
                        promotie.subiect_email,
                        mesaj_text,
                        'biancagrigore208@gmail.com',
                        [user.email]
                    )
                    datatuple.append(email_obj)
            try:
                if datatuple:
                    send_mass_mail(tuple(datatuple), fail_silently=False)
                    messages.success(request, f"Promoția a fost salvată și au fost trimise {len(datatuple)} mailuri!")
                else:
                    messages.warning(request, "Promoția a fost salvată, dar niciun user nu a îndeplinit condiția K vizualizări.")
            except Exception as e:
                subiect_eroare = "Eroare Trimitere Promotii"

                logger.critical(f"CRITICAL: Serviciul de Email Mass-Mail a esuat total! Eroare: {e}")

                eroare_str = str(e)
                mesaj_text_admin = f"A apărut o eroare la send_mass_mail: {eroare_str}"
                html_eroare = f"""
                <p>A apărut o excepție în timpul trimiterii promoțiilor:</p>
                <div style="background-color: red; color: white; padding: 15px; border-radius: 5px; font-family: monospace;">
                    <strong>Detalii eroare:</strong><br>
                    {eroare_str}
                </div>
                """
                trimite_alerta_admin(subiect_eroare, mesaj_text_admin, html_eroare)
                messages.error(request, "A apărut o eroare tehnică la trimiterea email-urilor. Administratorii au fost notificați.")
            return redirect('pagina_promotii')
    else:
        form = PromotiiForm()
    return render(request, 'Magazin_de_muzica/promotii.html', {'form': form})

@login_required
def revendica_oferta(request):
    permisiune = Permission.objects.get(codename='vizualizeaza_oferta')
    request.user.user_permissions.add(permisiune)
    return redirect('pagina_oferta')


def afisare_oferta(request):

    if not request.user.has_perm('Magazin_de_muzica.vizualizeaza_oferta'):
        
        counter = request.session.get('counter_403', 0) + 1
        request.session['counter_403'] = counter
        
        context_error = {
            'titlu': 'Eroare afisare oferta',
            'mesaj_personalizat': 'Nu ai voie să vizualizezi oferta',
            'counter': counter,
            'n_max': getattr(settings, 'N_MAX_403', 5),
        }

        return HttpResponseForbidden(render(request, 'Magazin_de_muzica/eroare_403.html', context_error))

    return render(request, 'Magazin_de_muzica/oferta-speciala.html')

def custom_logout(request):
    if request.user.is_authenticated:
        try:
            permisiune = Permission.objects.get(codename='vizualizeaza_oferta')
            request.user.user_permissions.remove(permisiune)
            print(f"Permisiunea a fost ștearsă pentru {request.user.username}")
            
        except Permission.DoesNotExist:
            pass 
    logout(request)
    return redirect('login') 


# def setup_permisiune(request):
#     content_type = ContentType.objects.get_for_model(Produs)
#     perm, created = Permission.objects.get_or_create(
#         codename='vizualizeaza_oferta',
#         defaults={
#             'name': 'Poate vizualiza oferta speciala',
#             'content_type': content_type
#         }
#     )
    
#     if created:
#         return HttpResponse("Succes! Permisiunea a fost creată.")
#     else:
#         return HttpResponse("Permisiunea exista deja.")

def vizualizare_produs(request, pk):
    produs = get_object_or_404(Produs, pk=pk)
    return render(request, 'Magazin_de_muzica/Detalii_produs.html', {'produs': produs})

def produse_dupa_categorie(request, nume_categorie):
    categorie = get_object_or_404(Categorie, nume_categorie=nume_categorie)
    produse = Produs.objects.filter(categorie=categorie)
    return render(request, 'Magazin_de_muzica/produse_categorie.html', {'categorie': categorie, 'produse': produse})

def detalii_artist(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    return render(request, 'Magazin_de_muzica/detaliu_artist.html', {'artist': artist})

def detalii_campanie(request, pk):
    campanie = get_object_or_404(Campanie_Promo, pk=pk)
    produse = campanie.produs_set.all() 
    return render(request, 'Magazin_de_muzica/detaliu_campanie.html', {'campanie': campanie, 'produse': produse})
