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

def learn_bovw(data):
    """
    Learns BoVW dictionary and saves it as "voc.npy" file.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image) and "label" (class_id).
    @return: Nothing
    """
    dict_size = 128
    bow = cv2.BOWKMeansTrainer(dict_size)

    sift = cv2.SIFT_create()
    for sample in data:
        kpts = sift.detect(sample['image'], None)
        kpts, desc = sift.compute(sample['image'], kpts)

        if desc is not None:
            bow.add(desc)

    vocabulary = bow.cluster()

    np.save('voc.npy', vocabulary)

def extract_features(data):
    """
    Extracts features for given data and saves it as "desc" entry.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image) and "label" (class_id).
    @return: Data with added descriptors for each sample.
    """
    sift = cv2.SIFT_create()
    flann = cv2.FlannBasedMatcher_create()
    bow = cv2.BOWImgDescriptorExtractor(sift, flann)
    vocabulary = np.load('voc.npy')
    bow.setVocabulary(vocabulary)
    for sample in data:
        # compute descriptor and add it as "desc" entry in sample
        # TODO PUT YOUR CODE HERE
        # Z ZAJĘĆ:
        kpts = sift.detect(sample['image'], None)
        desc = bow.compute(sample['image'], kpts)  # robienie deskryptora
        sample['desc'] = desc
        # ------------------

    return data

def train(data):  # tylko trenujemy model tutaj
    """
    Trains Random Forest classifier.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor).
    @return: Trained model.
    """
    # train random forest model and return it from function.
    # TODO PUT YOUR CODE HERE
    # GITHUB:

    # Z ZAJEC:
    descs = []
    labels = []
    for sample in data:
        if sample['desc'] is not None:
            descs.append(sample['desc'].squeeze(0))  # squeeze zmienia macierz na wektor wokol konkretnej osi -> tu wokol osi 0 (a mozemy wokol 0, 1 lub 2)
            labels.append(sample['label'])
    rf = RandomForestClassifier()
    rf.fit(descs, labels)
    # ------------------
    # Z ZAJEC:
    return rf  # wyjsciem funkcji jest model

def predict(rf, data):  # przyjmuje rf gdzie mamy zapisany model i dane porzednie
    """
    Predicts labels given a model and saves them as "label_pred" (int) entry for each sample.
    @param rf: Trained model.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor).
    @return: Data with added predicted labels for each sample.
    """
    # perform prediction using trained model and add results as "label_pred" (int) entry in sample
    # TODO PUT YOUR CODE HERE
    # Z ZAJEC:
    for idx, sample in enumerate(data):
        if sample['desc'] is not None:
            pred = rf.predict(sample['desc'])  # ta linia jest kluczowa dla predykcji, ale my chcemy zewaluowac cala baze danych dlatego robimy inne linijki
            sample['label_pred'] = int(pred)
    # zwraca etykiete do pred i uzupelniamy tabele data etykietą (etykiety byly 1, 2 ,3)
    # ------------------

    return data  # dane z wypredykowanymi etykietami

def evaluate(data):  # porownanie statystyczne, kolumna label_pred - wypredkowane labele, a w kolumnie label - etykiety prawdziwe. Wykorzystujemy jedna z metryk ewaluacji
    """
    Evaluates results of classification.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor), and "label_pred".
    @return: Nothing.
    """
    # evaluate classification results and print statistics
    # TODO PUT YOUR CODE HERE
    # Accuracy, ile rzeczy model trafil -> pierwsza z metod ewaluacji (wszystkie proby -> mianownik, to co sie udal -> w liczniku)
    # Z ZAJEC:
    n_corr = 0
    n_incorr = 0
    pred_labels = []
    true_labels = []
    for idx, sample in enumerate(data):
        if sample['desc'] is not None:
            pred_labels.append(sample['label_pred'])
            true_labels.append(sample['label'])
            if sample['label_pred'] == sample['label']:
                n_corr += 1
            else:
                n_incorr += 1
    n = n_corr / max(n_corr + n_incorr, 1)
    print("Score = " + str(n))

    conf_matrix = confusion_matrix(true_labels, pred_labels)
    print(conf_matrix)

    # ------------------
    # ------------------

    # this function does not return anything
    return

def display(data):
    """
    Displays samples of correct and incorrect classification.
    @param data: List of dictionaries, one for every sample, with entries "image" (np.array with image), "label" (class_id),
                    "desc" (np.array with descriptor), and "label_pred".
    @return: Nothing.
    """
    n_classes = 3

    corr = {}
    incorr = {}
    for idx, sample in enumerate(data):
        if sample['desc'] is not None:
            print(sample['image'])
    # this function does not return anything
    return

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
    data_test = load_data('./', 'Test.csv','./Test/images/')
    print('Dane testowe przed balansowaniem:')
    display_dataset_stats(data_test)
    data_test = balance_dataset(data_test, 1.0)
    print('Dane testowe po balansowaniu:')
    display_dataset_stats(data_test)

    # you can comment those lines after dictionary is learned and saved to disk.
    # print('learning BoVW')
    # learn_bovw(data_train)

    print('extracting train features')
    data_train = extract_features(data_train)

    print('training')
    rf = train(data_train)

    print('extracting test features')
    data_test = extract_features(data_test)

    print('testing on testing dataset')
    data_test = predict(rf, data_test)
    evaluate(data_test)
    display(data_test)

if __name__ == '__main__':
    main()
