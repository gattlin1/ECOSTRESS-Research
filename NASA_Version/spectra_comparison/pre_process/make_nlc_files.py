import os
from algorithms.nlc import nlc
from os import listdir
from os.path import isfile, join
from pre_process.make_nasa_dataset import make_nasa_dataset


def make_nlc_files(dataset_path, destination):

    # creates destination if it does not already exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    # loop through spectrum files in a directory and find matches in the hitlist
    for file in os.listdir(dataset_path):
        if file.endswith('.txt') and 'spectrum' in file:
            spectrum = make_nasa_dataset(dataset_path + file)
            spectrum = nlc(spectrum, 9)

            with open(destination + '/{0}'.format(file) , mode='wt', encoding='utf-8') as myfile:
                for wavelength, reflectance in spectrum:
                    myfile.write('{0}\t {1}\n'.format(wavelength, reflectance))
