import os
"""
    takes a file path to a dataset in csv form and converts it into a dataset
    @param file_path: file path to the dataset to be made
    @return: a list of lists to form the finished dataset
"""
def make_dataset(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            point = []
            line = line.strip('\n').split(',')
            for entry in line:
                point.append(float(entry))
            dataset.append(point)

    return dataset