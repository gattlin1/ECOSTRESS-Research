import shutil
import os

if __name__=='__main__':
    src = '../../ecospeclib-organized/'
    directory_path = '../../ecospeclib-all/'
    for file in os.listdir(directory_path):
        if file.endswith('.txt') and 'spectrum' in file:
            file_path = directory_path + file
            new_path = src + '/'.join(file.split('.')[:5])
            split_file = file.split('.')[:5]

            for i in range(len(split_file) + 1):
                if not os.path.exists(src + '/'.join(split_file[:i])):
                    os.mkdir(src + '/'.join(split_file[:i]))
            shutil.copy(file_path, new_path)
