import numpy as np

def cor(spectra_1, spectra_2):
    avg1 = np.mean(spectra_1['Absorbance'])
    avg2 = np.mean(spectra_2['Absorbance'])
    nominator = norm_spectra_1 = norm_spectra_2 = 0

    for i in range(min(len(spectra_1), len(spectra_2))):
        nominator += (spectra_1['Absorbance'][i] - avg1) * (spectra_2['Absorbance'][i] - avg2)
        norm_spectra_1 += (spectra_1['Absorbance'][i] - avg1) ** 2
        norm_spectra_2 += (spectra_2['Absorbance'][i] - avg2) ** 2

    norm_spectra_1 **= 0.5
    norm_spectra_2 **= 0.5

    return nominator / (norm_spectra_1 * norm_spectra_2)
