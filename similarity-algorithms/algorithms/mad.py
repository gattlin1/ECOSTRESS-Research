import numpy as np

def mad(spectra_1, spectra_2):
    distance = 0

    for i in range(min(len(spectra_1), len(spectra_2))):
        distance += abs(spectra_1['Absorbance'][i] - spectra_2['Absorbance'][i])

    return 1 / distance