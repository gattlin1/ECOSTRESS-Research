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

def match_points(spectra1, spectra2):
    matched_spectra = []
    spectra2.sort(key = lambda x: x[0])
    for wavenumber, absorbance in spectra1:
        closest_index = get_closest_value_index(spectra2, wavenumber)
        matched_spectra.append(spectra2[closest_index])

    return matched_spectra
