import os #variabile de mediu

from django.core.files import File
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "magazin_muzica.settings")
django.setup() 
from Magazin_de_muzica.models import Categorie, Campanie_Promo, Artist, Produs, Produs_Artist
from django.utils import timezone
from datetime import date

categorie1=Categorie.objects.create(nume_categorie='CD Pop', tip_categorie='C')
categorie2=Categorie.objects.create(nume_categorie='CD Rock', tip_categorie='C')
categorie3=Categorie.objects.create(nume_categorie='CD Country', tip_categorie='C')
categorie4=Categorie.objects.create(nume_categorie='Vinyl Pop', tip_categorie='V')
categorie5=Categorie.objects.create(nume_categorie='Vinyl Rock', tip_categorie='V')
categorie6=Categorie.objects.create(nume_categorie='Vinyl Hip-Hop', tip_categorie='V')
categorie7=Categorie.objects.create(nume_categorie='Caseta Pop', tip_categorie='K')
categorie8=Categorie.objects.create(nume_categorie='Caseta Rock', tip_categorie='K')
categorie9=Categorie.objects.create(nume_categorie='Casete Anii 90', tip_categorie='K')
categorie10=Categorie.objects.create(nume_categorie='Casete Anii 80', tip_categorie='K')
categorie11=Categorie.objects.create(nume_categorie='Casete Anii 70', tip_categorie='K')
categorie12=Categorie.objects.create(nume_categorie='Tricouri', tip_categorie='M')
categorie13=Categorie.objects.create(nume_categorie='Postere', tip_categorie='M')
categorie14=Categorie.objects.create(nume_categorie='Figurine', tip_categorie='M')
categorie15=Categorie.objects.create(nume_categorie='Breloc', tip_categorie='M')

c1=Campanie_Promo.objects.create(
    nume_campanie="Reducere Craciun",
    tip_campanie='S',
    reducere=20.0,
    data_sfarsit=date(2025, 12, 31)
)

c2=Campanie_Promo.objects.create(
    nume_campanie="Black Friday 2025",
    tip_campanie='B',
    reducere=50.0,
    data_sfarsit=date(2025, 11, 30)
)

c3=Campanie_Promo.objects.create(
    nume_campanie="Flash Sale Pop",
    tip_campanie='F',
    reducere=15.0,
    data_sfarsit=date(2025, 10, 25)
)

c4=Campanie_Promo.objects.create(
    nume_campanie="Reducere Vara",
    tip_campanie='S',
    reducere=10.0,
    data_sfarsit=date(2025, 8, 31)
)

c5=Campanie_Promo.objects.create(
    nume_campanie="Flash Sale Rock",
    tip_campanie='F',
    reducere=25.0,
    data_sfarsit=date(2025, 10, 28)
)

produs1 = Produs.objects.create(
    denumire="The Life of A Showgirl",
    categorie=categorie1,
    pret=100,
    stoc=100,
    data_adaugare=timezone.now()
)
produs1.campanii.add(c2)

produs2 = Produs.objects.create(
    denumire="Speak Now (Taylor's Version)",
    categorie=categorie1,
    pret=50,
    stoc=87,
    data_adaugare=timezone.now()
)
produs2.campanii.add(c1)

produs3 = Produs.objects.create(
    denumire="Death or Glory",
    categorie=categorie2,
    pret=75,
    stoc=120,
    data_adaugare=timezone.now()
)
produs3.campanii.add(c2)

produs4 = Produs.objects.create(
    denumire="The Tortured Poets Department",
    categorie=categorie4,
    pret=280,
    stoc=190,
    data_adaugare=timezone.now()
)
produs4.campanii.add(c3)

produs5 = Produs.objects.create(
    denumire="Taylor Swift-Debut",
    categorie=categorie3,
    pret=64,
    stoc=87,
    data_adaugare=timezone.now()
)
produs5.campanii.add(c3)

produs6 = Produs.objects.create(
    denumire="The Bastards",
    categorie=categorie5,
    pret=200,
    stoc=162,
    data_adaugare=timezone.now()
)
produs6.campanii.add(c1)

