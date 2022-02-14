import shutil, os
from tracemalloc import start

original = r'./annotations_/'

target_test = r'./Test/annotations/'
target_train = r'./Train/annotations/'

crosswalk_train = 160
crosswalk_test = 40
Stop_train = 70
Stop_test = 21
Speedlimit_train = 625
Speedlimit_test = 783 - Speedlimit_train
Trafficlight_train = 135
Trafficlight_test = 170 - Trafficlight_train

plik_crosswalk = open("crosswalk_set.txt",'r')
plik_stop = open("stop_set.txt",'r')
plik_traffic = open("trafficlight_set.txt",'r')
plik_speedlimit = open("speedlimit_set.txt",'r')
liczba = 0
liczba_cal = 0
# Crosswalk
while liczba_cal <= (crosswalk_test + crosswalk_train-2):
    if plik_crosswalk.readable():
        tekst = repr(plik_crosswalk.readline())
        size = len(tekst)
        tekst = tekst[1:(size-3)]
        liczba += 1
        liczba_cal += 1
        if(liczba <= crosswalk_train):
            sciezka_cel = (target_train + tekst)
            sciezka_original = original + tekst
            shutil.copyfile(sciezka_original, sciezka_cel)
        else:
            sciezka_cel = target_test + tekst
            sciezka_original = original + tekst
            shutil.copyfile(os.path.join(original,tekst),os.path.join(target_test,tekst))
liczba = 0
liczba_cal = 0
# Stop
while liczba_cal <= (Stop_test + Stop_train-2):
    if plik_stop.readable():
        tekst = repr(plik_stop.readline())
        size = len(tekst)
        tekst = tekst[1:(size-3)]
        liczba += 1
        liczba_cal += 1
        if(liczba <= Stop_train):
            sciezka_cel = (target_train + tekst)
            sciezka_original = original + tekst
            shutil.copyfile(sciezka_original, sciezka_cel)
        else:
            sciezka_cel = target_test + tekst
            sciezka_original = original + tekst
            shutil.copyfile(os.path.join(original,tekst),os.path.join(target_test,tekst))
# Speedlimit
liczba = 0
liczba_cal = 0
while liczba_cal <= (Speedlimit_test + Speedlimit_train-2):
    if plik_speedlimit.readable():
        tekst = repr(plik_speedlimit.readline())
        size = len(tekst)
        tekst = tekst[1:(size-3)]
        liczba += 1
        liczba_cal += 1
        if(liczba <= Speedlimit_train):
            sciezka_cel = (target_train + tekst)
            sciezka_original = original + tekst
            shutil.copyfile(sciezka_original, sciezka_cel)
        else:
            sciezka_cel = target_test + tekst
            sciezka_original = original + tekst
            shutil.copyfile(os.path.join(original,tekst),os.path.join(target_test,tekst))
# traffic
liczba = 0
liczba_cal = 0
while liczba_cal <= (Trafficlight_test + Trafficlight_train-2):
    if plik_traffic.readable():
        tekst = repr(plik_traffic.readline())
        size = len(tekst)
        tekst = tekst[1:(size-3)]
        liczba += 1
        liczba_cal += 1
        if(liczba <= Trafficlight_train):
            sciezka_cel = (target_train + tekst)
            sciezka_original = original + tekst
            shutil.copyfile(sciezka_original, sciezka_cel)
        else:
            sciezka_cel = target_test + tekst
            sciezka_original = original + tekst
            shutil.copyfile(os.path.join(original,tekst),os.path.join(target_test,tekst))