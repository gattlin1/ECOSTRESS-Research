import os
import datetime
import time
from cnn_hitlist import Hitlist
import pickle
import shutil

if __name__=='__main__':
    start = datetime.datetime.now()
    model_dir = '../saved_models/'
    dataset_path = pickle.load(open('../data/pickles/Hitlist_Entries_2d.pickle', 'rb'))
    for file in os.listdir(model_dir):
        if file.endswith('.h5'):
            model_path = os.path.join(model_dir, file)
            # paths to spectrum directories
            results_name = str(datetime.datetime.now().strftime('%m-%d-%Y %Hhr %Mm %Ss'))

            created_hitlist = Hitlist(dataset_path, model_path, results_name)
            created_hitlist.find_matches()
            created_hitlist.accuracy()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))