# CS6033 - Artificial Intelligence
# Fall 2022
# Scott Fasone
# Assignment 01

# Homework Group 14
#  - Adonia Jebessa
#  - Breanna King
#  - Mohammad Yahiya Khan
#  - Scott Fasone

from functools import reduce
from random import randint
from typing import Literal



#####################
# Utility Functions #
#####################

def swap(nums: list[int], i: int, j: int):
    """Swaps two elements in a list."""
    tmp = nums[i]
    nums[i] = nums[j]
    nums[j] = tmp
def make_random_list(length: int):
    nums = []
    max = length * 10 + 1
    for _ in range(0, length):
        nums.append(randint(0, max))
    return nums
def verify_sort(nums: list[int]):
    """Verify that a list is of integers is sorted, ascending"""
    for i in range(0, len(nums) - 1):
        if nums[i] > nums[i + 1]:
            raise ValueError("List not sorted!")



###############
# Bubble Sort #
###############
def bubble_sort(nums: list[int], low=0, high=None):
    # print("Bubble Sort!")
    # Default high to end of the list.
    if high is None: high = len(nums)

    for i in range(high - 1, low, -1):
        for j in range(low, i):
            if nums[j] > nums[j + 1]:
                swap(nums, j, j + 1)
    return nums

##############
# Quick Sort #
##############
def quick_sort(nums: list[int], low=0, high=None, sort_callback=None):
    # print("Quick Sort!")
    # Default high to end of the list.
    if high is None: high = len(nums)
    # Enable sort_callback, to allow seperate recursive sorting algorithms.
    if sort_callback is None: sort_callback = quick_sort

    # Recursion guard.
    if low >= high: return

    # Partition
    # Pick first element as the pivot.
    pivot = nums[low]
    # The placeholder pivot index. Pivot is not moved until after partition.
    pivot_index = low
    for i in range(low + 1, high):
        if nums[i] <= pivot:
            pivot_index += 1
            swap(nums, pivot_index, i)
    # Put pivot into the correct position.
    swap(nums, pivot_index, low)

    # Recurse
    sort_callback(nums, low, pivot_index)
    sort_callback(nums, pivot_index + 1, high)
    return nums

##############
# Merge Sort #
##############
def merge_sort(nums: list[int], low=0, high=None, sort_callback=None):
    # print("Merge Sort!")
    # Default high to end of the list.
    if high is None: high = len(nums)
    # Enable sort_callback, to allow seperate recursive sorting algorithms.
    if sort_callback is None: sort_callback = merge_sort

    # Recursion guard.
    if high - low <= 1: return nums
    if high - low == 2:
        # Short-circuit for just two elements in sub-array.
        if nums[low] > nums[high - 1]:
            swap(nums, low, high - 1)
        return nums

    # Recurse
    median = (high + low) // 2
    sort_callback(nums, low, median)
    sort_callback(nums, median, high)

    # Merge
    # Use a working list to merge into the return array.
    # Increases memory complexity to n, but keeps time complexity at nlogn
    # Memory complexity could be reduced by using a single n-length work list through the entire callstack.
    work_list = nums[low:high]
    left_index = low
    right_index = median
    for i in range(0, high - low):
        if not left_index >= median and (right_index >= high or nums[left_index] <= nums[right_index]):
            # Left number is less.
            work_list[i] = nums[left_index]
            left_index += 1
        else:
            # Right number is less.
            work_list[i] = nums[right_index]
            right_index += 1
    nums[low:high] = work_list

    return nums


###############
# Hybrid Sort #
###############
ALGO_OPTION = Literal["mergesort", "quicksort", "bubblesort"]
def hybrid_sort(nums: list[int], big_algo: ALGO_OPTION, small_algo: ALGO_OPTION, threshold: int, low=0, high=None):
    # Default high to end of the list.
    if high is None: high = len(nums)

    # NOTE: while it may look like we're just calling merge_sort and quick_sort on the rest of the array,
    #       we are actually just running it during this one step, then calling hybrid_sort again on further
    #       recursions by using the sort_callback named parameters.

    algo = small_algo if (high - low) < threshold else big_algo
    if algo == "bubblesort":
        bubble_sort(nums, low, high)
    elif algo == "mergesort":
        merge_sort(nums, low, high, sort_callback=lambda n, l, h: hybrid_sort(n, big_algo, small_algo, threshold, l, h))
    elif algo == "quicksort":
        quick_sort(nums, low, high, sort_callback=lambda n, l, h: hybrid_sort(n, big_algo, small_algo, threshold, l, h))
    else:
        raise ReferenceError(f"Unknown sort algorithm: {algo}")
    return nums



################
# Example Runs #
################

# Bubble Sort
numbers = make_random_list(20)
bubble_sort(numbers)
verify_sort(numbers)

numbers = make_random_list(100)
bubble_sort(numbers)
verify_sort(numbers)

# Quick Sort
numbers = make_random_list(20)
quick_sort(numbers)
verify_sort(numbers)

numbers = make_random_list(100)
quick_sort(numbers)
verify_sort(numbers)

# Merge Sort
numbers = make_random_list(20)
merge_sort(numbers)
verify_sort(numbers)

numbers = make_random_list(100)
merge_sort(numbers)
verify_sort(numbers)

# Hybrid Sort
numbers = make_random_list(100)
hybrid_sort(numbers, "quicksort", "bubblesort", 16)
verify_sort(numbers)

numbers = make_random_list(100)
hybrid_sort(numbers, "mergesort", "bubblesort", 16)
verify_sort(numbers)



# Example of my profiling function for analyzing performance.
def profile():
    import time

    times = []
    reps = 10
    N = 20000

    for _ in range(0, reps):
        arr = make_random_list(N)
        start_time = time.time()
        hybrid_sort(arr, "quicksort", "bubblesort", 64)
        end_time = time.time()
        verify_sort(arr)

        elapsed = end_time - start_time
        times.append(elapsed)
        print("--- %s seconds ---" % (elapsed))
    avg_time = reduce(lambda acc, val: acc + val / len(times), times, 0)
    print("Average Time: %s seconds ---" % (avg_time))

# |--------------------------|
# | Performance and Comments |
# |--------------------------|
#
# I ran each algorithm on lists of random integers, averaged across 10 runs.
# The following were the results on my machine:
#
#     Bubble Sort (5,000 elements):  1.92 seconds
#     Quick Sort  (20,000 elements): 57.0 milliseconds
#     Merge Sort  (20,000 elements): 47.9 milliseconds
#
#     Hybrid Sort (20,000 elements)
#         - quicksort, T=0:     71.2 milliseconds
#         - quick+bubble, T=16: 56.5 milliseconds
#         - quick+bubble, T=64: 94.4 milliseconds
#
#         - mergesort, T=0:     56.3 milliseconds
#         - merge+bubble, T=16: 50.4 milliseconds
#         - merge+bubble, T=64: 85.2 milliseconds
#
# My implementation on mergesort, on my machine, is marginally faster than quicksort. This is probably due to my merge
# algorithm using extra space to elimate swapping, and my quicksort simply picking the first element as a pivot.
# Bubblesort, as expected, performs untenably at larger inputs.
#
# My hybridsort, even without switching algorithms, performed worse than its non-hybrid versions. This is probably due
# to the extra conditionals it adds to the algorithm, as well as creating recursive lambda functions for callbacks.
# Even with the drawback, however, we still saw performance improvements when hybridizing with bubblesort for certain
# small values of T (threshold). A parametric study on that threshold could generate a more optimum threshold for
# certain inputs
