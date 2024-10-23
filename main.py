from random import sample, randint, choices
from math import floor, ceil, sqrt
from typing import List

"""
Desc : Implementation part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""


def lazy_select(arr: List[int], k: int, max_iteration: int = 2000) -> int:
    """
    Returns the kth smallest element of the arr
    :param arr the array of size len_arr to search
    :param k the index [1,len_arr]
    :param max_iteration nbr of iteration before stopping the algorithm if no solution found
    """
    n: int = len(arr)
    n_34 = n ** (3 / 4)
    n_14 = n ** (1 / 4)
    x: int = int(k / n_14)  # k / len_arr**1/4 == k * len_arr**-1/4

    current_iteration: int = 0

    while current_iteration < max_iteration:
        # 1. pick n^3/4 elements from S independently and uniformly at random with replacement
        # call this multiset R
        R: List[int] = sample(arr, ceil(n_34))  # choice is with replacement
        # 2. sort R in O(len_arr**3/4) using an optimal sorting algo
        R.sort()

        # 3.
        l: int = max(floor(x - sqrt(n)), 1)
        h: int = min(ceil(x + sqrt(n)), len(R) - 1)

        a: int = R[l - 1]
        b: int = R[h - 1]

        rank_a: int = 0
        rank_b: int = 0
        P: List[int] = []

        for i in range(n):
            elem = arr[i]
            if elem < a:
                rank_a += 1
            if elem <= b:
                rank_b += 1
            if a <= elem <= b:
                P.append(elem)

        # 4. Check if S_k is in P and |p| <= 4r + 2
        if len(P) <= (4 * n_34) + 2:  # small enough

            range_elem: int = k - rank_a - 1
            if rank_a <= k <= rank_b and range_elem < len(P):  # S-k in P
                P.sort()
                return P[range_elem]

        current_iteration += 1

    if current_iteration >= max_iteration:
        raise Exception(f"Too many iterations {max_iteration}, solution not found.")
    else:
        raise Exception("Unknown error")


def partition(arr: List[int], left: int, right: int) -> int:
    """
    Subalgorithm for quickselect, 2 pointer algorithm
    :return: the pivot
    """
    pivot = arr[right]

    # start the lookup at the left of the vector
    i = left  # i = next potential sport for left partition, 1st pointer
    for j in range(left, right):  # j is the already traversed vector, 2nd pointer
        elem = arr[j]
        if elem < pivot:
            arr[i], arr[j] = elem, arr[i]  # swap
            i += 1  # move lecture head to right

    arr[i], arr[right] = arr[right], arr[i]
    return i


def quick_select_non_recursive(input_array: List[int], left: int, right: int, k: int) -> int:
    """
    Quick select algorithm (find the kth smallest element of an array) without recursion to save a bit of performance,
    using partition()
    :param input_array:
    :param left:
    :param right:
    :param k: the index to find
    :param max_iteration:
    :return: the kth smallest element of input_array
    """
    current_iteration: int = 0
    max_iteration = 1
    while current_iteration < max_iteration:
        pivot = partition(input_array, left, right)

        if pivot == k - 1:
            return input_array[k - 1]

        elif pivot > k - 1:
            right = pivot - 1

        else:
            left = pivot + 1

    if current_iteration >= max_iteration:
        raise Exception(f"Too many iterations {max_iteration}, solution not found.")
    else:
        raise Exception("Unknown error")


def print_array(input_array: List):
    """
    print an array as "[array[0], ..., array[n-1]]"
    :param input_array: the array to print
    :return: None
    """

    if len(input_array) == 0:
        print("[]")
        return

    str_arr = "["
    for i in range(len(input_array)):
        str_arr += f"{i}:{input_array[i]}, "
    str_arr = str_arr[:-2] + "]"
    print(f"str_arr:\n{str_arr}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    n = 100
    arr = [randint(-n*10, n*10) for i in range(n)]
    k = randint(1, n)
    #result = str(lazy_select(arr, k))
    result = str(quick_select_non_recursive(arr, 0, len(arr)-1, k))

    # print array
    arr.sort()
    print_array(arr)

    # print results
    print(f"result:{result}, k:{k}, arr[{k}]:{arr[k-1]}")
