import math
import shutil
import os
import random

def make_ab_pairs(final_path):
    original_dataset_path = '../datasets/ecospeclib-all/'
    organized_path = '../datasets/ecospeclib-organized/'

    organize_data(original_dataset_path, organized_path)

    # ensures we start out with a new dataset
    if os.path.exists(final_path):
        shutil.rmtree(final_path)

    # if the dataset is not present then a directory is created for it
    if not os.path.exists(final_path):
        os.mkdir(final_path)

    subfolders = [ f.path for f in os.scandir(organized_path) if f.is_dir() ]
    for folder in subfolders:
        files = []

        for f in os.scandir(str(folder)):
            if f.is_dir():
                subfolders.append(f.path)
            else:
                files.append(f.path)

        if len(files) == 1:
            shutil.rmtree(folder, ignore_errors=True)

        elif len(files) >= 2:
            shutil.move(files[0], final_path)
            shutil.move(files[1], final_path)

        elif len(files) >= 3:
            random.shuffle(files)

            shutil.move(files[0], final_path)
            shutil.move(files[1], final_path)



def organize_data(directory_path, dest_path):
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            new_path = dest_path + '/'.join(file.split('.')[:5])
            split_file = file.split('.')[:5]

            for i in range(len(split_file) + 1):
                if not os.path.exists(dest_path + '/'.join(split_file[:i])):
                    os.mkdir(dest_path + '/'.join(split_file[:i]))
            shutil.copy(file_path, new_path)

f = '../datasets/ecospeclib-all/'
dest = '../cnn/spectrum_similarity/data/ecospeclib-raw/'

organize_data(f, dest)
