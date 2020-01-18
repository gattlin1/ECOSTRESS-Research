def mad(spectra_1, spectra_2):
    distance = 0

    for i in range(min(len(spectra_1), len(spectra_2))):
        distance += abs(spectra_1[i][1] - spectra_2[i][1])

    if distance == 0:
        return 1.0
    else:
        return 1 / distance