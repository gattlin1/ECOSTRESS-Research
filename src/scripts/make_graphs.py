# Authors: Gattlin Walker
# A script to generate a matplotlib graph of every spectrum file in the
# ECOSTRESS dataset. The graphs are then saved in the datasets directory. This
# program utilized multiprocessing to speed up the process since there are
# several thousand files.

import sys
sys.path.append('../')

from lib.lib import create_spectrum
import multiprocessing as mp
import os
import matplotlib.pyplot as plt
import shutil
import datetime
import colorama
from colorama import Fore, Back, Style

def create_graphs(files, directory):
    pid = os.getpid()
    print(Fore.YELLOW + f'Process {pid} starting w/ {len(files)} files')

    for file in files:
        file_name = file.split('/')[-1]
        split_file = file_name.split('.')[:0]

        for i in range(0, len(split_file) + 1):
            new_dir = f'{directory}/{"/".join(split_file[:i])}'
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)

        spectrum = create_spectrum(file)
        x_vals = [x[0] for x in spectrum]
        y_vals = [y[1] for y in spectrum]

        plt.figure(figsize=(3, .15))
        plt.plot(x_vals, y_vals)
        plt.axis('off')

        picture_path = f'{directory}/{"/".join(split_file)}/{file_name}.png'
        plt.savefig(picture_path, bbox_inches = 'tight', pad_inches = 0,
            facecolor='black', edgecolor='none', cmap='Blues_r')
        plt.close()

    print(Fore.GREEN + f'Process {pid} finished w/ {len(files)} files')

if __name__=='__main__':
    start = datetime.datetime.now()
    vis_dir = '../../datasets/ecospeclib-graphs/'
    directory_path = '../../datasets/ecospeclib-all/'

    if os.path.exists(vis_dir):
        shutil.rmtree(vis_dir)

    if not os.path.exists(vis_dir):
        os.mkdir(vis_dir)

    folders = [directory_path]
    files = []
    for folder in folders:
        folder_files = []
        for f in os.scandir(str(folder)):
            if f.is_dir():
                folders.append(f.path)
            elif 'spectrum' in f.path:
                folder_files.append(f.path)
        files += folder_files

    core_count = mp.cpu_count()
    chunk_size = int(len(files) / core_count)

    # Serial
    # create_graphs(files, vis_dir)

    processes = []
    for i in range(0, len(files), chunk_size):
        p = mp.Process(
            target=create_graphs,
            args=(files[i: i+chunk_size],
            vis_dir))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))
