import sys
sys.path.append('../../')

import colorama
from colorama import Fore, Back, Style
import os
import os.path
from os import path
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

        if not os.path.exists('./results/{0} results.txt'.format(self.comparison_type)):
            open('./results/{0} results.txt'.format(self.comparison_type), 'x', errors='ignore')

    def find_match(self, file_path, dir_path):
        unknown_spectrum_name = file_path.split('/')
        unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
        spectra_hitlist = []
        spectrometer_range = ''

        # The dataset has several different spectrometer ranges that are used.
        # This is in place so later in the program it can ensure the same spectrum
        # ranges are being compared and others are ignored.
        if '.vswir' in unknown_spectrum_name:
            spectrometer_range = '.vswir'
        elif '.tir' in unknown_spectrum_name:
            spectrometer_range = '.tir'
        elif '.all' in unknown_spectrum_name:
            spectrometer_range = '.all'

        unknown_spectrum = make_nasa_dataset(file_path)

        for file in os.listdir(dir_path):
            if file.endswith('.txt') and file != unknown_spectrum_name and self.valid_spectrum_file(file, spectrometer_range):
                unknown_spectrum_copy = deepcopy(unknown_spectrum)
                spectrum_name = file.split('.txt')[0]
                #print(Fore.CYAN + 'Checking File {0}'.format(spectrum_name) + Style.RESET_ALL)
                known_spectrum = make_nasa_dataset(dir_path + file)

                # calculating similarity score and then adding it to hitlist
                unknown_spectrum_copy, known_spectrum = match_points(unknown_spectrum_copy, known_spectrum, 5.0)

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

    def valid_spectrum_file(self, file_name, spectrometer_range):
        if 'spectrum' in file_name:
            if spectrometer_range == '.vswir':
                if spectrometer_range in file_name:
                    return True
            elif spectrometer_range == '.tir' or spectrometer_range == '.all':
                if '.vswir' not in file_name:
                    return True
        return False

    def get_results(self, hitlist, title, expected_name):
        file =  open('./results/{0} results.txt'.format(self.comparison_type), 'a', errors='ignore')
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
                    
                    file.write('\n{0}: {1} is closest to: {2} w/ score: {3:.3f}\n'.format(title, expected_name, hitlist[0]['name'], hitlist[0]['score']))
                    file.write('Actual closest compound, {0}, was {1} spectrum from closest\n'.format(actual_closest, i))
                else:
                    print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)

    def accuracy(self):
        average_miss = 0

        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            
            for entry in self.missed_spectrum:
                average_miss += entry[2]
            average_miss /= len(self.missed_spectrum)

        file =  open('./results/{0} results.txt'.format(self.comparison_type), 'a', errors='ignore')

        print(color + '\n{0} Spectrum Misclassified {1}'.format(self.comparison_type, len(self.missed_spectrum)) + Style.RESET_ALL)
        print(color + '\nAverage Miss: {0:.2f}'.format(average_miss) + Style.RESET_ALL)

        file.write('\n{0} Spectrum Misclassified {1}\n'.format(self.comparison_type, len(self.missed_spectrum)))
        file.write('\nAverage Miss: {0:.2f}\n'.format(average_miss))
