import os, glob
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import xml.etree.ElementTree as Xet
import pandas

# Klasy:
class Zdjecie:
    """
    Zdjęcia -> nazwa i lista obiektów.
    """
    def __init__(self,name,object):
        self.Nazwa = name # Nazwa zdjęcia
        self.lista_obiektow = object # Lista znaków(obiektów) na zdjęciu 

class Obiekt:
    """
    Poszczególne obiekty(znaki) w obrębie jednego zdjęcia.
    """
    def __init__(self,Width,Height,Name,Roi_X1,Roi_Y1,Roi_X2,Roi_Y2,Path):
        # Dane z pliku:
        self.Path = Path # Ścieżka do pliku
        self.Width = Width
        self.Height = Height
        self.Type = Name # Typ: crosswalk, Stop, trafficlight, speedlimit 
        self.X1 = Roi_X1
        self.X2 = Roi_X2
        self.Y1 = Roi_Y1
        self.Y2 = Roi_Y2
        if self.Type == 'crosswalk':
            self.label = 0
        elif self.Type == 'stop':
            self.label = 1
        elif self.Type == 'speedlimit':
            self.label = 1
        elif self.Type == 'trafficlight':
            self.label = 1
        self.image = cv2.imread(Path) # Załadowane zdjęcie
        # Dane uzyskane z predykcji:
        self.label_pred = 10
        self.X1_pred = 0
        self.X2_pred = 0
        self.Y1_pred = 0
        self.Y2_pred = 0
        self.desc = 0

