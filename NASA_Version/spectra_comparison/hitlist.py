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

        self.file = open('./results/{0} results.txt'.format(self.comparison_type), 'a', errors='ignore')

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
                    self.log_info('{0}: {1} is closest to: {2} w/ score: {3:.3f}'.format(title, expected_name, hitlist[0]['name'], hitlist[0]['score']), Fore.RED)
                    self.log_info('Actual closest compound, {0}, was {1} spectrum from closest\n'.format(actual_closest, i), Fore.RED)
                else:
                    print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)

    def accuracy(self):
        average_miss = 0
        missed_categories = {'manmade': [0,0], 'meteorites': [0,0], 'mineral': [0,0], 'nonphotosyntheticvegetation': [0,0], 'rock': [0,0], 'soil': [0,0], 'vegetation': [0,0], 'water':[0,0]}

        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            for entry in self.missed_spectrum:
                average_miss += entry[2]
                spectrum_type = entry[1].split('.')[0]

                if spectrum_type in missed_categories.keys():
                    missed_categories[spectrum_type][0] += 1
                    missed_categories[spectrum_type][1] += entry[2]
                        
            average_miss /= len(self.missed_spectrum)
            
        self.log_info('Total Spectrum Misclassified {0}'.format(len(self.missed_spectrum)), color)
        self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)

        for category in missed_categories.keys():
            self.log_info('{0} Spectrum Misclassified {1}'.format(category, missed_categories[category][0]), color)

            average_miss = 0
            if missed_categories[category][0] > 0:
                average_miss = missed_categories[category][1] / missed_categories[category][0]

            self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)
    
    def log_info(self, text, color):
        print(color + text + Style.RESET_ALL)
        self.file.write('\n' + text)
