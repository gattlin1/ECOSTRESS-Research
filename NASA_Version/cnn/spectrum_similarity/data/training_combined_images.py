import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle
import math

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
    types_count = 0

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        for i in range(len(folder_files)):
            for j in range(i, len(folder_files)):
                if types_count < count_per_type: # to ensure there isn't a same file ab pair
                    img_array_1 = cv2.imread(folder_files[i])
                    img_array_2 = cv2.imread(folder_files[j])

                    img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

                    combined = combine_spectra(img_array_1, img_array_2)

                    data.append([combined, num_class])

                    types_count += 1

    return data

def get_nonmatching_entries(files, num_class, count_per_type):
    data = []
    types_count = 0

    for folder_files in files:
        folder_files[0] = folder_files[0].replace('\\', '/', -1)  # incase of windows os
        spectrum_type = folder_files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

        for file in folder_files:

            for _ in range(2):
                img_array_1 = cv2.imread(file)
                # While loop to get a folder that is not the same as the first spectrum's folder
                random_folder = []
                while True:
                    random_folder = random.choice(files)

                    if spectrum_type not in random_folder[0]:
                        break


                random_file = random.choice(random_folder)

                img_array_2 = cv2.imread(random_file)

                cv2.imshow('1b', img_array_1)
                cv2.imshow('2b', img_array_2)

                img_array_1, img_array_2 = randomly_flip_graphs(img_array_1, img_array_2)

                cv2.imshow('1a', img_array_1)
                cv2.imshow('2a', img_array_2)

                combined = combine_spectra(img_array_1, img_array_2)

                cv2.imshow('combined', combined)
                cv2.waitKey(0)
                data.append([combined, num_class])
                types_count += 1

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


if __name__=='__main__':
    directory = './training-graphs'
    categories = ['non-match', 'match']

    random.seed(3)

    files = get_files(directory)
    print(f'File Count: {len(files)}')

    matching_data = get_matching_entries(files, categories.index('match'), math.inf)
    print(f'Matching entries {len(matching_data)}')

    nonmatching_data = get_nonmatching_entries(files, categories.index('non-match'), math.inf)
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
    save('./X_train.pickle', X)
    save('./y_train.pickle', y)