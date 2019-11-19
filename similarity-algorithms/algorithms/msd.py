import numpy as np

def msd(spectra):
    distance = 0
    mean = np.mean(spectra['Absorbance'])

    for value in spectra['Absorbance']:
        distance += (value - mean) ** 2

    distance /= len(spectra) - 1

    return distance ** 0.5
