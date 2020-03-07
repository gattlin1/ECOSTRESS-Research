from make_nasa_dataset import make_nasa_dataset
import multiprocessing
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
        split_file = file.replace('\\', '/').split('/')
        file_name = split_file[len(split_file) - 1]
        split_file = split_file[len(split_file) - 1].split('.')[:5]

        for i in range(1, len(split_file) + 1):
            if not os.path.exists(directory + '/'.join(split_file[:i])):
                os.mkdir(directory + '/'.join(split_file[:i]))

        dataset = make_nasa_dataset(file)
        dataset = pd.DataFrame(dataset, columns = ['Wavelength', 'Reflectance'])

        plt.figure(figsize=(3, .15))
        plt.plot(dataset['Wavelength'], dataset['Reflectance'])
        plt.axis('off')

        plt.savefig(directory + '/'.join(split_file) + '/' + file_name + '.png', bbox_inches = 'tight', pad_inches = 0)
        plt.close()

    print(Fore.GREEN + 'Process {0} finished w/ {1} files'.format(pid, len(files)) + Style.RESET_ALL)

if __name__=='__main__':
    start = datetime.datetime.now()

    vis_dir = '../../cnn/spectrum_similarity/data/visualization-similarity/'
    data_dir = '../../ecospeclib-organized/'

    if os.path.exists(vis_dir):
        shutil.rmtree(vis_dir)

    if not os.path.exists(vis_dir):
        os.mkdir(vis_dir)

    subfolders = [ f.path for f in os.scandir(data_dir) if f.is_dir() ]
    files = []
    for folder in subfolders:

        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                files.append(f.path)


    core_count = multiprocessing.cpu_count()
    chunk_size = int(len(files) / core_count)

    # # Serial
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