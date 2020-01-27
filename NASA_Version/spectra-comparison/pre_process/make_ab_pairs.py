import colorama
import os
from os import listdir
from os.path import isfile, join
import shutil

def main():
    path = os.getcwd() + '/ecospeclib-all-no-ancillary'

    if not os.path.exists(path):
        os.mkdir(path)

    ab_pairs = {}

    # loop through spectrum files in a directory and find matches in the hitlist
    directory_path = '../../ecospeclib-all/'
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            # ab_pair = file.split('.')[:5]
            # ab_pair = '.'.join(ab_pair)
            # print(ab_pair)
            file_path = directory_path + file
            shutil.copy(file_path, path)

main()