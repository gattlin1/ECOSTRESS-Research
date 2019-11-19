import pandas as pd
import os
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn

def hitlist(unknown_spectra_path, known_spectra_directory):
    unknown_spectra = pd.read_csv(unknown_spectra_path, names=['Wavenumber', 'Absorbance'], header=None)
    most_similar_spectra = {'name': '', 'score': 0}

    for file in os.listdir(known_spectra_directory):
        if (file.endswith('.csv') and file != unknown_spectra_name):
            spectra_name = file.split('.')[0]
            known_spectra = pd.read_csv(known_spectra_directory + file, names=['Wavenumber', 'Absorbance'], header=None)
            score = dpn(unknown_spectra, known_spectra)

            if score > most_similar_spectra['score']:
                most_similar_spectra['name'] = spectra_name
                most_similar_spectra['score'] = score

    print('The spectra was identified most closely with {0} with a score of {1}'
    .format(most_similar_spectra['name'], most_similar_spectra['score']))

if __name__=='__main__':
    directory_path = '../spectra/'
    unknown_spectra_name = '109-97-7_b.csv'

    hitlist(directory_path+unknown_spectra_name, directory_path)

