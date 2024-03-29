import sys
sys.path.append('../')

import datetime
import colorama
from colorama import Fore, Back, Style
import os
from os import path
from lib.lib import cor, dpn, mad, msd, create_spectrum, match_points
from copy import deepcopy

class Hitlist:
    def __init__(self, algorithm, dataset_path, results_path):
        self.comparison_type = algorithm
        self.missed_spectrum = []
        self.dataset_path = dataset_path
        self.difference_matrix = self.create_difference_matrix()
        self.classification_level = [0, 0, 0, 0, 0]
        self.results, self.heatmap = self.setup_results(algorithm, results_path)

    def setup_results(self, algorithm, path):
        results_path = f'./results/{path}/{algorithm}.txt'
        results = self.open_file(results_path)

        heatmap_path = f'./results/{path}/heatmap/{algorithm} heatmap.txt'
        heatmap = self.open_file(heatmap_path)
        return results, heatmap


    def open_file(self, path):
        if not os.path.exists(path):
            open(path, 'x', errors='ignore')
        return open(path, 'a', errors='ignore')

    def create_difference_matrix(self):
        difference_matrix = {}
        for file in os.listdir(self.dataset_path):
            if file.endswith('.txt') and 'spectrum' in file:
                difference_matrix[file] = {}

                for other_file in os.listdir(self.dataset_path):
                    if other_file.endswith('.txt') and 'spectrum' in other_file:
                        difference_matrix[file][other_file] = 0
                difference_matrix[file][file] = 1

        return difference_matrix

    def run_spectra(self):
        # loop through spectrum files in a directory and find matches in the hitlist
        for file in os.listdir(self.dataset_path):
            if file.endswith('.txt') and 'spectrum' in file:
                file_path = self.dataset_path + file
                self.find_matches(file_path, self.dataset_path)

    def find_matches(self, file_path, dir_path):
        unknown_spectrum_name = file_path.split('/')
        unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]

        unknown_spectrum = create_spectrum(file_path)

        for file in os.listdir(dir_path):
            if self.valid_spectrum_file(file, unknown_spectrum_name):
                unknown_spectrum_copy = deepcopy(unknown_spectrum)
                known_spectrum = create_spectrum(dir_path + file)

                # calculating similarity score and then adding it to hitlist
                unknown_spectrum_copy, known_spectrum = match_points(
                    unknown_spectrum_copy, known_spectrum, 1.0)

                score = 0
                if 'cor' in self.comparison_type:
                    score = cor(unknown_spectrum_copy, known_spectrum)
                elif 'dpn' in self.comparison_type:
                    score = dpn(unknown_spectrum_copy, known_spectrum)
                elif 'mad' in self.comparison_type:
                    score = mad(unknown_spectrum_copy, known_spectrum)
                elif 'msd' in self.comparison_type:
                    score = msd(unknown_spectrum_copy, known_spectrum)

                self.add_similiarity_score(unknown_spectrum_name, file, score)

        self.get_results(unknown_spectrum_name)


    def valid_spectrum_file(self, file_name, unknown_spectrum_name):
        if not file_name.endswith('.txt'):
            return False
        if 'spectrum' not in file_name:
            return False
        if not self.uncalculated_spectra_pair(file_name, unknown_spectrum_name):
            return False
        if not self.correct_ir_range(file_name, unknown_spectrum_name):
            return False

        return True

    def uncalculated_spectra_pair(self, file_name, unknown_spectrum_name):
        if self.difference_matrix[file_name][unknown_spectrum_name] == 0:
            return True

        if self.difference_matrix[unknown_spectrum_name][file_name] == 0:
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

    def add_similiarity_score(self, unknown_spectrum, known_spectrum, score):
        self.difference_matrix[unknown_spectrum][known_spectrum] = score
        self.difference_matrix[known_spectrum][unknown_spectrum] = score

    def get_results(self, spectrum_name):

        # convert dict to list
        spectra_hitlist = []
        for name, score in self.difference_matrix[spectrum_name].items():
            spectra_hitlist.append({'name': name, 'score': score, 'count': 0})

        compound = spectrum_name.split('.')[:5]
        for i in range(len(spectra_hitlist)):
            hitlist_compound = spectra_hitlist[i]['name'].split('.')

            similarity_count = 0
            j = 0
            while j < len(compound) and compound[j] == hitlist_compound[j]:
                similarity_count += 1
                j += 1

            spectra_hitlist[i]['count'] = similarity_count

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['count'],
            reverse=True)

        for i in range(len(spectra_hitlist)):
            if spectra_hitlist[i]['name'] == spectrum_name:
                spectra_hitlist.pop(i)
                break

        expected_closest = spectra_hitlist[0]['name']

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'],
            reverse=True)

        for i in range(len(spectra_hitlist)):
            if expected_closest == spectra_hitlist[i]['name']:
                if i > 0:
                    self.missed_spectrum.append([self.comparison_type,
                        spectrum_name, i])

                    self.log_info(f'{self.comparison_type}: {spectrum_name} ' \
                        f'is closest to: {spectra_hitlist[0]["name"]} w/ score: ' \
                        f'{spectra_hitlist[0]["score"]:.3f}', Fore.RED)
                    self.log_info(f'Actual closest compound, {expected_closest},' \
                        f' was {i} spectrum from closest\n'.format(expected_closest, i), Fore.RED)
                else:
                    print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)

                self.add_classification_results(spectrum_name,
                    spectra_hitlist[0]['name'])

    def accuracy(self):
        missed_categories = {'manmade': [0,0], 'meteorites': [0,0],
                             'mineral': [0,0], 'nonphotosyntheticvegetation': [0,0],
                             'rock': [0,0], 'soil': [0,0], 'vegetation': [0,0],
                             'water':[0,0]}
        average_miss = 0

        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            for entry in self.missed_spectrum:
                average_miss += entry[2]

                # this section is used to get the tally of each
                # spectrum misclassified in a certain class
                spectrum_type = entry[1].split('.')[0]
                if spectrum_type in missed_categories.keys():
                    missed_categories[spectrum_type][0] += 1
                    missed_categories[spectrum_type][1] += entry[2]

            average_miss /= len(self.missed_spectrum)

        self.log_info(f'Total Spectrum Misclassified {self.missed_spectrum}',
            color)
        self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)

        accuracy = (1 - len(self.missed_spectrum) / len(self.difference_matrix))
        self.heatmap.write(f'{accuracy}, {average_miss}, {self.classification_level}\n')

        for category in missed_categories.keys():
            self.log_info(f'{category} Spectrum Misclassified ' \
                f'{missed_categories[category][0]}', color)

            average_miss = 0
            if missed_categories[category][0] > 0:
                average_miss = missed_categories[category][1] / missed_categories[category][0]

            self.log_info('Average Miss: {0:.2f}\n'.format(average_miss), color)

        for i in range(1, len(self.classification_level)):
            s = f'Calculcated Best Matches at Level {i}: {self.classification_level[i]}'
            self.log_info(s, Fore.YELLOW)

        s = f'Calculcated Best Matches that are not same type: {self.classification_level[0]}'
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
            i = 1
            while unknown_spectrum[i - 1] == known_spectrum[i - 1] and i < len(self.classification_level):
                self.classification_level[i] += 1
                i += 1
