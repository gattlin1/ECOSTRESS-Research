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
    new_x = []
    new_y = []
    for x in X[40:70]:
        new_x.append(x[0])
        new_y.append(x[1])
    ynew = model.predict_proba(new_x)
    ynew1 = model.predict_classes(new_x)
    # show the inputs and predicted outputs
    for i in range(len(ynew)):
        print(new_y[i][0], new_y[i][1])
        print(f"X[{i}], Val = {ynew[i]},Class = {ynew1[i]}")
