from algorithms.nlc import nlc
from algorithms.nlc_wavelength_partition import nlc_wavelength_range
from NASA_Version.spectra_comparison.pre_process.make_nasa_dataset import make_nasa_dataset
import matplotlib.pyplot as plt
import pandas as pd

if __name__=='__main__':
    path = './NASA_Version/ecospeclib-final-v2/manmade.generalconstructionmaterial.brick.solid.all.0412uuubrk.jhu.becknic.spectrum.txt'
    spectrum = make_nasa_dataset(path)
    nlc_wave = nlc_wavelength_range(spectrum, .2)
    nlc_index = nlc(spectrum, 9)


    dataset = pd.DataFrame(nlc_wave, columns = ['Wavelength', 'Reflectance'])

    plt.figure(figsize=(12, 6))
    plt.plot(dataset['Wavelength'], dataset['Reflectance'])
    plt.title('file')
    plt.ylabel('Reflectance')
    plt.xlabel('Wavelength')
    plt.savefig( './wave.png')

    dataset = pd.DataFrame(nlc_index, columns = ['Wavelength', 'Reflectance'])

    plt.figure(figsize=(12, 6))
    plt.plot(dataset['Wavelength'], dataset['Reflectance'])
    plt.title('file')
    plt.ylabel('Reflectance')
    plt.xlabel('Wavelength')
    plt.savefig( './index.png')
