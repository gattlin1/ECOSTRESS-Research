import shutil
import os

if __name__=='__main__':
    directory_path = '../../ecospeclib-organized/'
    dest_path = '../../ecospeclib-final/'

    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    subfolders = [ f.path for f in os.scandir(directory_path) if f.is_dir() ]
    for folder in subfolders:
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
                file_split = file.split('ecospeclib-organized/')[1]
                file_split = file_split.split('/')[:5]

                for i in range(len(file_split) + 1):
                    if not os.path.exists(dest_path + '/'.join(file_split[:i])):
                        os.mkdir(dest_path + '/'.join(file_split[:i]))

                shutil.move(file, dest_path + '/'.join(file_split))

        elif len(files) >= 3:
            print(folder)
