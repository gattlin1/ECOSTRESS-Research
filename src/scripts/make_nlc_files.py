import os
import sys

sys.path.append('../')
from lib.lib import nlc, nlc_wavelength_range, create_spectrum
import os
import multiprocessing as mp
import shutil
import datetime

def nlc_process(files, dataset_path, destination, floor_value, width):
    pid = os.getpid()

    # loop through spectrum files in a directory and find matches in the hitlist
    for file in files:
        if file.endswith('.txt') and 'spectrum' in file:
            spectrum = create_spectrum(os.path.join(dataset_path, file))
            #spectrum = nlc(spectrum, floor_value=floor_value, width=width)
            spectrum = nlc_wavelength_range(
                spectrum,
                floor_value=floor_value,
                width=width)

            file_path = os.path.join(destination, file)
            with open(file_path, mode='wt', encoding='utf-8') as myfile:
                for wavelength, reflectance in spectrum:
                    myfile.write('{0}\t {1}\n'.format(wavelength, reflectance))
        #print('process {0} finished file'.format(process_number))
    print('FINISHED PROCESS {0} w/ {1}'.format(pid, len(files)))

def make_nlc_files(dataset_path, destination, floor_value, width):
    start = datetime.datetime.now()

    # ensures we start out with a new dataset
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # creates destination if it does not already exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    files = [file for file in os.listdir(dataset_path)
        if file.endswith('.txt') and 'spectrum' in file]

    core_count = mp.cpu_count()
    chunk_size = int(len(files) / core_count)
    
    # Serial Version
    #nlc_process(files, dataset_path, destination, floor_value, width, 2)

    # Multiprocessing Version
    processes = []
    j = 0
    for i in range(0, len(files), chunk_size):
        j += 1
        p = mp.Process(target=nlc_process, args=(files[i:i + chunk_size],
            dataset_path, destination, floor_value, width))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))

if __name__=='__main__':
    path = '../datasets/ecospeclib-all'
    dest = '../datasets/ecospeclib-nlc'
    make_nlc_files(path, dest, 0.3, 0.2)
