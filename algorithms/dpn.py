def dpn(spectra_1, spectra_2):
    min_length = min(len(spectra_1), len(spectra_2)) - 1
    spectra_1_mag = 0
    spectra_2_mag = 0
    dot_prod = 0

    for i in range(min_length):
        spectra_1_mag += spectra_1[i][1] ** 2
        spectra_2_mag += spectra_2[i][1] ** 2
        dot_prod += spectra_1[i][1] * spectra_2[i][1]

    spectra_1_mag **= 0.5
    spectra_2_mag **= 0.5

    if spectra_1_mag == 0 or spectra_2_mag == 0:
        return 0
    else:
        return dot_prod / (spectra_1_mag * spectra_2_mag)