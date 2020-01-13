import os
import time
import colorama
from colorama import Fore, Back, Style
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc
from pre_process.make_dataset import make_dataset
from pre_process.spectra_point_matcher import match_points

def get_results(hitlist, title, expected_name):
    print('{0}: {1} is closest to: {2} w/ score: {3:.3f}'.format(title, expected_name, hitlist[0]['name'], hitlist[0]['score']))

    compound = expected_name[: len(expected_name) - 2]

    for i in range(len(hitlist)):
        hitlist_compound = hitlist[i]['name']
        hitlist_compound = hitlist_compound[: len(hitlist_compound) - 2]

        if compound == hitlist_compound:
            if i > 0:
                missed_spectrum.append([title, expected_name, i])
                print(Fore.RED + 'Actual closest compound was {0} spectrum from closest'.format(i) + Style.RESET_ALL)
            else:
                print(Fore.GREEN + 'Found an exact match' + Style.RESET_ALL)
            break

def hitlist(unknown_spectrum_path, known_spectra_directory):
    unknown_spectrum = make_dataset(unknown_spectrum_path)
    unknown_spectrum_name = unknown_spectrum_path.split('/')
    unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
    spectra_hitlist = []
    nlc_hitlist = []

    nlc_unknown = nlc(unknown_spectrum, 9)

    for file in os.listdir(known_spectra_directory):
        if (file.endswith('.csv') and file != unknown_spectrum_name):
            spectrum_name = file.split('.')[0]
            known_spectrum = make_dataset(known_spectra_directory + file)

            # calculating similarity score and then adding it to hitlist
            known_spectrum = match_points(unknown_spectrum, known_spectrum)
            score = cor(unknown_spectrum, known_spectrum)
            spectra_hitlist.append({'name': spectrum_name, 'score': score})

            # converting to nlc and then adding to nlc hitlist
            nlc_known = nlc(known_spectrum, 9)
            nlc_score = cor(nlc_unknown, nlc_known)
            nlc_hitlist.append({'name': spectrum_name, 'score': nlc_score})

    spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)
    nlc_hitlist = sorted(nlc_hitlist, key = lambda i: i['score'], reverse=True)

    get_results(spectra_hitlist, 'COR', unknown_spectrum_name.split('.')[0])
    get_results(nlc_hitlist, 'NLC -> COR', unknown_spectrum_name.split('.')[0])

    # print('%s seconds' % (time.time() - start_time))

if __name__=='__main__':
    colorama.init()
    missed_spectrum = []
    start_time = time.time()
    directory_path = '../spectra/'

    for file in os.listdir(directory_path):
        if (file.endswith('.csv')):
            hitlist(directory_path + file, directory_path)

    color = Fore.GREEN
    if len(missed_spectrum) > 0:
        color = Fore.RED
    print(color + '\nTotal Spectrum Misclassified {0}'.format(len(missed_spectrum)))
