import numpy as np

def msd(spectra_1, spectra_2):
    distance = 0

    for i in range(min(len(spectra_1), len(spectra_2))):
        distance += (spectra_1['Absorbance'][i] - spectra_2['Absorbance'][i]) ** 2

    return 1 / (distance ** 0.5)
