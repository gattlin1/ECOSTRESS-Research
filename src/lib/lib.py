# Author: Gattlin Walker
# Lib file that includes creating a spectrum, similarity algorithms,
# nlc pre-processing, and spectra point matching

import math

# Takes in a file and creates a spectrum from it
# @param file_path: file path of an ECOSTRESS spectrum file
# @return: the spectrum as a list of lists
def create_spectrum(file_path):
    spectrum = []
    with open(file_path, 'r', errors='ignore') as file:
        for line in file.readlines():
            if line.count(':') == 0 and line != '\n' and line != '\t\n':
                line = line.replace(' ', '').strip('\n').split('\t')
                line[0] = float(line[0])
                line[1] = float(line[1])
                spectrum.append([line[0], line[1]])

    return spectrum 

# Pearson Correlation Coefficient (cor)
# @param spectrum_1: The first spectrum to be compared
# @param spectrum_2: The second spectrum to be compared
# @return: the pearson correlation coefficient calculation. Does return 0 if the
# norm of either spectra is 0
def cor(spectrum_1, spectrum_2):
    avg1 = get_mean(spectrum_1)
    avg2 = get_mean(spectrum_2)
    nominator, norm_spectrum_1, norm_spectrum_2 = 0, 0, 0

    for i in range(min(len(spectrum_1), len(spectrum_2))):
        nominator += (spectrum_1[i][1] - avg1) * (spectrum_2[i][1] - avg2)
        norm_spectrum_1 += (spectrum_1[i][1] - avg1) ** 2
        norm_spectrum_2 += (spectrum_2[i][1] - avg2) ** 2

    norm_spectrum_1 **= 0.5
    norm_spectrum_2 **= 0.5

    if norm_spectrum_1 == 0 or norm_spectrum_2 == 0:
        return 0
    else:
        return nominator / (norm_spectrum_1 * norm_spectrum_2)

# Mean Squared Distance (msd)
# @param spectrum_1: The first spectrum to be compared
# @param spectrum_2: The second spectrum to be compared
# @return: return 1 / distance to be computed as a similarity score instead
# of a distance score. If the distance between the two spectra is 0 then 
# math.inf is returned due to the fact that a distance of 0 means the two
# spectra are the same.
def msd(spectrum_1, spectrum_2):
    distance = 0

    for i in range(min(len(spectrum_1), len(spectrum_2))):
        distance += (spectrum_1[i][1] - spectrum_2[i][1]) ** 2

    if distance == 0:
        return math.inf
    else:
        return 1 / (distance ** 0.5)

# Mean Average Distance (mad)
# @param spectrum_1: The first spectrum to be compared
# @param spectrum_2: The second spectrum to be compared
# @return: return 1 / distance to be computed as a similarity score instead
# of a distance score. If the distance between the two spectra is 0 then 
# math.inf is returned due to the fact that a distance of 0 means the two
# spectra are the same.
def mad(spectrum_1, spectrum_2):
    distance = 0

    for i in range(min(len(spectrum_1), len(spectrum_2))):
        distance += abs(spectrum_1[i][1] - spectrum_2[i][1])

    if distance == 0:
        return math.inf
    else:
        return 1 / distance

# Cosine Similarity (dpn) 
# @param spectrum_1: The first spectrum to be compared
# @param spectrum_2: The second spectrum to be compared
# @return: the cosine similarity calculation. Does return 0 if the magnitude of
# either spectra is 0.
def dpn(spectrum_1, spectrum_2):
    min_length = min(len(spectrum_1), len(spectrum_2)) - 1
    spectrum_1_mag = 0
    spectrum_2_mag = 0
    dot_prod = 0

    for i in range(min_length):
        spectrum_1_mag += spectrum_1[i][1] ** 2
        spectrum_2_mag += spectrum_2[i][1] ** 2
        dot_prod += spectrum_1[i][1] * spectrum_2[i][1]

    spectrum_1_mag **= 0.5
    spectrum_2_mag **= 0.5

    if spectrum_1_mag == 0 or spectrum_2_mag == 0:
        return 0
    else:
        return dot_prod / (spectrum_1_mag * spectrum_2_mag)

# Normalized Local Change (index version)
# @param spectrum: the spectrum to be processed with nlc
# @param floor_value: Value to floor the spectrum by 
# @param width: number of indexes considered when calculating the value for a 
# certain point
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

        new_y = right_section / (left_section + right_section)
        results.append([spectrum[i][0] , new_y])

    return results

