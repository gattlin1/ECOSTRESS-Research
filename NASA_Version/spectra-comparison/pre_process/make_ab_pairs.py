import sys
sys.path.append('../../../')
import math
import shutil
import os
from algorithms.cor import cor
from make_nasa_dataset import make_nasa_dataset 

def move_file(destination, file):
    # file_split = file.split('ecospeclib-organized/')[1]
    # file_split = file_split.split('/')[:5]

    # for i in range(len(file_split) + 1):
    #     if not os.path.exists(destination + '/'.join(file_split[:i])):
    #         os.mkdir(destination + '/'.join(file_split[:i]))

    shutil.move(file, destination)

if __name__=='__main__':
    directory_path = '../../ecospeclib-organized/'
    dest_path = '../../ecospeclib-final/'

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    subfolders = [ f.path for f in os.scandir(directory_path) if f.is_dir() ]
    for folder in subfolders:
        folder = folder.replace('\\', '/')
        #print(folder)
        files = []
        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                files.append(f.path)
        if len(files) == 1:
            shutil.rmtree(folder, ignore_errors=True)

        elif len(files) == 2:
            for file in files:
                file = file.replace('\\', '/')
                move_file(dest_path, file)

        elif len(files) >= 3 :
            ab_pairs = []
            for file in files:
                file = file.replace('\\', '/')

                dataset = make_nasa_dataset(file)

                for other_file in files:
                    other_file = other_file.replace('\\', '/')
                    if file != other_file:
                        other_dataset = make_nasa_dataset(other_file)
                        score = cor(dataset, other_dataset)
                        pair = {'files': [file, other_file], 'score': score}

                        ab_pairs.append(pair)

            ab_pairs = sorted(ab_pairs, key = lambda i: i['score'], reverse=True)
        
            first_file = ab_pairs[0]['files'][0]
            second_file = ab_pairs[0]['files'][1]
            
            move_file(dest_path, first_file)
            move_file(dest_path, second_file)
            print('Moved files {0} & {1} w/ score:{2}'.format(first_file, second_file, ab_pairs[0]['score']))
