import pickle
import os
import matplotlib.pyplot as plt
import pandas as pd

if __name__=='__main__':
    directory = './training-graphs'
    dataset = pickle.load(open('./specjar.pickle', 'rb'))

    if not os.path.exists(directory):
        os.mkdir(directory)

    for compound_type, samples in dataset.items():
        if len(samples.keys()) > 1:
            compound_path = f'{directory}/{compound_type}'
            if not os.path.exists(compound_path):
                os.mkdir(compound_path)

            for sample, data in samples.items():
                dataset = pd.DataFrame(data, columns = ['Wavelength', 'Reflectance'])

                plt.figure(figsize=(3, .15))
                plt.plot(dataset['Wavelength'], dataset['Reflectance'])
                plt.axis('off')

                picture_path = f'{compound_path}/{sample}.png'
                plt.savefig(picture_path, bbox_inches = 'tight', pad_inches = 0,
                    facecolor='black', edgecolor='none', cmap='Blues_r')
                plt.close()