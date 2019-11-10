import numpy as np

def mad(spectra):
    distance = 0
    mean = np.mean(spectra['Absorbance'])

    for value in spectra['Absorbance']:
        distance += abs(value - mean)

    return distance / len(spectra)