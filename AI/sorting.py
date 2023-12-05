import random

# Generating a list of random numbers
random_list = [random.randint(1, 100000) for _ in range(100000)]  # Generates 10 random numbers between 1 and 100

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

# Printing the original list
print("Original List:", random_list)

# Sorting the list using bubble sort
bubble_sort(random_list)

# Printing the sorted list
print("Sorted List:", random_list)
