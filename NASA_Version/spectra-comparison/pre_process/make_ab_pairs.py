import sys
sys.path.append('../../../')
import math
import shutil
import os
import random
from algorithms.cor import cor
from algorithms.dpn import dpn
from algorithms.mad import mad
from algorithms.msd import msd
from make_nasa_dataset import make_nasa_dataset

def move_file(destination, file):
    # file_split = file.split('ecospeclib-organized/')[1]
    # file_split = file_split.split('/')[:5]

    # for i in range(len(file_split) + 1):
    #     if not os.path.exists(destination + '/'.join(file_split[:i])):
    #         os.mkdir(destination + '/'.join(file_split[:i]))

    shutil.move(file, destination)

def generate_file_list(file_path):
    files = []
    with open(file_path, 'r') as file:
        files = [line.strip('\n').strip(' ') for line in file.readlines()]
        
    return files
        
        
def find_best_match(files, algorithm='cor'):
    ab_pairs = []
    for file in files:
        file = file.replace('\\', '/')

        dataset = make_nasa_dataset(file)

        for other_file in files:
            other_file = other_file.replace('\\', '/')
            if file != other_file:
                other_dataset = make_nasa_dataset(other_file)
                
                score = 0
                if algorithm == 'cor':
                    score = cor(dataset, other_dataset)
                elif algorithm == 'dpn':
                    score = dpn(dataset, other_dataset)
                elif algorithm == 'msd':
                    score = mad(dataset, other_dataset)
                elif algorithm == 'mad':
                    score = msd(dataset, other_dataset)

                pair = {'files': [file, other_file], 'score': score}

                ab_pairs.append(pair)

    ab_pairs = sorted(ab_pairs, key = lambda i: i['score'], reverse=True)

    first_file = ab_pairs[0]['files'][0]
    second_file = ab_pairs[0]['files'][1]

    move_file(dest_path, first_file)
    move_file(dest_path, second_file)

if __name__=='__main__':
    directory_path = '../../ecospeclib-organized/'
    dest_path = '../../ecospeclib-final-v2/'

    spectrum_to_ignore = generate_file_list('./spectrum_to_ignore.txt')
    msd_spectrum = generate_file_list('./special_cases.txt')

    print('Spectrum to ignore\n', spectrum_to_ignore)
    print('MSD Spectrum\n', msd_spectrum)

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    subfolders = [ f.path for f in os.scandir(directory_path) if f.is_dir() ]
    for folder in subfolders:
        folder.replace('\\', '/')
        files = []

        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                files.append(f.path)

        # handle file moving based on number of files in directory
        if len(files) == 1:
            shutil.rmtree(folder, ignore_errors=True)

        elif len(files) >= 2:
            valid_directory = True
            algorithm = 'cor'
            for entry in spectrum_to_ignore:
                if entry in files[0]:
                    valid_directory = False
            for entry in msd_spectrum:
                if entry in files[0]:
                    algorithm = 'mad'
            if valid_directory:
                if(algorithm == 'mad'):
                    print(algorithm)
                    print(files[0])
                find_best_match(files, algorithm=algorithm)
