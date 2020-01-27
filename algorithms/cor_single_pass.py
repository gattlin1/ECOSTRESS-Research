def cor(spectrum_1, spectrum_2):
    nominator, spectrum_1_sum, spectrum_2_sum = 0, 0, 0

    for i in range(len(spectrum_1)):
        nominator += spectrum_1[i][1] * spectrum_2[i][1]
        spectrum_1_sum += spectrum_1[i][1] ** 2
        spectrum_2_sum += spectrum_2[i][1] ** 2

    spectrum_1_avg = spectrum_1_sum / len(spectrum_1)
    spectrum_2_avg = spectrum_2_sum / len(spectrum_2)

    nominator -= len(spectrum_1) * spectrum_1_avg * spectrum_2_avg
    spectrum_1_sum -= (len(spectrum_1) * (spectrum_1_avg ** 2)) ** 0.5
    spectrum_2_sum -= (len(spectrum_2) * (spectrum_2_avg ** 2)) ** 0.5

    return nominator / (spectrum_1_sum * spectrum_2_sum)
