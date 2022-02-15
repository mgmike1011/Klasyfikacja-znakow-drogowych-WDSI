# Wprowadzenie do sztucznej inteligencji - laboratorium
Projekt zaliczeniowy na przedmiot Wprowadzenie do sztucznej inteligencji - laboratorium. Autor: Miłosz Gajewski
### Cel projektu
Celem projektu było stworzenie oprogramowania rozpoznającego znaki drogowe i wyświetlającego informacje na temat znalezionego znaku przejścia dla pieszych (kategoria: crosswalk).
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
W nawiązaniu do zdobytych umiejętności z poprzednich lat studiów postanowiłem zrealizować program w oparciu o klasy i obiekty (podejście obiektowe). Struktura samego programu, czyli kolejne realizowane kroki oparte są o program z zajęć laboratoryjnych. Program rozpoczyna od pobrania plików .xml z odpowiednio folderów Train/annotations – zbiór treningowy oraz Test/annotations – zbiór testowy, przy czym informacje ze zbioru testowego używane są w pełni do uczenia, a ze zbioru testowego jedynie wybrane takie jak nazwa pliku .png. Znaki typu crosswalk stanowią kategorie ‘0’, wszystkie pozostałe znaki(typy znaków) stanowią kategorie 1. Kolejne kroki działania programu opisane są w funkcji main() programu. Przed wyświetleniem informacji o samych zanalezionych znakach wyświetlona zostaje ewaluacja wyników klasyfikacji z confusion_matrix.

**Wyświetlenie wyników:**

Nazwa zdjęcia, na którym został wykryty znak typu *Crosswalk*.

Ilość wykrytych znaków typu crosswalk.

Koordynaty znaku: x_min, x_max, y_min, y_max.

Wyświetlane są jedynie informacje o znalezionych znakach typu crosswalk - label_pred = 0.

**Plik programu:** [main.py](https://github.com/mgmike1011/WDSI_projekt_lab/blob/main/main.py) 