# Normalized Local Change (wavelength version)
# @param spectrum: the spectrum to be processed with nlc
# @param floor_value: Value to floor the spectrum by 
# @param width: number of indexes considered when calculating the value for a 
# certain point
def nlc_wavelength_range(spectrum, floor_value=0.3, width=1.5):
    floor(spectrum, floor_value)
    results = []

    for i in range(len(spectrum)):
        left_sum, left_count, left_avg = 0, 0, 0 
        right_sum, right_count, right_avg = 0, 0, 0 

        j = 1
        in_bounds = True
        while i - j >= 0 and in_bounds:
            if abs(spectrum[i][0] - spectrum[i - j][0]) <= width:
                left_sum += spectrum[i - j][1]
                left_count += 1
            else:
                in_bounds = False
            j += 1

        j = 1
        in_bounds = True
        while i + j < len(spectrum) and in_bounds:
            if abs(spectrum[i][0] - spectrum[i + j][0]) <= width:
                right_sum += spectrum[i + j][1]
                right_count += 1
            else:
                in_bounds = False
            j += 1

        right_avg = 0 if right_count == 0 else right_sum / right_count
        left_avg = 0 if left_count == 0 else left_sum / left_count
        sum_avg = left_avg + right_avg
        new_y = 0 if sum_avg == 0 else right_avg / sum_avg
        results.append([spectrum[i][0] , new_y])

    return results

# Pre-processing method used to match up the individual points of one spectrum
# to the other. This method is used as the entry point to sort the two spectra
# and determine which way they will be matched. Currently the method finds out 
# which spectrum has the lowest starting position and matches the other 
# spectrum's points to its points. This may not be the best way to do it but it
# ensures consistency because results can vary depending which spectrum is 
# getting mapped and which spectrum is staying the same.
# @param spectrum_1: first spectrum to have points matched
# @param spectrum_2: second spectrum to have points matched
# @param max_difference: maximum difference between the two x values of the
# points to be considered.
# @return: the two spectra that now have matched points 
def match_points(spectrum_1, spectrum_2, max_difference):
    spectrum_1.sort(key = lambda x: x[0])
    spectrum_2.sort(key = lambda x: x[0])

    if spectrum_1[0][0] > spectrum_2[0][0]:
        return create_matched_spectra(spectrum_1, spectrum_2, max_difference)
    else:
        return create_matched_spectra(spectrum_2, spectrum_1, max_difference)

# Point matcher method to actually match up the two spectra's points
# @param spectrum_1: first spectrum to have points matched
# @param spectrum_2: second spectrum to have points matched
# @param max_difference: maximum difference between the two x values of the
# points to be considered.
# @return: two separate spectra that now have matched points
def create_matched_spectra(spectrum_1, spectrum_2, max_difference):
    matched_spectrum_1, matched_spectrum_2 = [], []
    for wavenumber, absorbance in spectrum_1:
        closest_i = get_closest_value_index(spectrum_2, wavenumber)
        if abs(wavenumber - spectrum_2[closest_i][0]) < max_difference:
            matched_spectrum_1.append([wavenumber, absorbance])
            matched_spectrum_2.append([wavenumber, spectrum_2[closest_i][1]])

    return matched_spectrum_1, matched_spectrum_2

# Helper method for create_matched_spectra. Since the spectra are sorted lists
# this does a binary search to find the closest index. Not optimal for spectra
# with similar ranges but this dataset deals with many different ranges
def get_closest_value_index(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    if target >= arr[n - 1][0]:
         n - 1
    if target <= arr[0][0]:
        return 0

    while left < right:
        mid = (left + right) // 2
        if target < arr[mid][0]:
            right = mid
        elif target > arr[mid][0]:
            left = mid + 1
        else:
            return mid

    if target < arr[mid][0]:
        return find_closest(arr, mid - 1, mid, target)
    else:
        return find_closest(arr, mid, mid + 1, target)

def find_closest(arr, left, right, target):
    return right if target - arr[left][0] >= arr[right][0] - target else left

# Helper method to create a floor for a spectrum. The floor is decided by
# multiplying the mean of the spectrum by a multiplier
# @param spectrum: the spectrum to be processed
# @param multiplier: the value to multiply the mean by
def floor(spectrum, multiplier):
    mean = get_mean(spectrum) * multiplier
    for entry in spectrum:
        if entry[1] < mean:
            entry[1] = mean

# Helper method to get the mean of the spectrum y values
# @return: the mean of the y values of the spectrum
def get_mean(spectrum):
    mean = 0
    for entry in spectrum:
        mean += entry[1]
    return mean / len(spectrum)