produs7 = Produs.objects.create(
    denumire="In Search Of The Antidote",
    categorie=categorie7,
    pret=123,
    stoc=54,
    data_adaugare=timezone.now()
)
produs7.campanii.add(c5)

produs8 = Produs.objects.create(
    denumire="Lotus T-Shirt",
    categorie=categorie12,
    pret=150,
    stoc=300,
    data_adaugare=timezone.now()
)
produs8.campanii.add(c3)

produs9 = Produs.objects.create(
    denumire="Father Figure T-Shirt",
    categorie=categorie12,
    pret=290,
    stoc=267,
    data_adaugare=timezone.now()
)
produs9.campanii.add(c1)

produs10 = Produs.objects.create(
    denumire="Eat Your Young - Breloc",
    categorie=categorie15,
    pret=30,
    stoc=124,
    data_adaugare=timezone.now()
)
produs10.campanii.add(c4)

a1=Artist.objects.create(
    nume= "Taylor Swift",
    gen_muzical="pop",
    ani_activitate=21,
    tip_activitate='S',
)

a2=Artist.objects.create(
    nume= "Palaye Royale",
    gen_muzical="rock",
    ani_activitate=10,
    tip_activitate='B',
)

a3=Artist.objects.create(
    nume= "Fletcher",
    gen_muzical="pop",
    ani_activitate=4,
    tip_activitate='S',
)
a4=Artist.objects.create(
    nume= "Hozier",
    gen_muzical="pop",
    ani_activitate=11,
    tip_activitate='S',
)

a5=Artist.objects.create(
    nume= "Litle Smitz",
    gen_muzical="hip-hop",
    ani_activitate=10,
    tip_activitate='B',
)

pa1 = Produs_Artist.objects.create(
    produs=produs1,
    artist=a1,
    rol_artist="Vocal, scriitor principal.",
    tip_rol='S', 
    colaborare_speciala="feat. Sabrina Carpenter",  
    descriere="The Life of a Showgirl este al doisprezecelea album al cântăreței și compozitoarei americane Taylor Swift. A fost lansat pe 3 octombrie 2025 prin Republic Records. Swift a creat albumul în timpul turneului The Eras Tour, acesta conținând 12 piese.",
    data_adaugare=timezone.now()
)

pa2 = Produs_Artist.objects.create(
    produs=produs2,
    artist=a1,
    rol_artist="Vocal principal. Singurul scriitor al melodiilor.",
    tip_rol='S', 
    descriere="Speak Now (Taylor's Version) este al treilea album re-înregistrat al artistei Taylor Swift, lansat pe 7 iulie 2023. Este re-înregistrarea celui de-al treilea său album, Speak Now, lansat în 2010. Albumul a fost anunțat pe 5 mai 2023 la unul din concertele Turneului Eras. Swift a început procesul re-înregistrărilor după vânzarea drepturilor înregistrărilor celor prime 6 albume ale sale, cu scopul de a le deține ea însăși."
)

pa3 = Produs_Artist.objects.create(
    produs=produs3,
    artist=a2,
    rol_artist="Producator melodii si clipuri video.",
    tip_rol='P', 
    descriere="Death or Glory” este al cincilea album de studio al trupei Palaye Royale, lansat pe 30 august 2024 prin Sumerian Records. Cu un amestec de glam rock, art rock și alternative, albumul marchează o evoluție semnificativă în sound-ul trupei, combinând influențe clasice cu o energie modernă și o producție rafinată."
) 

pa4 = Produs_Artist.objects.create(
    produs=produs4,
    artist=a1,
    rol_artist="Scriitor si solist principal.",
    tip_rol='S', 
    descriere="The Tortured Poets Department” este al unsprezecelea album de studio al lui Taylor Swift, lansat pe 19 aprilie 2024. Este un proiect ambițios și introspectiv, care reflectă o perioadă de tranziție în viața și cariera sa. Într-un interviu din octombrie 2025, Swift a declarat că a fost „mizerabilă” în timpul procesului de scriere a albumului, considerându-l „artă frumoasă despre mizerie People.com.Ulterior, a lansat albumul „The Life of a Showgirl”, care reprezenta o schimbare stilistică față de „The Tortured Poets Department"
)

