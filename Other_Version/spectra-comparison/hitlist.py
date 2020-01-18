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
from pre_process.make_dataset import make_dataset
from pre_process.spectra_point_matcher import match_points

class Hitlist:
    def __init__(self, algorithm):
        self.comparison_type = algorithm
        self.missed_spectrum = []

    def find_match(self, file_path, dir_path):
        unknown_spectrum = make_dataset(file_path)
        unknown_spectrum_name = file_path.split('/')
        unknown_spectrum_name = unknown_spectrum_name[len(unknown_spectrum_name) - 1]
        spectra_hitlist = []

        if 'nlc' in self.comparison_type:
            unknown_spectrum = nlc(unknown_spectrum, 9)

        for file in os.listdir(dir_path):
            if (file.endswith('.csv') and file != unknown_spectrum_name):
                spectrum_name = file.split('.')[0]
                known_spectrum = make_dataset(dir_path + file)

                # calculating similarity score and then adding it to hitlist
                known_spectrum = match_points(unknown_spectrum, known_spectrum)

                if 'nlc' in self.comparison_type:
                    known_spectrum = nlc(known_spectrum, 9)

                score = 0
                if 'cor' in self.comparison_type:
                    score = cor(unknown_spectrum, known_spectrum)
                elif 'dpn' in self.comparison_type:
                    score = dpn(unknown_spectrum, known_spectrum)
                elif 'mad' in self.comparison_type:
                    score = mad(unknown_spectrum, known_spectrum)
                elif 'msd' in self.comparison_type:
                    score = msd(unknown_spectrum, known_spectrum)

                spectra_hitlist.append({'name': spectrum_name, 'score': score})

        spectra_hitlist = sorted(spectra_hitlist, key = lambda i: i['score'], reverse=True)

        self.get_results(spectra_hitlist, self.comparison_type, unknown_spectrum_name.split('.')[0])

    def get_results(self, hitlist, title, expected_name):
        print('{0}: {1} is closest to: {2} w/ score: {3:.3f}'.format(title, expected_name, hitlist[0]['name'], hitlist[0]['score']))

        compound = expected_name[: len(expected_name) - 2]

        for i in range(len(hitlist)):
            hitlist_compound = hitlist[i]['name']
            hitlist_compound = hitlist_compound[: len(hitlist_compound) - 2]

            if compound == hitlist_compound:
                if i > 0:
                    self.missed_spectrum.append([title, expected_name, i])
                    print(Fore.RED + 'Actual closest compound was {0} spectrum from closest'.format(i) + Style.RESET_ALL)
                else:
                    print(Fore.GREEN + 'Found an exact match' + Style.RESET_ALL)

    def accuracy(self):
        color = Fore.GREEN
        if len(self.missed_spectrum) > 0:
            color = Fore.RED
        print(color + '\n{0} Spectrum Misclassified {1}'.format(self.comparison_type, len(self.missed_spectrum)) + Style.RESET_ALL)