import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle
import sys
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

def get_matching_entries(files, num_class, count_per_type):
    data = []
    types_count = {} # dict that keeps track of all entries we have of a specific type

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        if spectrum_type not in types_count:
            types_count[spectrum_type] = 0

        for i in range(len(folder_files)):
            for j in range(i, len(folder_files)):
                if types_count[spectrum_type] < count_per_type: # to ensure there isn't a same file ab pair
                    img_array_1 = make_nasa_dataset(folder_files[i])
                    img_array_2 = make_nasa_dataset(folder_files[j])

                    img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

                    data.append([img_array_1, img_array_2, num_class])

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
            img_array_1 = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

            # While loop to get a folder that is not the same as the first spectrum's folder
            random_folder = []
            while True:
                random_folder = random.choice(files)

                if spectrum_type not in random_folder[0]:
                    break

            random_file = random.choice(random_folder)

            img_array_2 = cv2.imread(random_file, cv2.IMREAD_GRAYSCALE)

            img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

            data.append([img_array_1, img_array_2, num_class])
            types_count[spectrum_type] += 1

    print(f'Nonmatching entries by type: {types_count}')
    return data

def randomly_flip_graphs(img_array_1, img_array_2):
    if random.choice([True, False]): # Randomly chooses whether to flip the graphs
        flip_code = random.choice([-1, 0, 1]) # -1 flips vertically and horizontally, 0 flips vertically, 1 flips horizontally

        img_array_1 = cv2.flip(img_array_1, flip_code)
        img_array_2 = cv2.flip(img_array_2, flip_code)

    return img_array_1, img_array_2

def save(destination, data):
    pickle_out = open(destination, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()

if __name__=='__main__':
    directory = './ecospeclib-similarity'
    categories = ['non-match', 'match']

    random.seed(3)

    files = get_files(directory)

    matching_data = get_matching_entries(files, categories.index('match'), 1000)
    print(f'Matching entries {len(matching_data)}')

    nonmatching_data = get_nonmatching_entries(files, categories.index('non-match'), 2000)
    print(f'Nonmatching entries {len(nonmatching_data)}')

    print(f'Index of match: {categories.index("match")}')
    print(f'Index of non-match: {categories.index("non-match")}')

    data = matching_data + nonmatching_data

    # shuffling the data an random amount of times
    for i in range(random.randint(1, 10)):
        random.shuffle(data)

    # Saving images and expected result to each dataset
    X, y = [], []
    for img_1, label in data:
        X.append(img_1)
        y.append(label)

    # Reshaping the data to be like the original image
    height = data[0][0].shape[0]
    width = data[0][0].shape[1]

    print(X[0].shape)

    print(f'height: {height}')
    print(f'width: {width}')

    cv2.imshow('x', X[0])
    cv2.waitKey(0)


    X = np.array(X).reshape(-1, height, width, 3)
    y = np.array(y)

    height = X[0].shape

    print(f'shape: {height}')

    cv2.imshow('x', X_1[0])
    cv2.waitKey(0)
    # Saving each dataset to the currect directory
    save('./X_1.pickle', X_1)
    save('./X_2.pickle', X_2)
    save('./y.pickle', y)