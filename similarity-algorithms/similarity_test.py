import pandas as pd
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc

"""
    Used for the difference based algorithms like MAD and MSD
"""
def difference_results(spectra1_score, spectra2_score, alg_name):
    print(alg_name)
    print('Spectra 1 score: {0}'.format(spectra1_score))
    print('Spectra 2 score: {0}'.format(spectra2_score))
    print('Difference between two spectra: {0}'.format(abs(spectra1_score - spectra2_score)))
    print()

"""
    Used for similarity based algorithms like COR and DPN
"""
def similarity_results(spectra_score, alg_name):
    print(alg_name)
    print('Spectra score: {0}'.format(spectra_score))
    print()


if __name__=='__main__':
    spectra1_path = '../spectra/79-09-4_a.csv'
    spectra2_path = '../spectra/79-09-4_b.csv'

    spectra_1 = pd.read_csv(spectra1_path, names=['Wavenumber', 'Absorbance'], header=None)
    spectra_2 = pd.read_csv(spectra2_path, names=['Wavenumber', 'Absorbance'], header=None)

    difference_results(mad(spectra_1), mad(spectra_2), 'MAD')
    difference_results(msd(spectra_1), msd(spectra_2), 'MSD')

    similarity_results(dpn(spectra_1, spectra_2), 'DPN')
    similarity_results(cor(spectra_1, spectra_2), 'COR')

    nlc_1 = nlc(spectra_1, 10)
    nlc_2 = nlc(spectra_2, 10)
    similarity_results(dpn(nlc_1, nlc_2), 'NLC -> DPN')
    similarity_results(cor(nlc_1, nlc_2), 'NLC -> COR')

