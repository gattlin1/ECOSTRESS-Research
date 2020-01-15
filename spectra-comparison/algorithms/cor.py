import numpy as np

def get_mean(spectra):
    mean = 0
    for entry in spectra:
        mean += entry[1]

    return mean / len(spectra)

def cor(spectra_1, spectra_2):
    avg1 = get_mean(spectra_1)
    avg2 = get_mean(spectra_2)
    nominator, norm_spectra_1, norm_spectra_2 = 0, 0, 0

    for i in range(min(len(spectra_1), len(spectra_2))):
        nominator += (spectra_1[i][1] - avg1) * (spectra_2[i][1] - avg2)
        norm_spectra_1 += (spectra_1[i][1] - avg1) ** 2
        norm_spectra_2 += (spectra_2[i][1] - avg2) ** 2

    norm_spectra_1 **= 0.5
    norm_spectra_2 **= 0.5

    return nominator / (norm_spectra_1 * norm_spectra_2)
