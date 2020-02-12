import os
import shutil
import datetime
from hitlist_multiprocessing import Hitlist
from algorithms.nlc import nlc
from pre_process.make_nlc_files import make_nlc_files
from pre_process.make_ab_pairs import make_ab_pairs
import multiprocessing
from multiprocessing import Manager
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Creates a hitlist for the specified algorithm and gives it the path to
# the spectrum directory
def make_hitlist(unknown_spectrum, files, difference_matrix):
    pid = os.getpid()
    print('Process {0} Starting w/ {1} files'.format(pid, len(files)))

    created_hitlist.find_matches(unknown_spectrum, files, difference_matrix)

def create_difference_matrix(dataset_path):
    difference_matrix = {}
    for file in os.listdir(dataset_path):
        if file.endswith('.txt') and 'spectrum' in file:
            difference_matrix[file] = {}

            for other_file in os.listdir(dataset_path):
                if other_file.endswith('.txt') and 'spectrum' in other_file:
                    difference_matrix[file][other_file] = 0

    return difference_matrix

if __name__=='__main__':
    start = datetime.datetime.now()

    dataset_path = '../ecospeclib-final/'
    nlc_dataset_path = '../ecospeclib-final-nlc/'
    alg = 'nlc - cor'
    floor_values = [0.3] #[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    wavelength_values = [0.5] #[0.2, 0.4, 0.6, 0.8, 1.0, 1.2]

    # Create Pairs
    #make_ab_pairs(dataset_path)

    run_count = 0

    # For loop to iterate through each
    for f_val in floor_values:
        for w_val in wavelength_values:

            # Create NLC Files for each hitlist
            #make_nlc_files(dataset_path, nlc_dataset_path, floor_value=f_val, width=w_val)

            created_hitlist = Hitlist(alg, nlc_dataset_path, file_title=run_count)
            run_count += 1

            difference_matrix = create_difference_matrix(nlc_dataset_path)

            files = [file for file in os.listdir(nlc_dataset_path) if file.endswith('.txt') and 'spectrum' in file]
            core_count = multiprocessing.cpu_count()
            chunk_size = int(len(files) / core_count)

            for file in files[:1]:
                unknown_spectrum = nlc_dataset_path + file

                # For running w/o multiprocessing
                # hitlist_dict = {}
                # for other_file in os.listdir(nlc_dataset_path):
                #     if file.endswith('.txt') and 'spectrum' in file:
                #         hitlist_dict[other_file] = 0
                # hitlist_dict[file] = 1

                # make_hitlist(unknown_spectrum, files, hitlist_dict)

                manager = multiprocessing.Manager()
                hitlist_dict = manager.dict()

                for other_file in os.listdir(nlc_dataset_path):
                    if file.endswith('.txt') and 'spectrum' in file:
                        hitlist_dict[other_file] = 0
                hitlist_dict[file] = 1

                # Multiprocessing to create a hitlist for an entry
                processes = []
                for i in range(0, len(files), chunk_size):
                    p = multiprocessing.Process(target=make_hitlist, args=(unknown_spectrum, files[i:i + chunk_size], hitlist_dict))
                    processes.append(p)
                    p.start()

                for process in processes:
                    process.join()
                print('In Parent Process')

                for key, value in hitlist_dict.items():
                    difference_matrix[file][key] = value
                    #print('key: {0} value: {1}'.format(key, value))

                created_hitlist.get_results(file, difference_matrix)



<<<<<<< HEAD
            # Start Multiprocessing
            processes = []
            hitlist_types = ['nlc - cor', 'nlc - dpn', 'nlc - mad', 'nlc - msd']
            for alg in hitlist_types:
                p = multiprocessing.Process(target=run_hitlist, args=(alg, nlc_dataset_path, i))
                processes.append(p)
                p.start()
=======
>>>>>>> 489060b9f5377a7e8a0041aa56ed1b606c0dd379



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