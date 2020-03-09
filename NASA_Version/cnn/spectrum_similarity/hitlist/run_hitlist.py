import os
import datetime
from cnn_hitlist import Hitlist
import shutil

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../data/visualization-similarity'

    created_hitlist = Hitlist(dataset_path, '')
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))