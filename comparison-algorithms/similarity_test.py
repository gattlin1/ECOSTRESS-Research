import pandas as pd
from algorithms.mad import mad
from algorithms.msd import msd
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.nlc import nlc

"""
    Used for similarity based algorithms like COR and DPN
"""
def similarity_results(spectra_score, alg_name):
    print('{0} Spectra score: {1}'.format(alg_name, spectra_score))


if __name__=='__main__':
    spectra1_path = '../spectra/79-09-4_a.csv'
    spectra2_path = '../spectra/79-09-4_b.csv'

    spectra_1 = pd.read_csv(spectra1_path, names=['Wavenumber', 'Absorbance'], header=None)
    spectra_2 = pd.read_csv(spectra2_path, names=['Wavenumber', 'Absorbance'], header=None)

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

