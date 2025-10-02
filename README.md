# OptDezAplWeb

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime

def afis_data(parametru):
    luni=['Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']
    zile=['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri', 'Sambata', 'Duminica']
    
    prezent=datetime.now()
    zi_saptamana=zile[prezent.weekday()]
    zi_luna=prezent.day
    nume_luna=luni[prezent.month-1]
    an=prezent.year 
    ora=prezent.strftime("%H:%M:%S")
    
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
	return HttpResponse("""
        <html>
        <body>
        <p><b>Descrierea proiectului</b></p>
        </body>
        </html>
        """
    )

def info(request):
    parametru=request.GET.get("data") 
    sectiune=""
    if parametru is not None:
        sectiune=afis_data(parametru)
    return HttpResponse(f"""
        <html>
        <head><title>Informatii despre server</title></head>
        <body>
        <h1>Informatii despre server</h1>  
        {sectiune}
        </body>
        </html>
        """
    )
