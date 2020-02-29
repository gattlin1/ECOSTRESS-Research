import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

if __name__=='__main__':
    directory = '../../../visualization-similarity'
    categories = ['non-match', 'match']
    training_data = []

    files = sorted([f.name for f in os.scandir(directory)])

    # Creating matching entries
    num_class = categories.index('match')
    for i in range(0, len(files), 2):
        img_array_1 = cv2.imread(files[i], cv2.IMREAD_GRAYSCALE)
        img_array_2 = cv2.imread(files[i + 1], cv2.IMREAD_GRAYSCALE)
        
        training_data.append([img_array_1, img_array_2, num_class])

    # Creating non-matching entries
    
    # height = training_data[0][0].shape[0]
    # width = training_data[0][0].shape[1]

    # random.shuffle(training_data)

    # X = []
    # y = []

    # for img, label in training_data:
    #     X.append(img)
    #     y.append(label)

    # X = np.array(X).reshape(-1, height, width, 1)

    # pickle_out = open('./X.pickle', 'wb')
    # pickle.dump(X, pickle_out)
    # pickle_out.close()

    # pickle_out = open('./y.pickle', 'wb')
    # pickle.dump(y, pickle_out)
    # pickle_out.close()