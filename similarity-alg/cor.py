import pandas as pd
import numpy as np

def cor(spectra):
    mean_x = np.mean(spectra['Wavenumber'])
    mean_y = np.mean(spectra['Absorbance'])
    nominator = 0
    wave_squared_sum = 0
    absorb_squared_sum = 0

    for index, entry in spectra.iterrows():
        nominator += entry['Wavenumber'] * entry['Absorbance']
        wave_squared_sum += entry['Wavenumber'] ** 2
        absorb_squared_sum += entry['Absorbance'] ** 2

    nominator -= len(spectra) * mean_x * mean_y
    wave_squared_sum -= len(spectra) * (mean_x ** 2)
    absorb_squared_sum -= len(spectra) * (mean_y ** 2)

    denominator = (wave_squared_sum ** 0.5) * (absorb_squared_sum ** 0.5)

    return nominator / denominator