# Authors: Gattlin Walker
# script file to generate a pickle of the dataset for spectrum type
# this will generate a X.pickle which is a list of lists. Each individual list
# is the image array and second entry of classification output

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

def save(data, path):
    pickle_out = open(path, 'wb')
    pickle.dump(data, pickle_out)
    pickle_out.close()

if __name__=='__main__':
    directory = '../../../../datasets/ecospeclib-graphs'
    rules = {
        'manmade.': {'exclusions': [
            'generalconstructionmaterial',
            'roofingmaterial',
            'reflectancetarget']},
        'mineral.': {'exclusions': []},
        'rock.igneous.': {'exclusions': ['intermediate', 'feslic']},
        'rock.metamorphic.': {'exclusions': []},
        'rock.sedimentary.': {'exclusions': ['carbonate']},
        'vegetation.': {'exclusions': []},
        'water': {'exclusions': []}
    }
    categories = {}
    dataset = []

    random.seed(3)

    for file in os.scandir(directory):
        if '.vswir.' not in file.name:
            for rule in rules.keys():
                substr = file.name.find(rule)
                if substr == 0:
                    excluded = False
                    for ex in rules[rule]['exclusions']:
                        if ex in file.name:
                            excluded = True
                            break
                    if not excluded:
                        file_name = file.name
                        if 'vegetation.' not in file_name and\
                            'water.' not in file_name:
                            file_name = file.name[substr + len(rule):]
                        s_type = file_name.split('.')[0]

                        if s_type in categories:
                            categories[s_type].append(file.path)
                        else:
                            categories[s_type] = [file.path]

    print(f'{len(categories.keys())} Categories')

    type_num = 0
    for _, files in categories.items():
        for file in files:
            img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
            dataset.append([img, type_num])
        type_num += 1

    print(f'len(dataset): {len(dataset)}')

    random.shuffle(dataset)
    X, y = [], []
    for img, label in dataset:
      X.append(img)
      y.append(label)

    height = dataset[0][0].shape[0]
    width = dataset[0][0].shape[1]
    X = np.array(X).reshape(-1, height, width, 1)

    save(X, 'X.pickle')
    save(y, 'y.pickle')