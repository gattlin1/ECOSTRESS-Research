import os
import datetime
import time
from cnn_hitlist import Hitlist
import shutil

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../data/visualization-similarity'

    created_hitlist = Hitlist(dataset_path, str(datetime.datetime.now().strftime('%Y%m%d-%H%M%S')))
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))