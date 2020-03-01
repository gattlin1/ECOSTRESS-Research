import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

if __name__=='__main__':
    directory = './visualization-similarity'
    categories = ['non-match', 'match']
    training_data = []

    # Creating matching entries
    num_class = categories.index('match')

    types_count = {} # dict that keeps track of all entries we have of a specific type
    subfolders = []
    for f in os.scandir(directory):
        types_count[f.name] = 0
        subfolders.append(f.path)

    for folder in subfolders:
        files = []
        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                files.append(f.path)

            if len(files) >= 2:
                spectrum_type = files[0].split('/')[-1].split('.')[0] # gets the first classifier (i.e. type)

                # Pick a random file
                random_index = random.randint(0, len(files) - 1)
                img_array_1 = cv2.imread(files[random_index], cv2.IMREAD_GRAYSCALE)

                # Loop through the directory and create the matches
                for i in range(len(files)):
                    if i != random_index and types_count[spectrum_type] < 3000: # to ensure there isn't a same file ab pair
                        img_array_2 = cv2.imread(files[i], cv2.IMREAD_GRAYSCALE)
                        training_data.append([img_array_1, img_array_2, num_class])

                        types_count[spectrum_type] += 1
        print(f'classified: {folder}')

    print(len(training_data))
    print(types_count)


    # Creating non-matching entries

    height = training_data[0][0].shape[0]
    width = training_data[0][0].shape[1]

    for i in range(6):
        random.shuffle(training_data)

    X = []
    y = []

    for img_1, img_2, label in training_data:
        X.append([img_1, img_2])
        y.append(label)

    X = np.array(X).reshape(-1, height, width, 1)

    pickle_out = open('./X.pickle', 'wb')
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open('./y.pickle', 'wb')
    pickle.dump(y, pickle_out)
    pickle_out.close()