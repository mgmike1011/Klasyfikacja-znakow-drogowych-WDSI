# Wprowadzenie do sztucznej inteligencji - laboratorium
Projekt zaliczeniowy na przedmiot Wprowadzenie do sztucznej inteligencji - laboratorium. Autor: Miłosz Gajewski
### Cel projektu
Celem projektu było stworzenie oprogramowania dokonującego **klasyfikacji znaków drogowych** i wyświetlającego informacje na temat rozpoznanego znaku (znak typu Crosswalk lub inny).
## Przebieg prac
### Statystyka zbioru
Prace rozpocząłem od przygotowania trzech programów napisanych w języku Python, które obliczyły ilość znaków w bazie danych oraz posortowały informacje o nich.

1. [dataset_statistics.py](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/dataset_statistics.py) - program przygotowujący informacje na temat ilości danych znaków w zbiorze oraz grupujący nazwy zdjęć do odpowiednich kategorii znaków. Rodzaje znaków oraz ilość w zbiorze:

| Typ znaku   | Ilość           |
| ------------- |:-------------:|
| Crosswalk    | 200 |
| Stop         |91   |
| Speedlimit   |783  |
| Trafficlight |170  |

**Pełna statystyka:** [Statystyka_zbioru.txt](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/Statystyka_zbioru.txt) 

2. [xml_to_csv.py](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/xml_to_csv.py) - program konwertujący informacje zawarte w plikach .xml odpowiednich zdjęć z bazy danych do jednego pliku .csv zawierającego odpowiednie informacje.

**Wynikowy plik .csv:** [data.csv](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/data.csv)

3. [create_set.py](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/create_set.py) - program przygotowujący(rozdzielający) pliki pomiędzy folder Train oraz Test.

### Prgoram główny
Struktura samego programu, czyli kolejne realizowane kroki oparte są o program z zajęć laboratoryjnych.
#### Wczytanie danych 
Program rozpoczyna pracę od wczytania danych treningowych oraz testowych za pomocą funkcji load_data(), pobrane zostają pliki .xml z odpowiednio folderów Train/annotations – zbiór treningowy oraz Test/annotations – zbiór testowy, przy czym informacje ze zbioru testowego używane są w pełni do uczenia, a ze zbioru testowego jedynie wybrane takie jak nazwa pliku .png, oraz współrzędne obszaru występowania znaku na zdjęciu. Informacje zostają zapisane w postaci obiektów klasy Zdjęcie, w której występuje pole listy obiektów klasy Obiekt, w której to przechowywane są właściwe dane o znakach. Następnym etapem jest wyświetlanie statystyki załadowanych zbiorów, funkcja display_dataset_stats() wyświetla ilość obiektów na zdjęciach przynależących do klasy(z etykietą) „0”, które stanowią znak typu crosswalk oraz ilość obiektów należących do klasy „1” stanowiących znaki inne niż znaki przejścia dla pieszych. 
#### Działanie na zbiorze treningowym
Kolejnym etapem działania programu jest ekstrakcja cech w algorytmie BoVW (learn_bovw()), której wynikiem jest zapis słownika w postaci pliku voc.npy, dzieje się to oczywiście na zbiorze treningowym. Wykrywane zostają kluczowe punkty na zdjęciach za pomocą detektorów, w programie został użyty detektor SIFT. Zapisany słownik następnie używany jest w funkcji extract_features(), w której dla każdego znaku z bazy treningowej tworzony jest deskryptor (zapisywany jako jedno z pól w klasie Obiekt). Ostatnim etapem pracy ze zbiorem treningowym jest trenowanie w funkcji train(), której wynikiem jest powstanie modelu – deskryptory i odpowiadające im etykiety. W funckji train() użyty został mechanizm drzew decyzyjnych/klasyfikacyjnych - Random forest.
#### Działanie na zbiorze testowym
Kolejne etapy działania programu opierają się już o zbiór testowy. Prace rozpoczynają się od wywołania funkcji extract_features(), która tworzy deskryptory, ale już dla zbioru testowanego. Ostatnim etapem jest dokonanie właściwej klasyfikacji etykiet do zdjęć w zbiorze testowym. Funkcja predict(), która przyjmuje jako swoje argumenty wejściowe model oraz dane do klasyfikacji dokonuje predykcji etykiet danych i zapisuje ją do jednego z pól w klasie Obiekt. Kluczową linią jest: pred = rf.predict(sample_i.desc), jednak cała funkcja jest potrzebna, do zewaluowania całej bazy danych.
#### Wyświetlenie wyników
Ostatnim etapem jest wyświetlenie wyników, pierwsza wyświetlona zostaje ewaluacja wyników klasyfikacji (Accuracy = ile rzeczy model zaklasyfikował poprawnie) oraz confusion_matrix, a następnie wyniki klasyfikacji poszczególnych znaków na zdjęciach.

**Wyświetlenie wyników:**
>Nazwa zdjęcia.

>Ilość wykrytych znaków (wsztrskich typów).

>Koordynaty znaku: x_min, x_max, y_min, y_max - label_pred: etykieta.

**Plik programu:** [main.py](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/main.py) 

---
### Miłosz Gajewski
### Automatyka i Robotyka
### Politechnika Poznańska 2022
---
Materiały pomocnicze: [Materiały z zajęć](https://colab.research.google.com/drive/1x8lNIXMfwNe-tjnjteDXTUDcPfkVI6Vc?usp=sharing)