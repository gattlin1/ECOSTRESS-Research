def nlc(spectrum, floor_value=0.3, width=9):
    floor(spectrum, floor_value)
    results = []

    for i in range(len(spectrum)):
        left_section, right_section = 0, 0
        for j in range(1, width + 1):
            if i - j >= 0:
                left_section += spectrum[i - j][1]
            if i + j < len(spectrum):
                right_section += spectrum[i + j][1]


        new_absorb = right_section / (left_section + right_section)

        results.append([spectrum[i][0] , new_absorb])

    return results

def floor(spectrum, multiplier):
    mean = get_mean(spectrum) * multiplier
    for entry in spectrum:
        if entry[1] < mean:
            entry[1] = mean

def get_mean(spectrum):
    mean = 0
    for entry in spectrum:
        mean += entry[1]

    return mean / len(spectrum)


