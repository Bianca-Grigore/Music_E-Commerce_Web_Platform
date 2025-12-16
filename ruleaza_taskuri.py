import schedule
import time
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'magazin_muzica.settings')
django.setup()
from django.conf import settings
from Magazin_de_muzica import tasks
def run_scheduler():

    k = settings.TASK_K_MINUTES
    schedule.every(k).minutes.do(tasks.sterge_useri_neconfirmati)
    print(f"Task 1 programat: Stergere useri neconfirmați la fiecare {k} minute.")


    z = settings.TASK_NEWSLETTER_DAY.lower() 
    o = settings.TASK_NEWSLETTER_HOUR      


    job_newsletter = schedule.every()
    if z == 'monday': job_newsletter = job_newsletter.monday
    elif z == 'tuesday': job_newsletter = job_newsletter.tuesday
    elif z == 'wednesday': job_newsletter = job_newsletter.wednesday
    elif z == 'thursday': job_newsletter = job_newsletter.thursday
    elif z == 'friday': job_newsletter = job_newsletter.friday
    elif z == 'saturday': job_newsletter = job_newsletter.saturday
    elif z == 'sunday': job_newsletter = job_newsletter.sunday
    
    job_newsletter.at(o).do(tasks.trimite_newsletter)
    print(f"Task 2 programat: Newsletter in fiecare {z} la ora {o}.")


    m = settings.TASK_M_MINUTES
    schedule.every(m).minutes.do(tasks.verificare_stocuri_scazute)
    print(f"Task 3 programat: Verificare stocuri la fiecare {m} minute.")


    z2 = settings.TASK_Z2_DAY.lower()
    o2 = settings.TASK_O2_HOUR
    
    job_raport = schedule.every()
    if z2 == 'monday': job_raport = job_raport.monday
    elif z2 == 'tuesday': job_raport = job_raport.tuesday
    elif z2 == 'wednesday': job_raport = job_raport.wednesday
    elif z2 == 'thursday': job_raport = job_raport.thursday
    elif z2 == 'friday': job_raport = job_raport.friday
    elif z2 == 'saturday': job_raport = job_raport.saturday
    elif z2 == 'sunday': job_raport = job_raport.sunday

    job_raport.at(o2).do(tasks.raport_saptamanal_admin)
    print(f"Task 4 programat: Raport săptămânal în fiecare {z2} la ora {o2}.")


    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\nScheduler oprit manual.")
        sys.exit()