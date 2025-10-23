from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from urllib.parse import urlparse
from collections import Counter

from .models import Produs


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


#functie ajutatoare pentru laborator 2

def salvare_accesari(request,nume_pagina):
    a = Accesare(
        ip_client =request.META.get("REMOTE_ADDR"), #pentru a lua ip-ul din dictionar
        url= request.build_absolute_uri(), #se construieste adresa completa a paginii accesate_
        data= datetime.now(),
        pagina_nume=nume_pagina
    )
    accesari.append(a)

###########################laborator 1 tema 

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

def info(request):
    salvare_accesari(request, "pagina info")
    parametru = request.GET.get("data") 
    afisat = ""
    
    if parametru:
        afisat = afis_data(parametru)
        
    # sectiunea parametri
    
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
        
    return HttpResponse(f"""
        <html>
        <head><title>Informatii despre server</title></head>
        <body>
        <h1>Informatii despre server</h1>  
        {afisat}
        {sectiune_parametri}
        </body>
        </html>
    """)

# FUNCTIE PENTRU TESTAREA CLASEI ACCESARE LABORATOR 1

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





##########LABORATOR 2 EXERCITI

def afis_template(request):
    return render(request, "Magazin_de_muzica/exemplu.html", {"nume": "Nume Paragraf"})

################################LABORATOR 2 TEMA

# Functia log 

def log(request):
    salvare_accesari(request, "log")

    # accesari=nr sau detalii
    
    nr_accesari = request.GET.get("accesari")
    
    if nr_accesari:
        if nr_accesari.lower() == "nr":
            total = len(accesari)
            return HttpResponse(f"<h2>Numarul total de accesari curente este {total}.</h2>")
        elif nr_accesari.lower() == "detalii":
            de_afisat = "<h1>Detalii accesari:</h1><ul>"
            for a in accesari:
                de_afisat += f"<li>ID {a.id} — Pagina: {a.pagina()} — Data: {a.data_formatata()}</li>"
            de_afisat += "</ul>"
            return HttpResponse(de_afisat)

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

        de_afisat = "<h1>Accesari dupa id-uri:</h1><ul>"
        for id_ in lista_id_finala:
            try:
                idx = int(id_) - 1
                de_afisat += f"<li>{accesari[idx].pagina()}</li>"
            except (ValueError, IndexError):
                de_afisat += f"<li>ID invalid: {id_}</li>"
        de_afisat += "</ul>"
        return HttpResponse(de_afisat)

    # tabelul 
    
    parametru_tabel = request.GET.get("tabel")
    if parametru_tabel:
        proprietati = [p.strip() for p in parametru_tabel.split(',')]
        if "tot" in proprietati:
            proprietati = ["id", "ip_client", "url", "data"]

        de_afisat = "<h1>Accesari in tabel:</h1><table border='1'><tr>"
        for prop in proprietati:
            de_afisat += f"<th>{prop}</th>"
        de_afisat += "</tr>"

        for a in accesari:
            de_afisat += "<tr>"
            for prop in proprietati:
                valoare = getattr(a, prop, "N/A")
                if prop == "data" and valoare:
                    valoare = a.data_formatata()
                elif callable(valoare):
                    valoare = valoare()
                de_afisat += f"<td>{valoare}</td>"
            de_afisat += "</tr>"
        de_afisat += "</table>"

        # Frecventa 
        
        frecventa = Counter([a.pagina() for a in accesari])
        if frecventa:
            pagina_max= max(frecventa, key=frecventa.get)
            pagina_min= min(frecventa, key=frecventa.get)
            de_afisat += f"<p>Cea mai accesata pagina: <b>{pagina_max}</b></p>"
            de_afisat += f"<p>Cea mai putin accesata pagina: <b>{pagina_min}</b></p>"

        return HttpResponse(de_afisat)

    #ultimele
    
    ultimele_accesari = request.GET.get("ultimele")
    if ultimele_accesari is None:
        
        de_afisat = "<h1>Toate accesarile:</h1><ul>"
        for a in accesari:
            de_afisat += f"<li>{a.pagina()}</li>"
        de_afisat += "</ul>"
    else:
        try:
            n = int(ultimele_accesari)
            if n < 0:
                raise ValueError
        except ValueError:
            return HttpResponse("<h2 style='color:purple'>Mesaj de eroare: parametrul nu este un numar intreg pozitiv</h2>")

        total_accesari = len(accesari)
        if n > total_accesari:
            de_afisat = "<h1>Toate accesarile:</h1><ul>"
            for a in accesari:
                de_afisat += f"<li>{a.pagina()}</li>"
            de_afisat += f"</ul><p style='color:red'>Exista doar {total_accesari} fata de {n} accesari cerute.</p>"
        else:
            de_afisat = f"<h1>Ultimele {n} accesari sunt:</h1><ul>"
            for a in accesari[-n:]:
                de_afisat += f"<li>{a.pagina()}</li>"
            de_afisat += "</ul>"

    return HttpResponse(de_afisat)


#afisarea produselor pentru utilizatori

def afis_produse(request):
    produse=Produs.objects.all()
    return render(request, "Magazin_de_muzica/produse.html",
        {          
            "produse": produse[0], 
        }
    )
    
