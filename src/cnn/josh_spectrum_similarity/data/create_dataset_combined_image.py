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

def get_matching_entries(files, num_class):
    data = []

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        for i in range(len(folder_files)):
            for j in range(i + 1, len(folder_files)):
                img_array_1 = cv2.imread(folder_files[i])
                img_array_2 = cv2.imread(folder_files[j])

                img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)
                combined = combine_spectra(img_array_1, img_array_2)
                data.append([combined, num_class])

    return data

def get_nonmatching_entries(files, num_class):
    data = []

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        for file in folder_files:

            # While loop to get a folder that is not the same as the first spectrum's folder
            random_folder = []
            while True:
                random_folder = random.choice(files)

                if spectrum_type not in random_folder[0]:
                    break

            random_file = random.choice(random_folder)
            img_array_1 = cv2.imread(file)
            img_array_2 = cv2.imread(random_file)
            img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)
            combined = combine_spectra(img_array_1, img_array_2)

            data.append([combined, num_class])

    return data

def randomly_flip_graphs(img_array_1, img_array_2):
    if random.choice([True, False]): # Randomly chooses whether to flip the graphs
        # -1 flips vertically and horizontally, 0 flips vertically, 1 flips
        # horizontally
        flip_code = random.choice([-1, 0, 1])

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
    matching_data = get_matching_entries(files, categories.index('match'))
    print(f'Matching entries {len(matching_data)}')

    nonmatching_data = get_nonmatching_entries(files, categories.index('non-match'))
    print(f'Nonmatching entries {len(nonmatching_data)}')

    print(f'Index of match: {categories.index("match")}')
    print(f'Index of non-match: {categories.index("non-match")}')

    data = matching_data + nonmatching_data

    # shuffling the data
    random.shuffle(data)

    # Saving images and expected result to each dataset
    X, y = [], []
    for img, label in data:
        X.append(img)
        y.append(label)

    X = np.array(X)
    y = np.array(y)

    # Saving each dataset to the currect directory
    save('./pickles/X.pickle', X)
    save('./pickles/y.pickle', y)

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
        print(f'{i} out of {len(files) - 1}')
        for j in range(i + 1, len(files)):
            spec_1_name = files[i].replace('\\', '/').split('/')
            spec_2_name = files[j].replace('\\', '/').split('/')
            spec_1_name = spec_1_name[-2]
            spec_2_name = spec_2_name[-2]

            img_array_1 = cv2.imread(files[i])
            img_array_2 = cv2.imread(files[j])

            img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

            combined = combine_spectra(img_array_1, img_array_2)

            hitlist_entries.append([combined, [spec_1_name, spec_2_name]])

    # save hitlist entries
    save('./pickles/Hitlist_Entries_2d.pickle', hitlist_entries)

    print(f'len(hitlist_entries): {len(hitlist_entries)}')

if __name__=='__main__':
    directory = '../../../../datasets/josh-dataset'
    random.seed(3)

    files = get_files(directory)
    random.shuffle(files)

    training, validation = split_data(files, validation_split=0.1)
    print(f'len(training): {len(training)}, len(validation): {len(validation)}')

    create_training(training)
    create_validation(validation)