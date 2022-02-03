# 
# Program do statystyki ilości i rodzaju znaków
# @author: Miłosz Gajewski
# 
import xml.etree.ElementTree as Xet
import pandas as pd
import glob, os
import csv
# Typy znaków
Crosswalk = [] #crosswalk
Crosswalk_liczba = 0
Stop = [] #stop
Stop_liczba = 0
Speedlimit = [] #speedlimit
Speedlimit_liczba = 0
Trafic_light = [] #trafficlight
Trafic_light_liczba = 0
# Zapis do pliku
plik = open("Statystyka.txt",'a')
# Ścieżka do folderu
path = 'annotations/'
# Odczytywanie danych
for filename in glob.glob(os.path.join(path, '*.xml')):
   with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
        xmlparse = Xet.parse(f)
        root = xmlparse.getroot()
        File_name = xmlparse.find("filename").text
        for i in xmlparse.findall("object"):
            if(i):
                Name = i.find("name").text
        if(Name == "crosswalk"):
            Crosswalk_liczba += 1
            Crosswalk.append(File_name)
        elif(Name == "stop"):
            Stop.append(File_name)
            Stop_liczba += 1
        elif(Name == "speedlimit"):
            Speedlimit.append(File_name)
            Speedlimit_liczba += 1
        elif(Name == "trafficlight"):
            Trafic_light.append(File_name)
            Trafic_light_liczba += 1
# Wyświetlenie wyników:
print("Kategorie znaków:")
print("1.   Crosswalk       -   ilość: " + str(Crosswalk_liczba))
print("2.   Stop            -   ilość: " + str(Stop_liczba))
print("3.   Speedlimit      -   ilość: " + str(Speedlimit_liczba))
print("4.   Trafficlight    -   ilość: " + str(Trafic_light_liczba))
# Zapis do pliku
plik.write("Kategorie znakow:"+ "\n")
plik.write("1.   Crosswalk       -   ilosc: " + str(Crosswalk_liczba)+ "\n")
plik.write("2.   Stop            -   ilosc: " + str(Stop_liczba)+ "\n")
plik.write("3.   Speedlimit      -   ilosc: " + str(Speedlimit_liczba)+ "\n")
plik.write("4.   Trafficlight    -   ilosc: " + str(Trafic_light_liczba)+ "\n")
plik.write("\n" + "Crosswalk:"+ "\n")
for i in Crosswalk:
    plik.write(str(i) + "\n")
plik.write("\n" + "Stop:"+ "\n")
for i in Stop:
    plik.write(str(i) + "\n")
plik.write("\n" + "Speedlimit:"+ "\n")
for i in Speedlimit:
    plik.write(str(i) + "\n")
plik.write("\n"+"Trafic_light:"+ "\n")
for i in Trafic_light:
    plik.write(str(i) + "\n")
plik.close()