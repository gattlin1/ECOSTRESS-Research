def mean(spectrum):
    sum = 0
    for wavelength, absorbance in spectrum:
        sum += wavelength

    return sum / len(spectrum)

def get_closest_value_index(arr, target):
    n = len(arr)
    left = 0
    right = n - 1
    mid = 0

    if target >= arr[n - 1][0]:
        return n - 1
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

def match_points(spectra1, spectra2, threshold_difference):
    matched_spectra1 = []
    matched_spectra2 = []

    mean_1 = mean(spectra1)
    mean_2 = mean(spectra2)

    if abs(mean_1 - mean_2) < 4:
        spectra1.sort(key = lambda x: x[0])
        spectra2.sort(key = lambda x: x[0])

        for wavenumber, absorbance in spectra1:
            closest_index = get_closest_value_index(spectra2, wavenumber)
            if abs(wavenumber - spectra2[closest_index][0]) < threshold_difference:
                matched_spectra1.append([wavenumber, absorbance])
                matched_spectra2.append(spectra2[closest_index])

    return matched_spectra1, matched_spectra2
