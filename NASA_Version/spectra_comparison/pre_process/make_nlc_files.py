import os
import sys

sys.path.append('../../../')
from algorithms.nlc import nlc
from algorithms.nlc_wavelength_partition import nlc_wavelength_range
from os import listdir
from os.path import isfile, join
from pre_process.make_nasa_dataset import make_nasa_dataset
import multiprocessing
import shutil
import datetime

def nlc_process(files, dataset_path, destination, floor_value, width, process_number):
    # loop through spectrum files in a directory and find matches in the hitlist
    for file in files:
        if file.endswith('.txt') and 'spectrum' in file:
            spectrum = make_nasa_dataset(dataset_path + file)
            #spectrum = nlc(spectrum, floor_value=floor_value, width=width)
            spectrum = nlc_wavelength_range(spectrum, floor_value=floor_value, width=width)

            with open(destination + '/{0}'.format(file), mode='wt', encoding='utf-8') as myfile:
                for wavelength, reflectance in spectrum:
                    myfile.write('{0}\t {1}\n'.format(wavelength, reflectance))
        #print('process {0} finished file'.format(process_number))
    print('FINISHED --------------------  PROCESS {0} w/ {1}'.format(process_number, len(files)))

def make_nlc_files(dataset_path, destination, floor_value, width):
    start = datetime.datetime.now()

    # ensures we start out with a new dataset
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # creates destination if it does not already exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    files = [file for file in os.listdir(dataset_path) if file.endswith('.txt') and 'spectrum' in file]
    core_count = multiprocessing.cpu_count()
    chunk_size = int(len(files) / core_count)

    #nlc_process(files, dataset_path, destination, floor_value, width, 2)
    
    processes = []
    j = 0
    for i in range(0, len(files), chunk_size):
        j += 1
        p = multiprocessing.Process(target=nlc_process, args=(files[i:i + chunk_size], dataset_path, destination, floor_value, width, j))
        processes.append(p)
        p.start()

    for process in processes:
        process.join()

    print('Total Runtime: {0}'.format(datetime.datetime.now() - start))

if __name__=='__main__':
    d = '../../ecospeclib-final/'
    s = '../../ecospeclib-final-nlc-wavelength/'
    make_nlc_files(d, s, 0.3, 0.2)
    