import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model, load_model
import os
import cv2
import random
import pickle

def create_img(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    height = image.shape[0]
    width = image.shape[1]
    return image.reshape(-1, height, width, 1)

if __name__=='__main__':
    directory = './visualization-similarity'
    model = load_model('../saved_models/3-conv-32-nodes-2-dense-1583365012.h5')

    image_1 = create_img('../data/visualization-similarity/manmade/concrete/pavingconcrete/solid/all/manmade.concrete.pavingconcrete.solid.all.0092uuu_cnc.jhu.becknic.spectrum.txt.png')
    image_2 = create_img('../data/visualization-similarity/rock/sedimentary/chemicalprecipitate/solid/all/rock.sedimentary.chemicalprecipitate.solid.all.ward75.jpl.nicolet.spectrum.txt.png')

    X_1 = [image_2, image_2, image_2, image_2]
    X_2 = [image_2, image_2, image_2, image_2]
    score = model.predict([X_1[0], X_2[0]])
    print(score)

