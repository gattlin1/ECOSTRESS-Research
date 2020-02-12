import os
import shutil
import datetime
from hitlist import Hitlist
from algorithms.nlc import nlc
from pre_process.make_nlc_files import make_nlc_files
from pre_process.make_ab_pairs import make_ab_pairs
import multiprocessing
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Creates a hitlist for the specified algorithm and gives it the path to
# the spectrum directory
def run_hitlist(algorithm, path, file_title):
    created_hitlist = Hitlist(algorithm, path, file_title=file_title)
    created_hitlist.run_spectra()
    created_hitlist.accuracy()

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../ecospeclib-final/'
    nlc_dataset_path = '../ecospeclib-final-nlc/'

    # Create Pairs
    make_ab_pairs(dataset_path)
    
    # nlc arguments
    floor_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    wavelength_values = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    i = 1

    # For loop to iterate through each
    for f_val in floor_values:
        for w_val in wavelength_values:

            # Create NLC Files for each hitlist
            make_nlc_files(dataset_path, nlc_dataset_path, floor_value=f_val, width=w_val)

            # Start Multiprocessing
            processes = []
            hitlist_types = ['nlc - cor', 'nlc - dpn', 'nlc - mad', 'nlc - msd']
            for alg in hitlist_types:
                p = multiprocessing.Process(target=run_hitlist, args=(alg, nlc_dataset_path, i))
                processes.append(p)
                p.start()

            for process in processes:
                process.join()

            shutil.rmtree(nlc_dataset_path)

    # heatmap = []
    # for i in range(10):
    #     heatmap.append([i for i in range(200, 222, 2)])
    # heatmap = np.array(heatmap)

    # fig, ax = plt.subplots()
    # plt.title('NLC Heatmap')
    # im = ax.imshow(heatmap)

    # # We want to show all ticks...
    # ax.set_xticks(np.arange(len(floor_values)))
    # ax.set_yticks(np.arange(len(wavelength_values)))

    # # ... and label them with the respective list entries
    # ax.set_xlabel('Floor')
    # ax.set_xticklabels(floor_values)

    # ax.set_ylabel('Wavelength')
    # ax.set_yticklabels(wavelength_values)

    # # Rotate the tick labels and set their alignment.
    # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
    #         rotation_mode="anchor")

    # # Loop over data dimensions and create text annotations.
    # for i in range(len(floor_values)):
    #     for j in range(len(heatmap)):
    #         text = ax.text(j, i, heatmap[i, j],
    #                     ha="center", va="center", color="w")

    # ax.set_title('NLC ACCURACY HEATMAP')
    # fig.tight_layout()
    # plt.savefig(plt.savefig('./temp.png')) #! ADD PATH LATER

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))