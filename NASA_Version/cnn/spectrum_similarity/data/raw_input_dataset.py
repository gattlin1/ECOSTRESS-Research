import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import cv2
import random
import pickle
import math

sys.path.append('../../../')
from pre_process.make_nasa_dataset import make_nasa_dataset
from pre_process.spectra_point_matcher import create_matched_spectra

def get_files(directory):
    subfolders = [ f.path for f in os.scandir(directory) ]
    files = []

    for folder in subfolders:
        folder_files = []
        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                folder_files.append(f.path)

        if len(folder_files) >= 2:
            files.append(folder_files)

    return files

def split_data(data, validation_split=0.1):
    split_point = int(len(data) * (1 - validation_split))

    return data[:split_point], data[split_point + 1:]

def get_matching_entries(files, num_class, count_per_type):
    data = []
    types_count = {} # dict that keeps track of all entries we have of a specific type

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        if spectrum_type not in types_count:
            types_count[spectrum_type] = 0

        for i in range(len(folder_files)):
            for j in range(i + 1, len(folder_files)):
                if types_count[spectrum_type] < count_per_type:
                    spectrum_1 = make_nasa_dataset(folder_files[i])
                    spectrum_2 = make_nasa_dataset(folder_files[j])

                    spectrum_1, spectrum_2 = create_matched_spectra(spectrum_1, spectrum_2, 5.0)
                    spectrum_1 = [x[1] for x in spectrum_1]
                    spectrum_2 = [x[1] for x in spectrum_2]

                    normalize(spectrum_1)
                    normalize(spectrum_2)

                    randomly_flip_graphs(spectrum_1, spectrum_2)

                    combined = [spectrum_1, spectrum_2]

                    data.append([combined, num_class])

                    types_count[spectrum_type] += 1

    print(f'Matching entries by type: {types_count}')
    return data

def get_nonmatching_entries(files, num_class, count_per_type):
    data = []
    types_count = {}

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        if spectrum_type not in types_count:
            types_count[spectrum_type] = 0

        for file in folder_files:
            spectrum_1 = make_nasa_dataset(file)

            # While loop to get a folder that is not the same as the first spectrum's folder
            random_folder = []
            while True:
                random_folder = random.choice(files)

                if spectrum_type not in random_folder[0]:
                    break

            random_file = random.choice(random_folder)

            spectrum_2 = make_nasa_dataset(random_file)

            spectrum_1, spectrum_2 = create_matched_spectra(spectrum_1, spectrum_2, 5.0)
            spectrum_1 = [x[1] for x in spectrum_1]
            spectrum_2 = [x[1] for x in spectrum_2]

            normalize(spectrum_1)
            normalize(spectrum_2)

            randomly_flip_graphs(spectrum_1, spectrum_2)

            combined = [spectrum_1, spectrum_2]

            data.append([combined, num_class])
            types_count[spectrum_type] += 1

    print(f'Nonmatching entries by type: {types_count}')
    return data

def normalize(spectrum):
    min_y = min(spectrum)
    max_y = max(spectrum)

    for i in range(len(spectrum)):
        if abs(max_y - min_y) == 0:
            spectrum[i] = 0
        else:
            spectrum[i] = (spectrum[i] - min_y) / (max_y - min_y)
            spectrum[i] = round(spectrum[i], 1)

def randomly_flip_graphs(spectrum_1, spectrum_2):
    if random.choice([True, False]): # Randomly chooses whether to flip the graphs
        flip_code = random.choice(['vert', 'hori', 'both'])

        if flip_code == 'vert':
            flip_vert(spectrum_1)
            flip_vert(spectrum_2)

        if flip_code == 'hori':
            flip_hori(spectrum_1)
            flip_hori(spectrum_2)

        if flip_code == 'both':
            flip_hori(spectrum_1)
            flip_hori(spectrum_2)
            flip_vert(spectrum_1)
            flip_vert(spectrum_2)

def flip_vert(spectrum):
    for i in range(len(spectrum)):
        spectrum[i] = 1 - spectrum[i]

def flip_hori(spectrum):
    spectrum.reverse()

def save(destination, data):
    pickle_out = open(destination, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()

def make_consistent_spectra_len(data):
    max_len = 0
    for entry in data:
        entry_max_len = max(len(entry[0][0]), len(entry[0][1]))

        if entry_max_len > max_len:
            max_len = entry_max_len

    print(f'max_len: {max_len}')

    for entry in data:
        for spectrum in entry[0]:
            if len(spectrum) < max_len:
                difference = max_len - len(spectrum)
                dummy_values = [0] * difference
                spectrum += dummy_values

def create_training(files):
    categories = ['non-match', 'match']

    matching_data = get_matching_entries(files, categories.index('match'), 1000)
    print(f'Matching entries {len(matching_data)}')

    nonmatching_data = get_nonmatching_entries(files, categories.index('non-match'), 1000)
    print(f'Nonmatching entries {len(nonmatching_data)}')

    print(f'Index of match: {categories.index("match")}')
    print(f'Index of non-match: {categories.index("non-match")}')

    data = matching_data + nonmatching_data

    make_consistent_spectra_len(data)

    # shuffling the data an random amount of times
    for i in range(random.randint(1, 10)):
        random.shuffle(data)

    # Saving images and expected result to each dataset
    X, y = [], []
    for spectra_pair, label in data:
        X.append(spectra_pair)
        y.append(label)

        print(len(spectra_pair[0]))
        print(len(spectra_pair[1]))
        break

    X = np.array(X).reshape(-1, len(spectra_pair[0]), 2)
    print(X[0])
    print(X.shape)
    y = np.array(y)
    print(y[0])
    print(y.shape)

    # Saving each dataset to the currect directory
    save('X_train.pickle', X)
    save('y_train.pickle', y)

def make_ab_pairs(files):
    pairs = []
    for i in range(len(files)):
        random.shuffle(files[i])
        pairs.append(files[i][0])
        pairs.append(files[i][1])
    return pairs

def create_validation(files):
    files = make_ab_pairs(files)
    print(f'len(folders): {len(files)}')
    hitlist_entries = []

    for i in range(len(files) - 1):
        for j in range(i + 1, len(files)):
            spec_1_name = files[i].replace('\\', '/')
            spec_1_name = spec_1_name.split('/')[-1]
            spec_2_name = files[i].replace('\\', '/')
            spec_2_name = spec_2_name.split('/')[-1]


            spectrum_1 = make_nasa_dataset(files[i])
            spectrum_2 = make_nasa_dataset(files[j])
            spectrum_1, spectrum_2 = create_matched_spectra(spectrum_1, spectrum_2, 5.0)

            spectrum_1 = [x[1] for x in spectrum_1]
            spectrum_2 = [x[1] for x in spectrum_2]

            normalize(spectrum_1)
            normalize(spectrum_2)

            randomly_flip_graphs(spectrum_1, spectrum_2)
            combined = [spectrum_1, spectrum_2]
            hitlist_entries.append([combined, [spec_1_name, spec_2_name]])

    # need to have a way to make sure the len between val and training is the same
    make_consistent_spectra_len(hitlist_entries)

    # save hitlist entries
    save('Hitlist_Entries.pickle', hitlist_entries)

    print(f'len(hitlist_entries): {len(hitlist_entries)}')

if __name__=='__main__':
    directory = './ecospeclib-raw'
    random.seed(3)

    files = get_files(directory)
    random.shuffle(files)

    training, validation = split_data(files, validation_split=0.2)
    print(f'len(training): {len(training)}, len(validation): {len(validation)}')

    create_training(training)
    #create_validation(validation)