import os
import datetime
from hitlist_multiprocessing import Hitlist
from algorithms.nlc import nlc
import multiprocessing
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import shutil
from pre_process.make_nlc_files import make_nlc_files
from pre_process.make_ab_pairs import make_ab_pairs

# Creates a hitlist for the specified algorithm and gives it the path to
# the spectrum directory
def run_hitlist(algorithm, path, file_title):
    created_hitlist = Hitlist(algorithm, path, file_title)
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../ecospeclib-final/'
    nlc_dataset_path = '../ecospeclib-final-nlc/'

    for i in range(1):
        file_name = 'run {0}'.format(i)

        # Setup Dataset
        #make_ab_pairs(dataset_path)
        #make_nlc_files(dataset_path, nlc_dataset_path, floor_value=0.3, width=0.5)

        run_hitlist('cor', dataset_path, file_name)

        # shutil.rmtree(dataset_path)
        # shutil.rmtree(nlc_dataset_path)

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))