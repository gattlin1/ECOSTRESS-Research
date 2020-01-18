from ..pre_process.make_nasa_dataset import make_nasa_dataset

def nlc(spectra, width):
    floor(spectra, 0.3)
    results = []

    for i in range(len(spectra)):
        left_section = right_section = 0
        for j in range(1, width + 1):
            if i - j > 0:
                left_section += spectra[i - j][1]
            if i + j < len(spectra):
                right_section += spectra[i + j][1]
        new_absorb = right_section / (left_section + right_section)
        results.append([spectra[i][1] , new_absorb])

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

if __name__=='__main__':
    path = '../../ecospeclib-all/manmade.concrete.constructionconcrete.solid.all.0598uuucnc.jhu.becknic.spectrum.txt'
    spectrum = make_nasa_dataset(path)
    nlc(spectrum, 50)