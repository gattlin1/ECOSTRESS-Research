import sys
import tensorflow as tf
from tensorflow.keras.models import load_model
import colorama
from colorama import Fore, Back, Style
import os
import os.path
from os import path
import cv2
import numpy as np

class Hitlist:
    def __init__(self, dataset, model_path, file_title=''):
        self.comparison_type = 'CNN'
        self.missed_spectrum = []
        self.dataset = dataset
        self.difference_matrix = {}
        self.classification_level = [0, 0, 0, 0, 0]
        self.model_path = model_path
        results_path = f'./results/nlc/{model_path.split("/")[-1]} {file_title}.txt'
        self.results = self.open_file(results_path)
        self.categories = ['non-match, match']

    def load_model(self, path):
        return load_model(path)

    def open_file(self, path):
        if not os.path.exists(path):
            open(path, 'x', errors='ignore')

        return open(path, 'a', errors='ignore')

    def find_matches(self):
        model = self.load_model(self.model_path)
        X, spectra_entries = [], []
        for pair, spectra_names in self.dataset:
            X.append(pair)
            spectra_entries.append(spectra_names)
        X = np.array(X)
        X = X / 255
        scores = model.predict_proba(X)

        for i in range(len(scores)):
            self.add_similiarity_score(spectra_entries[i][0], spectra_entries[i][1],
                scores[i][0])
        self.get_results()

    def add_similiarity_score(self, unknown_spectrum, known_spectrum, score):
        self.add_key(unknown_spectrum)
        self.add_key(known_spectrum)
        self.difference_matrix[unknown_spectrum][known_spectrum] = score
        self.difference_matrix[known_spectrum][unknown_spectrum] = score

    def add_key(self, name):
        if name not in self.difference_matrix:
            self.difference_matrix[name] = {}

    def get_results(self):
        for spectrum_name, entries in self.difference_matrix.items():
            spectra_hitlist = []
            for comp_spectrum_name, score in entries.items():
                spectra_hitlist.append({'name': comp_spectrum_name, 'score': score,
                    'count': 0})

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
                    self.log_info(f'{spectrum_name} ' \
                        f'is closest to: {spectra_hitlist[0]["name"]} ' \
                        f'w/ score: {spectra_hitlist[0]["score"]:.3f}', Fore.RED, False)
                    if i > 0:
                        self.missed_spectrum.append([spectrum_name, i])


                        self.log_info(f'Actual closest compound, {expected_closest},' \
                            f'was {i} spectrum from closest w/ score ' \
                            f'{spectra_hitlist[i]["score"]}\n', Fore.RED, False)
                    else:
                        pass
                        # print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)

                    self.add_classification_results(spectrum_name,
                        spectra_hitlist[0]['name'])

    def accuracy(self):
        missed_categories = {'manmade': [0,0], 'meteorites': [0,0], 'mineral': [0,0],
                             'nonphotosyntheticvegetation': [0,0], 'rock': [0,0],
                             'soil': [0,0], 'vegetation': [0,0], 'water':[0,0]}
        average_miss = 0

        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            for entry in self.missed_spectrum:
                average_miss += entry[1]

                # this section is used to get the tally of each spectrum misclassified in a certain class
                spectrum_type = entry[0].split('.')[0]
                if spectrum_type in missed_categories.keys():
                    missed_categories[spectrum_type][0] += 1
                    missed_categories[spectrum_type][1] += entry[1]

            average_miss /= len(self.missed_spectrum)

        self.log_info(f'Average Miss: {average_miss:.2f}\n', color, False)

        for category in missed_categories.keys():
            self.log_info(f'{category} Spectrum Misclassified {missed_categories[category][0]}', color, False)

            average_miss = 0
            if missed_categories[category][0] > 0:
                average_miss = missed_categories[category][1] / missed_categories[category][0]

            self.log_info(f'Average Miss: {average_miss:.2f}\n', color, False)

        self.log_info(f'Total Spectrum Misclassified {len(self.missed_spectrum)}', color, False)
        self.log_info(self.model_path, Fore.LIGHTMAGENTA_EX, True)
        for i in range(1, len(self.classification_level)):
            class_acc = self.classification_level[i] / len(self.difference_matrix)
            s = f'Calculcated Best Matches at Level {i}: {class_acc:.4f}'
            self.log_info(s, Fore.YELLOW, True)

        non_type_acc = self.classification_level[0] / len(self.difference_matrix)
        s = f'Calculcated Best Matches that are not same type: {non_type_acc:.4f}'
        self.log_info(s, Fore.YELLOW, True)

    def log_info(self, text, color, print_text):
        self.results.write('\n' + text)
        if print_text:
            print(color + text + Style.RESET_ALL)

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
