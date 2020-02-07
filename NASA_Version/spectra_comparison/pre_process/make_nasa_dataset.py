from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import math

def make_nasa_dataset(file_path):
    dataset = []
    with open(file_path, 'r', errors='ignore') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n' and line != '\t\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = float(line[1])
                dataset.append([line[0], line[1]])

    return dataset

if __name__=='__main__':
    vis_dir = '../../visualization-final-v2/'
    directory_path = '../../ecospeclib-final-nlc/'

    if not os.path.exists(vis_dir):
        os.mkdir(vis_dir)
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            new_path = vis_dir + '/'.join(file.split('.')[:5])
            split_file = file.split('.')[:5]

            for i in range(len(split_file) + 1):
                if not os.path.exists(vis_dir + '/'.join(split_file[:i])):
                    os.mkdir(vis_dir + '/'.join(split_file[:i]))

            dataset = make_nasa_dataset(file_path)
            dataset = pd.DataFrame(dataset, columns = ['Wavelength', 'Reflectance'])

            plt.figure(figsize=(12, 6))
            plt.plot(dataset['Wavelength'], dataset['Reflectance'])
            plt.title(file)
            plt.ylabel('Reflectance')
            plt.xlabel('Wavelength')

            plt.savefig(vis_dir + '/'.join(split_file) + '/' + file + '.png')
            plt.close('all')
