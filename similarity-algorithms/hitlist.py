import pandas as pd
import os
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc

def hitlist(unknown_spectrum_path, known_spectra_directory):
    unknown_spectrum = pd.read_csv(unknown_spectrum_path, names=['Wavenumber', 'Absorbance'], header=None)
    spectra_hitlist = []
    nlc_hitlist = []

    nlc_unknown = nlc(unknown_spectrum, 10)

    for file in os.listdir(known_spectra_directory):
        if (file.endswith('.csv') and file != unknown_spectra_name):
            spectra_name = file.split('.')[0]
            known_spectrum = pd.read_csv(known_spectra_directory + file, names=['Wavenumber', 'Absorbance'], header=None)
            score = cor(unknown_spectrum, known_spectrum)
            spectra_hitlist.append({'name': spectra_name, 'score': score})

            nlc_known = nlc(known_spectrum, 10)
            nlc_score = cor(nlc_unknown, nlc_known)
            nlc_hitlist.append({'name': spectra_name, 'score': nlc_score})

    spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)
    nlc_hitlist = sorted(nlc_hitlist, key = lambda i: i['score'], reverse=True)

    print('Spectra Hitlist: Most Similar -> Least Similar')
    for spectrum in spectra_hitlist:
        print('{0}: {1:.4f}'.format(spectrum['name'], spectrum['score']))

    print('\nNLC Spectra Hitlist: Most Similar -> Least Similar')
    for spectrum in nlc_hitlist:
        print('{0}: {1:.4f}'.format(spectrum['name'], spectrum['score']))

if __name__=='__main__':
    directory_path = '../spectra/'
    unknown_spectra_name = '79-09-4_b.csv'

    hitlist(directory_path+unknown_spectra_name, directory_path)

