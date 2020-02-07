import os
import sys

sys.path.append('../../../')
from algorithms.nlc import nlc
from algorithms.nlc_wavelength_partition import nlc_wavelength_range
from os import listdir
from os.path import isfile, join
from make_nasa_dataset import make_nasa_dataset
import datetime


def make_nlc_files(dataset_path, destination, floor_value=0.3, width=1.5):
    #start = datetime.datetime.now()
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
    #print('Total Runtime: {0}'.format(datetime.datetime.now() - start))

if __name__=='__main__':

    dataset_path = '../../ecospeclib-final/'
    nlc_dataset_path = '../../ecospeclib-final-nlc/'
    # Create NLC Versions of Dataset
    make_nlc_files(dataset_path, nlc_dataset_path)
