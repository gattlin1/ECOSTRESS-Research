import colorama
import os
from hitlist import Hitlist
import datetime
import random

def main():
    start = datetime.datetime.now()
    # initialize console color.
    colorama.init()

    # initialize hitlists for normal spectra comparison
    cor_hitlist = Hitlist('cor')
    dpn_hitlist = Hitlist('dpn')
    mad_hitlist = Hitlist('mad')
    msd_hitlist = Hitlist('msd')

    # loop through spectrum files in a directory and find matches in the hitlist
    directory_path = '../ecospeclib-final-v2/'
    a = os.listdir(directory_path)
    random.shuffle(a)
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            cor_hitlist.find_match(file_path, directory_path)
            dpn_hitlist.find_match(file_path, directory_path)
            mad_hitlist.find_match(file_path, directory_path)
            msd_hitlist.find_match(file_path, directory_path)

    cor_hitlist.accuracy()
    dpn_hitlist.accuracy()
    mad_hitlist.accuracy()
    msd_hitlist.accuracy()


        # initialize hitlists for normal spectra comparison and nlc.
    nlc_cor_hitlist = Hitlist('nlc - cor')
    nlc_dpn_hitlist = Hitlist('nlc - dpn')
    nlc_mad_hitlist = Hitlist('nlc - mad')
    nlc_msd_hitlist = Hitlist('nlc - msd')

    # loop through spectrum files in a directory and find matches in the hitlist
    directory_path = '../ecospeclib-all-nlc-v2/'
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            nlc_cor_hitlist.find_match(file_path, directory_path)
            nlc_dpn_hitlist.find_match(file_path, directory_path)
            nlc_mad_hitlist.find_match(file_path, directory_path)
            nlc_msd_hitlist.find_match(file_path, directory_path)

    nlc_cor_hitlist.accuracy()
    nlc_dpn_hitlist.accuracy()
    nlc_mad_hitlist.accuracy()
    nlc_msd_hitlist.accuracy()
    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))

main()