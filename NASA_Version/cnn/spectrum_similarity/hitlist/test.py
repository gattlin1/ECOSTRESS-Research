import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, LeakyReLU
import os
import cv2
import random
import pickle

if __name__=='__main__':
    model = load_model('../saved_models/1d-sequential.h5')

    X = pickle.load(open('../data/Hitlist_Entries.pickle', 'rb'))
    X = [x[0] for x in X]
    ynew = model.predict_proba([X[40: 70]])
    ynew1 = model.predict_classes([X[40: 70]])
    # show the inputs and predicted outputs
    for i in range(len(ynew)):
        print(f"X[{i}], Predicted Val = {ynew[i]}, Predicted Class = {ynew1[i]}")
        cv2.imshow(f'X[{i}]', X[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

