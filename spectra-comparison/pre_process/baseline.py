from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import peakutils

def make_nasa_data(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = abs(math.log(1 / float(line[1]), 10)) # converting reflectance to absorbance
                dataset.append([line[0], line[1]])

    return dataset

def baseline(data):
    y = data['Absorbance']
    base = peakutils.baseline(y, 1)
    return y - base

def set_range(data):
    max_peak = data['Absorbance'].max()
    data['Absorbance'] / max_peak


if __name__=='__main__':
    file_path = '../../nasa-dataset/manmade.concrete.pavingconcrete.solid.all.0425uuuasp.jhu.becknic.spectrum.txt'
    dataset = make_nasa_data(file_path)
    dataset = pd.DataFrame(dataset, columns = ['Wavenumber', 'Absorbance'])


    plt.figure(figsize=(12, 6))
    plt.subplot(2,1,1)
    plt.plot(dataset['Wavenumber'], dataset['Absorbance'])
    plt.title('Manmade Concrete -- Original')
    plt.ylabel('Absorbance')
    plt.xlabel('Wavenumber')

    dataset['Absorbance'] = baseline(dataset)

    plt.subplot(2,1,2)
    plt.plot(dataset['Wavenumber'], dataset['Absorbance'])
    plt.ylabel('Absorbance')
    plt.xlabel('Wavenumber')
    plt.show()