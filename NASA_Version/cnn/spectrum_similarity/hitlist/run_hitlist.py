import os
import datetime
import time
from cnn_hitlist import Hitlist
import pickle
import shutil

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = X = pickle.load(open('../data/Hitlist_Entries_2d.pickle', 'rb'))
    model_path = '../saved_models/2d-sequential.h5'
    results_name = str(datetime.datetime.now().strftime('%m-%d-%Y %Hhr %Mm %Ss'))

    created_hitlist = Hitlist(dataset_path, model_path, results_name)
    created_hitlist.find_matches()
    created_hitlist.accuracy()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))