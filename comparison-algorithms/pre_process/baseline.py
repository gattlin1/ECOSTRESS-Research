from scipy import sparse
from scipy.sparse.linalg import spsolve
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def make_nasa_data(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = abs(math.log10(1 / float(line[1]))) # converting reflectance to absorbance
                dataset.append([line[0], line[1]])

    return dataset

def baseline(data):
    print(data)
    x = data['Wavenumber']
    y = data['Absorbance']
    z = np.polyfit(x, y, 2)
    print(z)


def baseline_als(y, lam, p, niter=10):
  L = len(y)
  D = sparse.diags([1,-2,1],[0,-1,-2], shape=(L,L-2))
  w = np.ones(L)
  for i in range(niter):
    W = sparse.spdiags(w, 0, L, L)
    Z = W + lam * D.dot(D.transpose())
    z = spsolve(Z, w*y)
    w = p * (y > z) + (1-p) * (y < z)
  return z



if __name__=='__main__':
    file_path = '../../nasa_dataset/manmade.concrete.pavingconcrete.solid.all.0424uuucnc.jhu.becknic.spectrum.txt'
    dataset = make_nasa_data(file_path)
    dataset = pd.DataFrame(dataset, columns = ['Wavenumber', 'Absorbance'])

    plt.figure(figsize=(12, 6))
    plt.subplot(2,1,1)
    plt.plot(dataset['Wavenumber'], dataset['Absorbance'])
    plt.title('Manmade Concrete -- Original')
    plt.ylabel('Absorbance')
    plt.xlabel('Wavenumber')

    dataset['Absorbance'] = baseline_als(dataset['Absorbance'], 1, 0.05)

    plt.subplot(2,1,2)
    plt.plot(dataset['Wavenumber'], dataset['Absorbance'])
    plt.title('Manmade Concrete -- Baselined')
    plt.ylabel('Absorbance')
    plt.xlabel('Wavenumber')
    plt.show()