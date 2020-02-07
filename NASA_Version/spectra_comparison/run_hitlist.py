import os
import datetime
from hitlist import Hitlist
from algorithms.nlc import nlc
from pre_process.make_nlc_files import make_nlc_files
import multiprocessing

# Creates a hitlist for the specified algorithm and gives it the path to
# the spectrum directory
def run_hitlist(algorithm, path):
    created_hitlist = Hitlist(algorithm, path)
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../ecospeclib-final/'
    nlc_dataset_path = '../ecospeclib-final-nlc/'

    # Create NLC Versions of Dataset
    make_nlc_files(dataset_path, nlc_dataset_path)

    processes = []
    hitlist_types = ['cor', 'dpn', 'mad', 'msd', 'nlc - cor', 'nlc - dpn', 'nlc - mad', 'nlc - msd']
    for alg in hitlist_types:
        if 'nlc' in alg:
            p = multiprocessing.Process(target=run_hitlist, args=(alg, nlc_dataset_path))
        else:
            p = multiprocessing.Process(target=run_hitlist, args=(alg, dataset_path))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))