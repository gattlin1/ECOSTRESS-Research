import numpy as np
import pandas as pd
import os
def nlc(spectra, width):
    results = pd.DataFrame(columns=['Wavenumber', 'Absorbance'])
    spectra_length = spectra.shape[0]

    for i in range(spectra_length):
        left_section = right_section = 0
        for j in range(1, width):
            if i - j > 0:
                left_section += spectra['Absorbance'][i - j]
            if i + j < spectra_length:
                right_section += spectra['Absorbance'][i + j]
        new_absorb = right_section / (left_section + right_section)
        results = results.append({'Wavenumber' : spectra['Wavenumber'][i] , 'Absorbance' : new_absorb}, ignore_index=True)

    return results

if __name__=='__main__':
    path = '../../spectra/'
    for file in os.listdir(path):
        if file.endswith('.csv'):
            spectra = pd.read_csv(path + file, names=['Wavenumber', 'Absorbance'], header=None)

            nlc_spectra = nlc(spectra, 10)
            nlc_spectra.to_csv('../../spectra/nlc_spectra/nlc_' + file, header=False, index=None)
