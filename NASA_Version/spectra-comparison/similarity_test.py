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

    # Nasa Dataset
    print(Fore.BLUE + '\nNASA DATASET' + Style.RESET_ALL)
    spectra1_path = '../ecospeclib-all/manmade.concrete.pavingconcrete.solid.all.0425uuuasp.jhu.becknic.spectrum.txt'
    spectra2_path = '../ecospeclib-all/manmade.concrete.pavingconcrete.solid.all.0397uuucnc.jhu.becknic.spectrum.txt'

    spectra_1 = make_nasa_dataset(spectra1_path)
    spectra_2 = make_nasa_dataset(spectra2_path)
    spectra_2 = match_points(spectra_1, spectra_2)

    similarity_results(mad(spectra_1, spectra_2), 'MAD')
    similarity_results(msd(spectra_1, spectra_2), 'MSD')
    similarity_results(dpn(spectra_1, spectra_2), 'DPN')
    similarity_results(cor(spectra_1, spectra_2), 'COR')

    nlc_1 = nlc(spectra_1, 10)
    nlc_2 = nlc(spectra_2, 10)
    similarity_results(mad(nlc_1, nlc_2), 'NLC -> MAD')
    similarity_results(msd(nlc_1, nlc_2), 'NLC -> MSD')
    similarity_results(dpn(nlc_1, nlc_2), 'NLC -> DPN')
    similarity_results(cor(nlc_1, nlc_2), 'NLC -> COR')
