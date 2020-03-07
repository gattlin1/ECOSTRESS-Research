import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

if __name__=='__main__':
    directory = './visualization-class'
    categories = [folder.name for folder in os.scandir(directory)]
    training_data = []

    for category in categories:
        class_num = categories.index(category)

        path = os.path.join(directory, category)
        for img in os.listdir(path):
            img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
            training_data.append([img_array, class_num])

    height = training_data[0][0].shape[0]
    width = training_data[0][0].shape[1]

    random.shuffle(training_data)

    X = []
    y = []

    for img, label in training_data:
        X.append(img)
        y.append(label)

    X = np.array(X).reshape(-1, height, width, 1)

    pickle_out = open('./X.pickle', 'wb')
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open('./y.pickle', 'wb')
    pickle.dump(y, pickle_out)
    pickle_out.close()