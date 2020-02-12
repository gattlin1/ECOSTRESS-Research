import sys
sys.path.append('../../')

import colorama
from colorama import Fore, Back, Style
import os
import os.path
from os import path
from algorithms.cor import cor
from algorithms.mad import mad
from algorithms.dpn import dpn
from algorithms.msd import msd
from pre_process.make_nasa_dataset import make_nasa_dataset
from pre_process.spectra_point_matcher import match_points
from copy import deepcopy
import multiprocessing
from multiprocessing import Manager

class Hitlist:
    def __init__(self, algorithm, dataset_path, file_title=''):
        self.comparison_type = algorithm
        self.missed_spectrum = []
        self.dataset_path = dataset_path
        self.classification_level = [0, 0, 0, 0, 0]

        results_path = '../results/5th_run/{0} results {1}.txt'.format(self.comparison_type, file_title)
        self.results = self.open_file(results_path)

        heatmap_path = '../results/heatmap/{0} results.txt'.format(self.comparison_type)
        self.heatmap = self.open_file(heatmap_path)

    def open_file(self, path):
        if not os.path.exists(path):
            open(path, 'x', errors='ignore')

        return open(path, 'a', errors='ignore')

    def find_matches(self, file_path, files, difference_matrix):
        unknown_spectrum_name = file_path.split('/')
        unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]

        unknown_spectrum = make_nasa_dataset(file_path)

        for file in files:
            if self.valid_spectrum_file(file, file_path, difference_matrix):
                unknown_spectrum_copy = deepcopy(unknown_spectrum)
                known_spectrum = make_nasa_dataset(self.dataset_path + file)

                if file == 'vegetation.shrub.arctostaphylos.glandulosa.vswir.vh122.ucsb.asd.spectrum.txt':
                    x = 5

                # calculating similarity score and then adding it to hitlist
                unknown_spectrum_copy, known_spectrum = match_points(unknown_spectrum_copy, known_spectrum, 1.0)

                score = 0
                if 'cor' in self.comparison_type:
                    score = cor(unknown_spectrum_copy, known_spectrum)
                elif 'dpn' in self.comparison_type:
                    score = dpn(unknown_spectrum_copy, known_spectrum)
                elif 'mad' in self.comparison_type:
                    score = mad(unknown_spectrum_copy, known_spectrum)
                elif 'msd' in self.comparison_type:
                    score = msd(unknown_spectrum_copy, known_spectrum)

                difference_matrix[file] = score


    def valid_spectrum_file(self, file_name, unknown_spectrum_name, difference_matrix):
        if not self.uncalculated_spectra_pair(file_name, difference_matrix):
            return False
        if not self.correct_ir_range(file_name, unknown_spectrum_name):
            return False

        return True

    def uncalculated_spectra_pair(self, file_name, difference_matrix):
        if difference_matrix[file_name] == 0:
            return True

        return False

    # check to see if the files have the same spectrophotometer range
    def correct_ir_range(self, file_name, unknown_spectrum_name):
        spectrometer_range = self.get_range(unknown_spectrum_name)
        if spectrometer_range == '.vswir':
            if spectrometer_range in file_name:
                return True
        elif spectrometer_range == '.tir' or spectrometer_range == '.all':
            if '.vswir' not in file_name:
                return True
        else:
            return False

    def get_range(self, name):
        spectrometer_range = ''

        if '.vswir' in name:
            spectrometer_range = '.vswir'
        elif '.tir' in name:
            spectrometer_range = '.tir'
        elif '.all' in name:
            spectrometer_range = '.all'

        return spectrometer_range

    def add_similiarity_score(self, known_spectrum, score):
        difference_matrix[known_spectrum] = score

        pid = os.getpid
        print('Process {0} added score'.format(pid))

    def get_results(self, spectrum_name, difference_matrix):

        # convert dict to list
        spectra_hitlist = []
        for name, score in difference_matrix[spectrum_name].items():
            spectra_hitlist.append({'name': name, 'score': score, 'count': 0})

        compound = spectrum_name.split('.')[:5]
        for i in range(len(spectra_hitlist)):
            hitlist_compound = spectra_hitlist[i]['name'].split('.')

            similarity_count = 0
            for j in range(len(compound)):
                if compound[j] == hitlist_compound[j]:
                    similarity_count += 1
            spectra_hitlist[i]['count'] = similarity_count

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['count'], reverse=True)

        for i in range(len(spectra_hitlist)):
            if spectra_hitlist[i]['name'] == spectrum_name:
                spectra_hitlist.pop(i)
                break

        expected_closest = spectra_hitlist[0]['name']

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)

        for i in range(len(spectra_hitlist)):
            if expected_closest == spectra_hitlist[i]['name']:
                if i > 0:
                    self.missed_spectrum.append([self.comparison_type, spectrum_name, i])

                    self.log_info('{0}: {1} is closest to: {2} w/ score: {3:.3f}'.format(self.comparison_type, spectrum_name, spectra_hitlist[0]['name'], spectra_hitlist[0]['score']), Fore.RED)
                    self.log_info('Actual closest compound, {0}, was {1} spectrum from closest\n'.format(expected_closest, i), Fore.RED)
                    self.add_classification_results(spectrum_name, spectra_hitlist[0]['name'])
                else:
                    print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)
                    self.classification_level[4] += 1

    def accuracy(self):
        missed_categories = {'manmade': [0,0], 'meteorites': [0,0], 'mineral': [0,0], 'nonphotosyntheticvegetation': [0,0], 'rock': [0,0], 'soil': [0,0], 'vegetation': [0,0], 'water':[0,0]}
        average_miss = 0

        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            for entry in self.missed_spectrum:
                average_miss += entry[2]

                # this section is used to get the tally of each spectrum misclassified in a certain class
                spectrum_type = entry[1].split('.')[0]
                if spectrum_type in missed_categories.keys():
                    missed_categories[spectrum_type][0] += 1
                    missed_categories[spectrum_type][1] += entry[2]

            average_miss /= len(self.missed_spectrum)

        self.log_info('Total Spectrum Misclassified {0}'.format(len(self.missed_spectrum)), color)
        self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)

        accuracy = 1 - (len(self.missed_spectrum) / len(self.difference_matrix) * 100)
        self.heatmap.write('({0}, {1})\n'.format(accuracy, average_miss))

        for category in missed_categories.keys():
            self.log_info('{0} Spectrum Misclassified {1}'.format(category, missed_categories[category][0]), color)

            average_miss = 0
            if missed_categories[category][0] > 0:
                average_miss = missed_categories[category][1] / missed_categories[category][0]

            self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)

        for i in range(1, len(self.classification_level)):
            s = 'Calculcated Best Matches at Level {0}: {1}'.format(i, self.classification_level[i])
            self.log_info(s, Fore.YELLOW)

        s = 'Calculcated Best Matches that are not same type: {0}'.format(self.classification_level[i])
        self.log_info(s, Fore.YELLOW)

    def log_info(self, text, color):
        print(color + text + Style.RESET_ALL)
        self.results.write('\n' + text)

    def add_classification_results(self, unknown_spectrum, known_spectrum):
        unknown_spectrum = unknown_spectrum.split('.')
        known_spectrum = known_spectrum.split('.')

        if unknown_spectrum[0] != known_spectrum[0]:
            self.classification_level[0] += 1

        else:
            for i in range(1, 4):
                if unknown_spectrum[i] == known_spectrum[i]:
                    self.classification_level[i] += 1
