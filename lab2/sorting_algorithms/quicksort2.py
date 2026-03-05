def partition(array, low, high):
    pivot = array[low + (high-low)//2]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while array[i] < pivot: i += 1
        j -= 1
        while array[j] > pivot: j -= 1
        if i >= j: return j
        array[i], array[j] = array[j], array[i]

def quicksort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quicksort(array, low, pi)
        quicksort(array, pi + 1, high)

def start_quick_sort_hoare_fixed(array):
    if len(array) > 1:
        quicksort(array, 0, len(array) - 1)
    return array
