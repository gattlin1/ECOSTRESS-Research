import os
import shutil
import datetime
from lib.lib import nlc
from hitlist import Hitlist
from scripts.make_nlc_files import make_nlc_files
from scripts.make_ab_pairs import make_ab_pairs
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

def generate_heatmaps(file_path, floor_values, wavelength_values, file_count):
    with open(file_path, 'r', errors='ignore') as file:
        entries = {'accuracy': [], 'avg miss': [], 'class lvl': []}
        for line in file.readlines():
            accuracy, avg_miss, class_lvl = line.split(sep=',', maxsplit=2)

            class_lvl = class_lvl.replace('[', '').replace(']', '').split(sep=',')
            accuracy = float(accuracy)
            avg_miss = float(avg_miss)
            class_lvl = [(float(lvl) / file_count * 100) for lvl in class_lvl]
            entries['accuracy'].append(accuracy)
            entries['avg miss'].append(avg_miss)
            entries['class lvl'].append(class_lvl)

    file_name = file_path.split('/')[4:][0].replace('heatmap.txt', '')

    accuracy_heatmap = np.array(entries['accuracy']).reshape(
        (len(floor_values), len(wavelength_values))).round(decimals=2)
    title = file_name + 'Best Match Accuracy'
    create_heatmap(title, np.rot90(accuracy_heatmap, k=1, axes=(0,1)),
        floor_values, wavelength_values)

    avg_miss_heatmap = np.array(entries['avg miss']).reshape(
        (len(floor_values), len(wavelength_values))).round(decimals=2)
    title = file_name + 'Average Best Match Miss'
    create_heatmap(title, np.rot90(avg_miss_heatmap, k=1, axes=(0,1)),
        floor_values, wavelength_values)

    class_lvl_heatmap = np.array(entries['class lvl'])
    for i in range(1, np.size(class_lvl_heatmap,1)):
        title = file_name + 'Accuracy at Level {0}'.format(i)
        lvl_heatmap = class_lvl_heatmap[:, i].reshape(
            (len(floor_values), len(wavelength_values)))
        print(np.rot90(lvl_heatmap.round(decimals=2)))

        create_heatmap(title, np.rot90(lvl_heatmap.round(decimals=2), k=1,
            axes=(0,1)), floor_values, wavelength_values)


def create_heatmap(title, heatmap, floor_values, wavelength_values):
    fig, ax = plt.subplots()
    plt.title(title)
    im = ax.imshow(heatmap)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(floor_values)))
    ax.set_yticks(np.arange(len(wavelength_values)))

    # ... and label them with the respective list entries
    ax.set_xlabel('Floor')
    ax.set_xticklabels(floor_values)

    ax.set_ylabel('Wavelength')
    ax.set_yticklabels(wavelength_values[::-1])

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(wavelength_values)):
        for j in range(len(floor_values)):
            text = ax.text(j, i, heatmap[i, j],
                        ha="center", va="center", color="w")

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig('../heatmaps/{0}.png'.format(title))
    plt.close()

if __name__=='__main__':
    start = datetime.datetime.now()

    # paths to spectrum directories
    dataset_path = '../ecospeclib-final/'
    nlc_dataset_path = '../ecospeclib-final-nlc/'

    # Create Pairs
    make_ab_pairs(dataset_path)

    # nlc arguments
    floor_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    wavelength_values = [0.2, 0.4, 0.6, 0.8, 1.0]
    i = 1

    # For loop to iterate through each
    for f_val in floor_values:
        for w_val in wavelength_values:

            # Create NLC Files for each hitlist
            make_nlc_files(dataset_path, nlc_dataset_path, floor_value=f_val,
                width=w_val)

            # Start Multiprocessing
            processes = []
            hitlist_types = ['nlc - cor', 'nlc - dpn', 'nlc - mad', 'nlc - msd']
            for alg in hitlist_types:
                p = multiprocessing.Process(target=run_hitlist,
                    args=(alg, nlc_dataset_path, i))
                processes.append(p)
                p.start()

            for process in processes:
                process.join()

            i += 1


    time = str(datetime.datetime.now().strftime('%m-%d-%Y %Hhr %Mm %Ss'))
    path = f'../results/{time}/heatmap/'
    file_count = len(list(os.listdir(nlc_dataset_path)))
    for file in os.listdir(path):
        generate_heatmaps(path + file, floor_values, wavelength_values, file_count)

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))