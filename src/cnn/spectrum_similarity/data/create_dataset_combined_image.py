import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import cv2
import random
import math
import pickle
import sys
sys.path.append('../../../')

from pre_process.make_nasa_dataset import make_nasa_dataset
from pre_process.spectra_point_matcher import match_points

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

def make_graph(spectrum, name):
    dataset = pd.DataFrame(spectrum, columns = ['Wavelength', 'Reflectance'])

    plt.figure(figsize=(3, .15))
    plt.plot(dataset['Wavelength'], dataset['Reflectance'])
    plt.axis('off')

    plt.savefig(f'{name}.png', bbox_inches = 'tight', pad_inches = 0,
                facecolor='black', edgecolor='none', cmap='Blues_r')
    plt.close()

def pre_process_spectra(file_1, file_2, threshold_diff):
    spectrum_1 = make_nasa_dataset(file_1)
    spectrum_2 = make_nasa_dataset(file_2)
    spectrum_1, spectrum_2 = match_points(spectrum_1, spectrum_2, threshold_diff)
    graph_1 = make_graph(spectrum_1, 'spectrum_1')
    graph_2 = make_graph(spectrum_2, 'spectrum_2')

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
                if types_count[spectrum_type] < count_per_type: # to ensure there isn't a same file ab pair
                    pre_process_spectra(folder_files[i], folder_files[j], 5.0)

                    img_array_1 = cv2.imread('./spectrum_1.png')
                    img_array_2 = cv2.imread('./spectrum_2.png')
                    img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)
                    combined = combine_spectra(img_array_1, img_array_2)
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

            # While loop to get a folder that is not the same as the first spectrum's folder
            random_folder = []
            while True:
                random_folder = random.choice(files)

                if spectrum_type not in random_folder[0]:
                    break

            random_file = random.choice(random_folder)

            pre_process_spectra(file, random_file, 5.0)
            img_array_1 = cv2.imread('./spectrum_1.png')
            img_array_2 = cv2.imread('./spectrum_2.png')
            img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)
            combined = combine_spectra(img_array_1, img_array_2)

            data.append([combined, num_class])
            types_count[spectrum_type] += 1

    print(f'Nonmatching entries by type: {types_count}')
    return data

def randomly_flip_graphs(img_array_1, img_array_2):
    if random.choice([True, False]): # Randomly chooses whether to flip the graphs
        flip_code = random.choice([-1, 0, 1]) # -1 flips vertically and horizontally, 0 flips vertically, 1 flips horizontally

        img_array_1 = cv2.flip(img_array_1, flip_code)
        img_array_2 = cv2.flip(img_array_2, flip_code)

    return img_array_1, img_array_2

def combine_spectra(img_array_1, img_array_2):
    # set green and red channels to 0
    img_array_1[:, :, 1] = 0
    img_array_1[:, :, 2] = 0

    # set blue and red channels to 0
    img_array_2[:, :, 0] = 0
    img_array_2[:, :, 2] = 0

    # combine the spectrum
    combined = img_array_2 + img_array_1

    return combined


def save(destination, data):
    pickle_out = open(destination, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()

def create_training(files):
    categories = ['non-match', 'match']
    matching_data = get_matching_entries(files, categories.index('match'), 1000)
    print(f'Matching entries {len(matching_data)}')

    nonmatching_data = get_nonmatching_entries(files, categories.index('non-match'), 1000)
    print(f'Nonmatching entries {len(nonmatching_data)}')

    print(f'Index of match: {categories.index("match")}')
    print(f'Index of non-match: {categories.index("non-match")}')

    data = matching_data + nonmatching_data

    # shuffling the data an random amount of times
    for i in range(random.randint(1, 10)):
        random.shuffle(data)

    # Saving images and expected result to each dataset
    X, y = [], []
    for img, label in data:
        X.append(img)
        y.append(label)

    X = np.array(X)
    y = np.array(y)

    # Saving each dataset to the currect directory
    save('./pickles/X_train_2d.pickle', X)
    save('./pickles/y_train_2d.pickle', y)

def make_ab_pairs(files):
    pairs = []
    for i in range(len(files)):
        random.shuffle(files[i])
        pairs.append(files[i][0])
        pairs.append(files[i][1])
    return pairs

def create_validation(files, josh_dataset):
    files = make_ab_pairs(files)
    print(f'len(folders): {len(files)}')
    hitlist_entries = []

    for i in range(len(files) - 1):
        print(f'{i} out of {len(files) - 1}')
        for j in range(i + 1, len(files)):
            pre_process_spectra(files[i], files[j], 5.0)

            spec_1_name = files[i].replace('\\', '/').split('/')
            spec_2_name = files[j].replace('\\', '/').split('/')
            if josh_dataset:
                spec_1_name = spec_1_name[-1]
                spec_2_name = spec_2_name[-1]
            else:
                spec_1_name = spec_1_name[-1]
                spec_2_name = spec_2_name[-1]
            img_array_1 = cv2.imread('./spectrum_1.png')
            img_array_2 = cv2.imread('./spectrum_2.png')

            img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

            combined = combine_spectra(img_array_1, img_array_2)

            hitlist_entries.append([combined, [spec_1_name, spec_2_name]])

    # save hitlist entries
    save('./pickles/Hitlist_Entries_2d.pickle', hitlist_entries)

    print(f'len(hitlist_entries): {len(hitlist_entries)}')

if __name__=='__main__':
    directory = './ecospeclib-raw'
    random.seed(3)

    files = get_files(directory)
    random.shuffle(files)

    training, validation = split_data(files, validation_split=0.2)
    print(f'len(training): {len(training)}, len(validation): {len(validation)}')

    # create_training(training)
    create_validation(validation, False)