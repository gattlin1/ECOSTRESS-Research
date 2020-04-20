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
    model = load_model('../saved_models/same-padding-2-conv-16-conv nodes-1-dense-32-dense nodes-0.01-alpha val.h5')

    data_X = pickle.load(open('../data/Hitlist_Entries_2d.pickle', 'rb'))
    X, spectra_entries = [], []
    for pair, spectra_names in data_X[:160]:
        cv2.imshow('pair', pair)
        cv2.waitKey(0)
        X.append(pair)
        spectra_entries.append(spectra_names)
    X = np.array(X)
    X = X / 255
    ynew = model.predict_proba(X)
    # show the inputs and predicted outputs
    for i in range(len(ynew)):
        print(f"{spectra_entries[i][0]}, {spectra_entries[i][1]}\n Val = {ynew[i]}")
