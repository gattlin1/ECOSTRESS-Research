# Authors: Gattlin Walker
# Runs a hitlist using each of the similarity algorithms with and without NLC
# Each algorithm is ran on a separate core so it is preferred if there are at
# least 8 cores running this program. Less than 8 cores might result in slower
# execution time.

import os
import datetime
from hitlist import Hitlist
import multiprocessing as mp
import shutil
from scripts.make_nlc_files import make_nlc_files
from scripts.make_ab_pairs import make_ab_pairs

# Creates a hitlist for the specified algorithm and gives it the path to
# the spectrum directory
def run_hitlist(algorithm, path, time):
    created_hitlist = Hitlist(algorithm, path, time)
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

if __name__=='__main__':
    start = datetime.datetime.now()
    time = start.strftime('%m-%d-%Y %Hhr %Mm %Ss')
    path = f'./results/{time}'
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(f'{path}/heatmap')


    # paths to spectrum directories
    dataset_path = '../../datasets/ecospeclib-final/'
    nlc_dataset_path = '../../datasets/ecospeclib-final-nlc/'

    # Setup Dataset
    make_ab_pairs(dataset_path)
    make_nlc_files(dataset_path, nlc_dataset_path, floor_value=0.3, width=0.5)

    # Sets up a hitlist for each algorithm on a separate process
    processes = []
    hitlist_types = ['cor', 'dpn', 'mad', 'msd', 'nlc - cor',
                     'nlc - dpn', 'nlc - mad', 'nlc - msd']
    for alg in hitlist_types:
        if 'nlc' in alg:
            p = mp.Process(target=run_hitlist,
                args=(alg, nlc_dataset_path, time))
        else:
            p = mp.Process(target=run_hitlist,
                args=(alg, dataset_path, time))

        processes.append(p)
        p.start()

    # joins all of the processes before continuing to the next iteration
    for process in processes:
        process.join()

    shutil.rmtree(dataset_path)
    shutil.rmtree(nlc_dataset_path)

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))