pa5 = Produs_Artist.objects.create(
    produs=produs5,
    artist=a1,
    rol_artist="Scriitor si solist principal.",
    tip_rol='S', 
    descriere="„Taylor Swift” este albumul de debut al cântăreței și compozitoarei americane Taylor Swift, lansat pe 24 octombrie 2006 de Big Machine Records. La vârsta de 16 ani, Swift a scris sau co-scris fiecare piesă de pe album, majoritatea în colaborare cu Liz Rose. Albumul a fost produs de Nathan Chapman și Robert Ellis Orrall și încorporează elemente de country cu influențe pop și pop-rock, fiind însoțit de aranjamente acustice cu chitare, banjo și vioară"
)

pa6 = Produs_Artist.objects.create(
    produs=produs6,
    artist=a2,
    rol_artist="Producator melodii si clipuri video.",
    tip_rol='P', 
    descriere="„The Bastards” este al treilea album de studio al trupei canadiano-americane Palaye Royale, lansat pe 29 mai 2020 de Sumerian Records. Acesta marchează o evoluție semnificativă în sound-ul și mesajul trupei, fiind un album conceptual cu teme sociale și politice puternice. Albumul este structurat în patru acte, fiecare reprezentând o eră diferită a unei societăți ipotetice care a trecut de la idealuri de libertate la o stare de opresiune politică și socială. Temele abordate includ sănătatea mintală, dependența de droguri, violența armată și critica față de visul american."
)

pa7 = Produs_Artist.objects.create(
    produs=produs7,
    artist=a3,
    rol_artist="Scriitoare, compozitoare si vocalista.",
    tip_rol='S', 
    descriere="„In Search of the Antidote” este al doilea album de studio al cântăreței și compozitoarei americane Fletcher, lansat pe 22 martie 2024 prin Capitol Records. Acest album marchează o evoluție semnificativă în cariera sa, explorând teme precum identitatea, ego-ul, nesiguranța și împlinirea personală, inspirate din căutarea sa pentru vindecare și sens prin iubire. Fletcher descrie proiectul ca fiind profund personal, modelat de introspecție nefiltrată și experiențele sale cu auto-reflecția și conexiunea."
)

pa8 = Produs_Artist.objects.create(
    produs=produs8,
    artist=a5,
    rol_artist=" ",
    tip_rol='P', 
    descriere="Tricoul este unul dintre articolele de merch ale trupei Little Simz din ultimul concert. ALbumul Lotus este al șaselea album de studio, lansat pe 6 iunie 2025 prin AWAL. Acesta marchează o schimbare semnificativă în cariera sa, fiind rezultatul unei perioade de introspecție profundă și de reconstrucție personală, după o dispută legală cu fostul său colaborator, Inflo."
)

pa9 = Produs_Artist.objects.create(
    produs=produs9,
    artist=a1,
    rol_artist="Designer",
    tip_rol='S', 
    descriere="Tricoul este cel mai vandut articol de merch din colectia albumului The Life of A Showgirl. Design-ul este realizat de catre Taylor si echipa sa de marketing."
)

pa10 = Produs_Artist.objects.create(
    produs=produs10,
    artist=a4,
    rol_artist=" ",
    tip_rol='P', 
    descriere="Breloc semnificativ fastuoasei melodii politice Eat Your Young care a avut un debut extraordinar inca din primele zile. „Eat Your Young” este o piesă pop-soul alternativă cu influențe de blues și folk, care abordează teme precum lăcomia, consumul excesiv și inegalitatea socială. Versurile evocă imagini puternice, comparând comportamentele distructive ale societății cu canibalismul, sugerând că cei aflați la putere „mănâncă” viitorul tinerelor generații pentru a-și satisface propriile dorințe. Această alegorie reflectă critica adusă sistemelor economice și politice care prioritizează profiturile în detrimentul bunăstării colective"
)