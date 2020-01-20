from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd
import math

def make_nasa_dataset(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = 1 / float(line[1]) if float(line[1]) > 0 else 0 # converting reflectance to absorbanc
                dataset.append([line[0], line[1]])

    return dataset

# if __name__=='__main__':
#     file_path = '../../ecospeclib-all/manmade.concrete.pavingconcrete.solid.all.0425uuuasp.jhu.becknic.spectrum.txt'
#     dataset = make_nasa_data(file_path)
#     dataset = pd.DataFrame(dataset, columns = ['Wavenumber', 'Absorbance'])


#     plt.figure(figsize=(12, 6))
#     plt.plot(dataset['Wavenumber'], dataset['Absorbance'])
#     plt.title('Manmade Concrete -- Original')
#     plt.ylabel('Absorbance')
#     plt.xlabel('Wavenumber')

#     plt.show()