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
    directory = './visualization-similarity'
    model = load_model('../saved_models/sequential-1-conv-32-nodes-1-dense.h5', custom_objects={'leaky_relu': tf.nn.leaky_relu})

    X = pickle.load(open('../data/X_combined_channel.pickle', 'rb'))
    X = X / 255
    ynew = model.predict_proba([X[40: 70]])
    ynew1 = model.predict_classes([X[40: 70]])
    # show the inputs and predicted outputs
    for i in range(len(ynew)):
        print(f"X[{i}], Predicted Val = {ynew[i]}, Predicted Class = {ynew1[i]}")
        cv2.imshow(f'X[{i}]', X[i])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

