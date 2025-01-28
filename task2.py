def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] == target:
            return iterations, arr[mid]
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    if left < len(arr):
        upper_bound = arr[left]
    else:
        upper_bound = None

    return iterations, upper_bound


array = [0.1, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0]
print(binary_search(array, 0.8))
