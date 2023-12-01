import time
import threading
from datetime import datetime

def afficher_heure(mode_12h, pause_flag):
    global heure_a_afficher
    while not stop_flag.is_set():
        while pause_flag.is_set():
            time.sleep(1)
        heure = list(heure_a_afficher)
        if mode_12h:
            heure_str = convertir_12h(heure)
        else:
            heure_str = convertir_24h(heure)
        
        print(f"\r{heure_str.ljust(11)}: (OFF/P/S) : ", end='', flush=True)
        time.sleep(1) 
        heure = incrementer_heure(heure)
        heure_a_afficher = tuple(heure)

def regler_heure(pause_flag):
    pause_flag.set()
    new_hour = int(input("Entrez les heures : "))
    new_minute = int(input("Entrez les minutes : "))
    new_second = int(input("Entrez les secondes : "))
    heure = (new_hour, new_minute, new_second)
    pause_flag.clear()
    return heure


def incrementer_heure(heure):
    new_second = heure[2] + 1
    new_minute = heure[1]
    new_hour = heure[0]
    
    if new_second >= 60:
        new_second = 0
        new_minute += 1
        if new_minute >= 60:
            new_minute = 0
            new_hour += 1
            if new_hour >= 24:
                new_hour = 0
    
    return (new_hour, new_minute, new_second)

def arreter_actualisation():
    stop_flag.set()

def convertir_12h(heure):
    heure_str = time.strftime("%I:%M:%S %p", (2000, 1, 1, heure[0], heure[1], heure[2], 0, 0, -1))
    return heure_str

def convertir_24h(heure):
    return "{:02d}:{:02d}:{:02d}".format(heure[0], heure[1], heure[2])

stop_flag = threading.Event()
pause_flag = threading.Event() 

heure_actuelle = datetime.now().time()
heure_a_afficher = (heure_actuelle.hour, heure_actuelle.minute, heure_actuelle.second)
mode_12h = True  

heure_thread = threading.Thread(target=afficher_heure, args=(mode_12h, pause_flag))
heure_thread.start()

while True:
    action = input().upper().strip()
    if action == 'OFF':
        arreter_actualisation()
        heure_thread.join()
        break
    elif action == 'P':
        pause_flag.set()
        print("\rHorloge en pause. Appuyez sur 'R' pour reprendre.")
        reprendre = input().upper().strip()
        if reprendre == 'R':
            pause_flag.clear()
    elif action == 'S':
        heure_a_afficher = regler_heure(pause_flag)