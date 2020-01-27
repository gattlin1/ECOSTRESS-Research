import colorama
import os
import sys
sys.path.append('../../../')
from algorithms.nlc import nlc
from os import listdir
from os.path import isfile, join
import shutil
from make_nasa_dataset import make_nasa_dataset


def main():
    path = os.getcwd() + '/ecospeclib-all-nlc'

    if not os.path.exists(path):
        os.mkdir(path)

    # loop through spectrum files in a directory and find matches in the hitlist
    directory_path = '../../ecospeclib-all/'
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            spectrum = make_nasa_dataset(file_path)
            spectrum = nlc(spectrum, 9)

            with open(path + '/{0}'.format(file) , mode='wt', encoding='utf-8') as myfile:
                for wavelength, reflectance in spectrum:
                    myfile.write('{0} {1}\n'.format(wavelength, reflectance))

main()