# Funkcje:
def load_data(path, path_type):
    """
    Ładownie danych do obiektów klas.
    @param path: Ścieżka do folderu z plikami "*.xml"
    @param path_type: Typ zbioru - testowy lub treningowy.
    @return lista_zdj: lista obiektów klasy Zdjecie.
    """
    lista_zdj = []
    for filename in glob.glob(os.path.join(path, '*.xml')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            obiekty = []
            xmlparse = Xet.parse(f)
            root = xmlparse.getroot()
            File_name = xmlparse.find("filename").text
            Width = xmlparse.find("size/width").text
            Height = xmlparse.find("size/height").text
            liczba = 0
            for i in xmlparse.findall("object"):
                if(i):
                    Name = i.find("name").text
                    Roi_X1 =  i.find("bndbox/xmin").text
                    Roi_Y1 =  i.find("bndbox/ymin").text
                    Roi_X2 =  i.find("bndbox/xmax").text
                    Roi_Y2 =  i.find("bndbox/ymax").text
                    liczba += 1
                    Path = str(path_type) + File_name
                    obiekt_ = Obiekt(Width,Height,Name,Roi_X1,Roi_Y1,Roi_X2,Roi_Y2,Path)
                    obiekty.append(obiekt_)
            lista_zdj.append(Zdjecie(File_name,obiekty))
    return lista_zdj

def display_dataset_stats(data):
    """
    Wyświetlenie statystyki zbioru danych.
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Nothing
    """
    class_to_num = {}
    kat_0 = 0
    kat_1 = 1
    for i in data:
        for j in i.lista_obiektow:
            if(j.label == 0):
                kat_0 += 1
            if(j.label == 1):
                kat_1 += 1
    class_to_num = {'0':kat_0,'1':kat_1}
    print(class_to_num)

def learn_bovw(data):
    """
    Ekstrakcja cech w algorytmie BoVW i zapis ich jako słownik pliku "voc.npy".
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Nothing
    """
    dict_size = 128
    bow = cv2.BOWKMeansTrainer(dict_size)

    sift = cv2.SIFT_create()
    for sample in data:
        for sample_i in sample.lista_obiektow:
            kpts = sift.detect(sample_i.image, None)
            kpts, desc = sift.compute(sample_i.image,kpts)
            if desc is not None:
                bow.add(desc)
    vocabulary = bow.cluster()
    np.save('voc.npy', vocabulary)

def extract_features(data):
    """
    Wydobywanie cech zbioru i zapis deskryptorów.
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Lista obiektów klasy Zdjęcie z dodanymi deskryptorami dla każdej próbki.
    """
    sift = cv2.SIFT_create()
    flann = cv2.FlannBasedMatcher_create()
    bow = cv2.BOWImgDescriptorExtractor(sift, flann)
    vocabulary = np.load('voc.npy')
    bow.setVocabulary(vocabulary)
    for sample in data:
        for sample_i in sample.lista_obiektow:
            kpts = sift.detect(sample_i.image, None)
            desc = bow.compute(sample_i.image, kpts)
            sample_i.desc = desc
    return data

def train(data):
    """
    Trains Random Forest classifier
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Wytrenowany model.
    """
    descs = []
    labels = []
    for sample in data:
        for sample_i in sample.lista_obiektow:
            if sample_i.desc is not None:
                descs.append(sample_i.desc.squeeze(0))
                labels.append(sample_i.label)
    rf = RandomForestClassifier()
    rf.fit(descs, labels)
    return rf 

def evaluate(data):
    """
    Ewaluacja wyników klasyfikacji.
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Nothing
    """
    n_corr = 0
    n_incorr = 0
    pred_labels = []
    true_labels = []
    for sample in data:
        for sample_i in sample.lista_obiektow:
            if sample_i.desc is not None:
                pred_labels.append(sample_i.label_pred)
                true_labels.append(sample_i.label)
                if sample_i.label_pred == sample_i.label:
                    n_corr += 1
                else:
                    n_incorr += 1
    n = n_corr / max(n_corr + n_incorr, 1)
    print("Score = " + str(n))

    conf_matrix = confusion_matrix(true_labels, pred_labels)
    print(conf_matrix)
    return

def predict(rf, data):
    """
    Predykcja etykiet dla zbioru testowego.
    @param data: Lista obiektów klasy Zdjęcie.
    @param rf: Wtrenowany model
    @return: Lista obiektów klasy Zdjęcie.
    """  
    for sample in data:
        for sample_i in sample.lista_obiektow:
            if sample_i.desc is not None:
                pred = rf.predict(sample_i.desc)  
                sample_i.label_pred = int(pred)
    return data 

def display(data):
    """
    Wyświetlenie danych.
    @param data: Lista obiektów klasy Zdjęcie.
    @return: Nothing
    """
    for sample in data:
        nazwa = ''
        ilosc = 0
        koordynaty = []
        for sample_i in sample.lista_obiektow:
            if(sample_i.label_pred == 0):
                nazwa = sample.Nazwa
                ilosc += 1
                koordynaty.append([sample_i.X1_pred,sample_i.X2_pred,sample_i.Y1_pred,sample_i.Y2_pred])
        if(ilosc >= 1):
            print(nazwa)
            print(len(sample.lista_obiektow))
            for i in koordynaty:
                print(str(i[0]) + " " + str(i[1]) + " " + str(i[2]) + " " + str(i[3]))
    return

# Program główny:
def main():
    print("### Dane treningowe ###")
    print("Wczytywanie danych treningowych.")
    data_train = load_data('./Train/annotations','./Train/images/')
    print('Statystyka zbioru treningowego:')
    display_dataset_stats(data_train)

    print("### Dane testowe ###")
    print("Wczytywanie danych testowych.")
    data_test = load_data('./Test/annotations','./test/images/')
    print('Statystyka zbioru testowego:')
    display_dataset_stats(data_test)

    print("Ekstrakcja cech w algorytmie BoVW.")
    learn_bovw(data_train)

    print("Wydobywanie cech zbioru treningowego.")
    data_train = extract_features(data_train)

    print("Trenowanie.")
    rf = train(data_train)

    print("Wydobywanie cech zbioru testowego.")
    data_test = extract_features(data_test)

    print("Testowanie na zbiorze testowym.")
    data_test = predict(rf,data_test)

    print("Wyświetlenie wyników.")
    evaluate(data_test)
    display(data_test)

if __name__ == '__main__':
    main()