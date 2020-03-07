import matplotlib.pyplot as plt
import pandas as pd

def nlc_wavelength_range(spectra, floor_value=0.3, width=1.5):
    floor(spectra, floor_value)
    results = []

    for i in range(len(spectra)):
        left_section = {'sum': 0, 'count': 0}
        right_section = {'sum': 0, 'count': 0}

        j = 1
        in_bounds = True
        while i - j >= 0 and in_bounds:
            if abs(spectra[i][0] - spectra[i - j][0]) <= width:
                left_section['sum'] += spectra[i - j][1]
                left_section['count'] += 1
            else:
                in_bounds = False
            j += 1

        j = 1
        in_bounds = True
        while i + j < len(spectra) and in_bounds:
            if abs(spectra[i][0] - spectra[i + j][0]) <= width:
                right_section['sum'] += spectra[i + j][1]
                right_section['count'] += 1
            else:
                in_bounds = False
            j += 1

        if right_section['count'] == 0:
            right_section['average'] = 0
        else:
            right_section['average'] = right_section['sum'] / right_section['count']
        if left_section['count'] == 0:
            left_section['average'] = 0
        else:
            left_section['average'] = left_section['sum'] / left_section['count']

        new_absorb = 0
        if right_section['average'] != 0 or left_section['average'] != 0:
            new_absorb = right_section['average'] / (left_section['average'] + right_section['average'])

        results.append([spectra[i][0] , new_absorb])

    return results

def floor(spectra, multiplier):
    mean = get_mean(spectra) * multiplier
    for entry in spectra:
        if entry[1] < mean:
            entry[1] = mean

def get_mean(spectra):
    mean = 0
    for entry in spectra:
        mean += entry[1]

    return mean / len(spectra)

# if __name__=='__main__':
#     path = '../../ecospeclib-all/manmade.concrete.constructionconcrete.solid.all.0598uuucnc.jhu.becknic.spectrum.txt'
#     spectrum = make_nasa_dataset(path)
#     nlc_wave = nlc_wavelength_range(spectrum, 1.5)
#     nlc_index = nlc(spectrum, 9)


#     dataset = pd.DataFrame(nlc_wave, columns = ['Wavelength', 'Reflectance'])

#     plt.figure(figsize=(12, 6))
#     plt.plot(dataset['Wavelength'], dataset['Reflectance'])
#     plt.title('file')
#     plt.ylabel('Reflectance')
#     plt.xlabel('Wavelength')
#     plt.savefig( './wave.png')

#     dataset = pd.DataFrame(nlc_index, columns = ['Wavelength', 'Reflectance'])

#     plt.figure(figsize=(12, 6))
#     plt.plot(dataset['Wavelength'], dataset['Reflectance'])
#     plt.title('file')
#     plt.ylabel('Reflectance')
#     plt.xlabel('Wavelength')
#     plt.savefig( './index.png')
