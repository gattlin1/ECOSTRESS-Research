import sys
sys.path.append('../../')
import colorama
from colorama import Fore, Back, Style
import pandas as pd
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc
from pre_process.make_dataset import make_dataset
from pre_process.make_nasa_dataset import make_nasa_dataset
from pre_process.spectra_point_matcher import match_points

def similarity_results(spectra_score, alg_name):
    print('{0} Spectra score: {1}'.format(alg_name, spectra_score))


if __name__=='__main__':
    colorama.init()

    # Smaller Dataset Comparison
    print(Fore.YELLOW + 'Other DATASET' + Style.RESET_ALL)
    spectra1_path = '../spectra/79-09-4_a.csv'
    spectra2_path = '../spectra/79-09-4_b.csv'

    spectra_1 = make_dataset(spectra1_path)
    spectra_2 = make_dataset(spectra2_path)
    spectra_2 = match_points(spectra_1, spectra_2)

    similarity_results(mad(spectra_1, spectra_2), 'MAD')
    similarity_results(msd(spectra_1, spectra_2), 'MSD')
    similarity_results(dpn(spectra_1, spectra_2), 'DPN')
    similarity_results(cor(spectra_1, spectra_2), 'COR')