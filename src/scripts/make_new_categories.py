# Authors: Gattlin Walker

import matplotlib.pyplot as plt
import os
import random
import shutil

if __name__=='__main__':
    directory = '../../datasets/ecospeclib-all'
    dest = '../../datasets/ecospeclib-new-categories'
    rules = {
        'manmade.': {'exclusions': [
            'generalconstructionmaterial',
            'roofingmaterial',
            'reflectancetarget']},
        'mineral.': {'exclusions': []},
        'rock.igneous.': {'exclusions': ['intermediate', 'feslic']},
        'rock.metamorphic.': {'exclusions': []},
        'rock.sedimentary.': {'exclusions': ['carbonate']},
        'vegetation.': {'exclusions': []},
        'water': {'exclusions': []}
    }
    categories = {}
    dataset = []

    if os.path.exists(dest):
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        os.mkdir(dest)

    random.seed(3)

    for file in os.scandir(directory):
        if '.vswir.' not in file.name:
            for rule in rules.keys():
                substr = file.name.find(rule)
                if substr == 0:
                    excluded = False
                    for ex in rules[rule]['exclusions']:
                        if ex in file.name:
                            excluded = True
                            break
                    if not excluded:
                        file_name = file.name
                        if 'vegetation.' not in file_name and\
                            'water.' not in file_name:
                            file_name = file.name[substr + len(rule):]
                            split_path = []
                            if '.tir.' in file_name:
                                split_path = file_name[:file_name.find('.tir.')+4] \
                                .split('.')
                            else:
                                split_path = file_name[:file_name.find('.all.')+4] \
                                .split('.')

                            for i in range(len(split_path)):
                                new_path = os.path.join(dest,
                                    '/'.join(split_path[:i+1]))
                                if not os.path.exists(new_path):
                                    os.mkdir(new_path)

                            final_path = os.path.join(dest, '/'.join(split_path))
                            shutil.copy(file.path, final_path)
                            os.rename(os.path.join(final_path, file.name),
                                os.path.join(final_path, file_name))
