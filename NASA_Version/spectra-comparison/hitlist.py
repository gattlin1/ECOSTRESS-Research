import sys
sys.path.append('../../')

import colorama
import os
from colorama import Fore, Back, Style
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc
from pre_process.make_nasa_dataset import make_nasa_dataset
from pre_process.spectra_point_matcher import match_points
from copy import deepcopy

class Hitlist:
    def __init__(self, algorithm):
        self.comparison_type = algorithm
        self.missed_spectrum = []

    def find_match(self, file_path, dir_path):
        unknown_spectrum = make_nasa_dataset(file_path)
        unknown_spectrum_name = file_path.split('/')
        unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
        spectra_hitlist = []

        for file in os.listdir(dir_path):
            if file.endswith('.txt') and file != unknown_spectrum_name and 'spectrum' in file:
                unknown_spectrum_copy = deepcopy(unknown_spectrum)
                spectrum_name = file.split('.txt')[0]
                #print(Fore.CYAN + 'Checking File {0}'.format(spectrum_name) + Style.RESET_ALL)
                known_spectrum = make_nasa_dataset(dir_path + file)

                # calculating similarity score and then adding it to hitlist
                unknown_spectrum_copy, known_spectrum = match_points(unknown_spectrum, known_spectrum, 5.0)

                score = 0
                if len(unknown_spectrum_copy) > 0: # check to make sure the spectrums somewhat match
                    if 'cor' in self.comparison_type:
                        score = cor(unknown_spectrum_copy, known_spectrum)
                    elif 'dpn' in self.comparison_type:
                        score = dpn(unknown_spectrum_copy, known_spectrum)
                    elif 'mad' in self.comparison_type:
                        score = mad(unknown_spectrum_copy, known_spectrum)
                    elif 'msd' in self.comparison_type:
                        score = msd(unknown_spectrum_copy, known_spectrum)

                spectra_hitlist.append({'name': spectrum_name, 'score': score})

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)

        self.get_results(spectra_hitlist, self.comparison_type, unknown_spectrum_name.split('.txt')[0])

    def get_results(self, hitlist, title, expected_name):
        print('{0}: {1} is closest to: {2} w/ score: {3:.3f}'.format(title, expected_name, hitlist[0]['name'], hitlist[0]['score']))
        similarity = []
        compound = expected_name.split('.')

        for i in range(len(hitlist)):
            hitlist_compound = hitlist[i]['name'].split('.')

            similarity_count = 0
            for j in range(len(compound)):
                if compound[j] == hitlist_compound[j]:
                    similarity_count += 1

            similarity.append({'compound': hitlist[i]['name'], 'count': similarity_count})

        similarity = sorted(similarity, key=lambda i: i['count'], reverse=True)
        actual_closest = similarity[0]['compound']

        for i in range(len(hitlist)):
            if actual_closest == hitlist[i]['name']:
                if i > 0:
                    self.missed_spectrum.append([title, expected_name, i])
                    print(Fore.RED + 'Actual closest compound, {0}, was {1} spectrum from closest'.format(actual_closest, i) + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)
        print(hitlist[:5])

    def accuracy(self):
        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
        print(color + '\n{0} Spectrum Misclassified {1}'.format(self.comparison_type, len(self.missed_spectrum)) + Style.RESET_ALL)