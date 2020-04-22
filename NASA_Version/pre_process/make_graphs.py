from make_nasa_dataset import make_nasa_dataset
#from make_ab_pairs import organize_data
import multiprocessing
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import shutil
import datetime
import colorama
from colorama import Fore, Back, Style

def create_graphs(files, directory):
    pid = os.getpid()
    print(Fore.YELLOW + 'Process {0} starting w/ {1} files'.format(pid, len(files)) + Style.RESET_ALL)

    for file in files:
        file_name = file.split('/')[-1]
        split_file = file_name.split('.')[1:2]

        for i in range(0, len(split_file) + 1):
            new_dir = f'{directory}/{"/".join(split_file[:i])}'
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)

        dataset = make_nasa_dataset(file)
        dataset = pd.DataFrame(dataset, columns = ['Wavelength', 'Reflectance'])

        plt.figure(figsize=(3, .15))
        plt.plot(dataset['Wavelength'], dataset['Reflectance'])
        plt.axis('off')

        picture_path = f'{directory}/{"/".join(split_file)}/{file_name}.png'
        plt.savefig(picture_path, bbox_inches = 'tight', pad_inches = 0,
            facecolor='black', edgecolor='none', cmap='Blues_r')
        plt.close()

    print(Fore.GREEN + 'Process {0} finished w/ {1} files'.format(pid, len(files)) + Style.RESET_ALL)

if __name__=='__main__':
    start = datetime.datetime.now()

    vis_dir = '../cnn/class_classification/data/visualization-class'
    directory_path = '../datasets/ecospeclib-type/'

    if os.path.exists(vis_dir):
        shutil.rmtree(vis_dir)

    if not os.path.exists(vis_dir):
        os.mkdir(vis_dir)

    #files = [ f.path for f in os.scandir(directory_path) if f.name.endswith('.txt') and 'spectrum' in f.name]

    subfolders = [ f.path for f in os.scandir(directory_path) if f.is_dir() ]

    subsubfolders = []
    for folder in subfolders:
        for f in os.scandir(folder):
            if f.is_dir():
                subsubfolders.append(f.path)

    files = []
    for folder in subfolders:
        for file in os.listdir(folder):
            if file.endswith('.txt') and 'spectrum' in file:
                files.append(folder + '/' + file)

    core_count = multiprocessing.cpu_count()
    chunk_size = int(len(files) / core_count)

    # Serial
    #create_graphs(files, vis_dir)

    # Multiprocessing to create a hitlist for an entry
    processes = []
    for i in range(0, len(files), chunk_size):
        p = multiprocessing.Process(target=create_graphs, args=(files[i:i + chunk_size], vis_dir))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))