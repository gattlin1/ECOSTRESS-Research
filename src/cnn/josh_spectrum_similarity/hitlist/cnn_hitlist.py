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
        results_path = f'./results/{model_path.split("/")[-1]} {file_title}.txt'
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

    #TODO: figure out how to get accuracy and average hit fixed.
    def get_results(self):
        for spectrum_name, entries in self.difference_matrix.items():
            spectra_hitlist = []
            for comp_spectrum_name, score in entries.items():
                spectra_hitlist.append({'name': comp_spectrum_name, 'score': score})

            spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['count'],
                reverse=True)

            expected_closest = spectra_hitlist[0]['name']

            spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'],
                reverse=True)

            for i in range(len(spectra_hitlist)):
                if expected_closest == spectra_hitlist[i]['name']:
                    self.log_info(f'{spectrum_name} ' \
                        f'is closest to: {spectra_hitlist[0]["name"]} ' \
                        f'w/ score: {spectra_hitlist[0]["score"]:.3f}', Fore.RED, True)
                    if i > 0:
                        self.missed_spectrum.append([spectrum_name, i])


                        self.log_info(f'Actual closest compound, {expected_closest},' \
                            f'was {i} spectrum from closest w/ score ' \
                            f'{spectra_hitlist[i]["score"]}\n', Fore.RED, True)
                    else:
                        print(Fore.GREEN + 'Found the best match' + Style.RESET_ALL)

    def accuracy(self):
        average_miss = 0
        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
            for entry in self.missed_spectrum:
                average_miss += entry[1]

            average_miss /= len(self.missed_spectrum)

        self.log_info(f'Average Miss: {average_miss:.2f}\n', color, True)

        self.log_info(f'Total Spectrum Misclassified {len(self.missed_spectrum)}', color, True)
        self.log_info(self.model_path, Fore.LIGHTMAGENTA_EX, True)

    def log_info(self, text, color, print_text):
        self.results.write('\n' + text)
        if print_text:
            print(color + text + Style.RESET_ALL)

