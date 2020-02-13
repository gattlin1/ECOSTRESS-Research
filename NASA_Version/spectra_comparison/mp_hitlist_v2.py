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
        self.correct_spectrum = []
        self.dataset_path = dataset_path
        self.classification_level = [0, 0, 0, 0, 0]

        results_path = '../results/6th_run/{0} results {1}.txt'.format(self.comparison_type, file_title)
        self.results = self.open_file(results_path)

        heatmap_path = '../results/6th_run/heatmap/{0} results.txt'.format(self.comparison_type)
        self.heatmap = self.open_file(heatmap_path)

    def open_file(self, path):
        if not os.path.exists(path):
            open(path, 'x', errors='ignore')

        return open(path, 'a', errors='ignore')

    def find_matches(self, files, full_hitlist):
        pid = os.getpid()
        count = 0
        comparison_count = 0
        for file in files:
            unknown_spectrum_name = file.split('/')
            unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
            unknown_spectrum = make_nasa_dataset(self.dataset_path + file)
            for other_file in os.listdir(self.dataset_path):
                if True:#self.correct_ir_range(other_file, unknown_spectrum_name):
                    unknown_spectrum_copy = deepcopy(unknown_spectrum)
                    known_spectrum = make_nasa_dataset(self.dataset_path + file)

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

                    entry = '{0},{1},{2}'.format(unknown_spectrum_name, other_file, score)
                    full_hitlist.append(entry)
                    comparison_count += 1
            count += 1
            if count == 67:
                print('Process {0} created hitlist #{1} w/ {2}'.format(pid, count, comparison_count))

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

    def get_results(self, difference_matrix):
        for spectrum_name in difference_matrix.keys():

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
                    else:
                        print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)
                        self.correct_spectrum.append([self.comparison_type, spectrum_name, i])
                    self.add_classification_results(spectrum_name, spectra_hitlist[0]['name'])

    def accuracy(self, difference_matrix):
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

        accuracy = (1 - len(self.missed_spectrum) / len(difference_matrix)) * 100
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

        s = 'Calculcated Best Matches that are not same type: {0}'.format(self.classification_level[0])
        self.log_info(s, Fore.YELLOW)

        #print('Amount of best matches {0}'.format(len(self.correct_spectrum)))

    def log_info(self, text, color):
        print(color + text + Style.RESET_ALL)
        self.results.write('\n' + text)

    def add_classification_results(self, unknown_spectrum, known_spectrum):
        unknown_spectrum = unknown_spectrum.split('.')
        known_spectrum = known_spectrum.split('.')

        if unknown_spectrum[0] != known_spectrum[0]:
            self.classification_level[0] += 1

        else:
            i = 1
            while unknown_spectrum[i] == known_spectrum[i] and i < len(self.classification_level):
                self.classification_level[i] += 1
                i += 1
