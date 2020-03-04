import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

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

        #print(f'Checking folder w/ type {spectrum_type} and len({len(folder_files)})')

        if spectrum_type not in types_count:
            types_count[spectrum_type] = 0

        for i in range(len(folder_files)):
            img_array_1 = cv2.imread(folder_files[i], cv2.IMREAD_GRAYSCALE)
            for j in range(i, len(folder_files)):
                if types_count[spectrum_type] < count_per_type: # to ensure there isn't a same file ab pair
                    img_array_2 = cv2.imread(folder_files[j], cv2.IMREAD_GRAYSCALE)
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
            data.append([img_array_1, img_array_2, num_class])
            types_count[spectrum_type] += 1

    print(f'Nonmatching entries by type: {types_count}')
    return data

def save(destination, data):
    pickle_out = open(destination, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()


if __name__=='__main__':
    directory = './visualization-similarity'
    categories = ['non-match', 'match']

    files = get_files(directory)

    matching_data = get_matching_entries(files, categories.index('match'), 2000)
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
    X_1, X_2, y = [], [], []
    for img_1, img_2, label in data:
        X_1.append(img_1)
        X_2.append(img_2)
        y.append(label)

    # Reshaping the data to be like the original image
    height = data[0][0].shape[0]
    width = data[0][0].shape[1]
    X_1 = np.array(X_1).reshape(-1, height, width, 1)
    X_2 = np.array(X_2).reshape(-1, height, width, 1)
    y = np.array(y)
    
    # Saving each dataset to the currect directory
    save('./X_1.pickle', X_1)
    save('./X_2.pickle', X_2)
    save('./y.pickle', y)