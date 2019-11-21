import pandas as pd
import os
import time
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc

def get_results(hitlist, title, expected_name):
    print(title)
    print('{0} is closest to: {1} w/ score: {2:.3f}'.format(expected_name, hitlist[0]['name'], hitlist[0]['score']))

    compound = expected_name[: len(expected_name) - 2]

    for i in range(len(hitlist)):
        hitlist_compound = hitlist[i]['name']
        hitlist_compound = hitlist_compound[: len(hitlist_compound) - 2]

        if compound == hitlist_compound:
            print('Actual closest compound was {0} spectrum from closest'.format(i))
            break

def hitlist(unknown_spectrum_path, known_spectra_directory):
    unknown_spectrum = pd.read_csv(unknown_spectrum_path, names=['Wavenumber', 'Absorbance'], header=None)
    unknown_spectrum_name = unknown_spectrum_path.split('/')
    unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
    spectra_hitlist = []
    nlc_hitlist = []

    nlc_unknown = nlc(unknown_spectrum, 10)

    for file in os.listdir(known_spectra_directory):
        if (file.endswith('.csv') and file != unknown_spectrum_name):
            spectrum_name = file.split('.')[0]
            known_spectrum = pd.read_csv(known_spectra_directory + file, names=['Wavenumber', 'Absorbance'], header=None)

            # calculating similarity score and then adding it to hitlist
            score = mad(unknown_spectrum, known_spectrum)
            spectra_hitlist.append({'name': spectrum_name, 'score': score})

            # converting to nlc and then adding to nlc hitlist
            nlc_known = nlc(known_spectrum, 10)
            nlc_score = mad(nlc_unknown, nlc_known)
            nlc_hitlist.append({'name': spectrum_name, 'score': nlc_score})

    spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)
    nlc_hitlist = sorted(nlc_hitlist, key = lambda i: i['score'], reverse=True)

    get_results(spectra_hitlist, 'COR', unknown_spectrum_name.split('.')[0])
    get_results(nlc_hitlist, '\nNLC -> COR', unknown_spectrum_name.split('.')[0])

    print('%s seconds' % (time.time() - start_time))

if __name__=='__main__':
    directory_path = '../spectra/'
    unknown_spectrum_name = '50-78-2_a.csv'

    start_time = time.time()
    hitlist(directory_path + unknown_spectrum_name, directory_path)

