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
    model = load_model('../saved_models/1-conv-32-nodes-2-dense.h5')
    im1_path = '../data/visualization-similarity/manmade/concrete/pavingconcrete/solid/all/manmade.concrete.pavingconcrete.solid.all.0092uuu_cnc.jhu.becknic.spectrum.txt.png'
    im2_path = '../data/visualization-similarity/rock/sedimentary/chemicalprecipitate/solid/all/rock.sedimentary.chemicalprecipitate.solid.all.ward75.jpl.nicolet.spectrum.txt.png'

    image_1 = create_img(im1_path)
    image_2 = create_img(im2_path)
    score = model.predict([image_1, image_2])
    print(score)

    image_1 = create_img(im1_path)
    image_2 = create_img(im1_path)
    score = model.predict([image_1, image_2])
    print(score)

