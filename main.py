# Wprowadzenie do sztucznej inteligencji - laboratorium - projekt zaliczeniowy 
import os
import random
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pandas

# TODO Dodać panią Piasek do repozytorium   jpiasek
 
def load_data(path, filename,folder_path):
    """
    Załadowanie danych.
    @param path: Ścieżka do folderu z próbkami.
    @param filename: Nazwa pliku csv, gdzie znajdują się informacje na temat próbki.
    @return: Lista słowników, jeden dla każdej próbki -> próbka i jej klasa. 
    """
    entry_list = pandas.read_csv(os.path.join(path, filename))
    data = []
    for idx, entry in entry_list.iterrows():
        if entry['Name'] == 'crosswalk':
            class_id = 1
        elif entry['Name'] == 'stop':
            class_id = 2
        elif entry['Name'] == 'speedlimit':
            class_id = 2
        elif entry['Name'] == 'trafficlight':
            class_id = 2
        
        image_path = folder_path + entry['Path']

        if class_id != -1:
            image = cv2.imread(os.path.join(path, image_path))
            data.append({'image': image, 'label': class_id})
    return data 

def display_dataset_stats(data):
    """
    Displays statistics about dataset in a form: class_id: number_of_samples
    @param data: List of dictionaries, one for every sample, with entry "label" (class_id).
    @return: Nothing
    """
    class_to_num = {}
    for idx, sample in enumerate(data):
        class_id = sample['label']
        if class_id not in class_to_num:
            class_to_num[class_id] = 0
        class_to_num[class_id] += 1

    class_to_num = dict(sorted(class_to_num.items(), key=lambda item: item[0]))
    print(class_to_num)

def balance_dataset(data, ratio):
    """
    Subsamples dataset according to ratio.
    @param data: List of samples.
    @param ratio: Ratio of samples to be returned.
    @return: Subsampled dataset.
    """
    sampled_data = random.sample(data, int(ratio * len(data)))

    return sampled_data

def main():
    print("### Dane treningowe ###")
    print("Wczytywanie danych treningowych.")
    data_train = load_data('./','Train.csv','./')
    print('Statystyka przed balansowaniem:')
    display_dataset_stats(data_train)
    data_train = balance_dataset(data_train, 1.0)
    print('Statystyka po balansowaniu:')
    display_dataset_stats(data_train)

    print("### Dane testowe ###")
    print("Wczytywanie danych testowych.")
    data_test = load_data('./', 'Test.csv','./Test/')
    print('Dane testowe przed balansowaniem:')
    display_dataset_stats(data_test)
    data_test = balance_dataset(data_test, 1.0)
    print('Dane testowe po balansowaniu:')
    display_dataset_stats(data_test)

if __name__ == '__main__':
    main()
