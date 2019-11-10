import numpy as np


def dpn(spectra_1, spectra_2):
    min_length = min(len(spectra_1), len(spectra_2)) - 1
    spectra_1_mag = np.linalg.norm(spectra_1['Absorbance'])
    spectra_2_mag = np.linalg.norm(spectra_2['Absorbance'])
    dot_prod = np.dot(spectra_1['Absorbance'][:min_length], spectra_2['Absorbance'][:min_length])

    return dot_prod / (spectra_1_mag * spectra_2_mag)