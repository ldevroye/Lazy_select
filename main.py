from random import sample, randint, randrange
from math import floor, ceil, sqrt
from typing import List

"""
Desc : Implementation part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""


class Select:
    comparisons: int = 0
    name: str = 'Select'

    def run(self, input_array: List[int], k: int) -> int:
        """
        Holder to be overridden
        :param k: kth smallest element to find
        :param input_array: array to search (not need to be sorted)
        """
        pass

    def partition(self, input_array: List[int], left: int, right: int, random: bool = True) -> int:
        """
        Subalgorithm for quickselect, 2 pointer algorithm
        :return: the pivot
        """
        # pivot is either randorm or arr[right] or some heuristic (like median)
        # takes the worst case (if array is sorted) out of the equation
        # comment this if you cant to take last element (and not random)
        if random:
            index_pivot = randint(left, right)
            input_array[right], input_array[index_pivot] = input_array[index_pivot], input_array[right]

        # we take the right element since we swap it for the random
        pivot = input_array[right]

        # start the lookup at the left of the vector
        i = left  # i = next potential sport for left partition, 1st pointer
        for j in range(left, right):  # j is the already traversed vector, 2nd pointer
            elem = input_array[j]
            self.comparisons += 1

            if elem <= pivot:
                input_array[i], input_array[j] = elem, input_array[i]  # swap
                i += 1  # move lecture head to right

        input_array[i], input_array[right] = input_array[right], input_array[i]
        return i

    def QuickSort(self, arr_to_sort: List[int]) -> None:
        """
        Quick implementation of an iterative QuickSort

        it is done to have the good number of comparisons for the QuickSelect and LazySelect
        :param arr_to_sort: array to sort
        :return: None
        """
        # Create an auxiliary stack to avoid recursion
        stack = [(0, len(arr_to_sort) - 1)]

        while stack:  # basic working of a stack
            self.comparisons += 2
            start, end = stack.pop()

            # Partition the array and get the pivot index
            pivot_index = self.partition(arr_to_sort, start, end, False)

            # Very similar to quick select, compare the pivot
            if pivot_index - 1 > start:
                stack.append((start, pivot_index - 1))

            # no elif because it can (and will in a lot of times) be both
            if pivot_index + 1 < end:
                stack.append((pivot_index + 1, end))


class LazySelect(Select):
    name = 'LazySelect'

    def run(self, input_array: List[int], k: int, max_iteration: int = 2000) -> int:
        """
        Returns the kth smallest element of the array 'arr'
        :param input_array the array of size len_arr to search
        :param k the index [1,len_arr]
        :param max_iteration nbr of iteration before stopping the algorithm if no solution found
        """
        n: int = len(input_array)
        n_34 = n ** (3 / 4)
        n_14 = n ** (1 / 4)
        x: int = int(k / n_14)  # k / len_arr**1/4 == k * len_arr**-1/4

        current_iteration: int = 0

        while current_iteration < max_iteration:
            # 1. pick n^3/4 elements from S independently and uniformly at random with replacement
            # call this multiset R
            R: List[int] = sample(input_array, ceil(n_34))  # choice is with replacement
            # 2. sort R in O(len_arr**3/4) using an optimal sorting algo
            self.QuickSort(R)

            # 3.
            l: int = max(floor(x - sqrt(n)), 1)
            h: int = min(ceil(x + sqrt(n)), len(R) - 1)

            a: int = R[l - 1]
            b: int = R[h - 1]

            rank_a: int = 0
            rank_b: int = 0
            P: List[int] = []

            for elem in input_array:
                self.comparisons += 3
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
                    self.QuickSort(P)  # 5. Sort and return
                    return P[range_elem]

            current_iteration += 1

        if current_iteration >= max_iteration:
            raise Exception(f"Too many iterations {max_iteration}, solution not found.")
        else:
            raise Exception("Unknown error")


class QuickSelect(Select):
    name = 'QuickSelect'

    def run(self, input_array: List[int], k: int) -> int:
        """
        Quick select algorithm (find the kth smallest element of an array) without recursion to save a bit of performance,
        using partition()
        :param input_array:
        :param k: the index to find
        :return: the kth smallest element of input_array
        """
        left: int = 0
        right: int = len(input_array)-1

        current_iteration: int = 0
        max_iteration: int = 1
        while current_iteration < max_iteration:
            self.comparisons += 2
            pivot = self.partition(input_array, left, right)

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    from test import print_array

    n = 100
    arr = [randint(-n * 10, n * 10) for i in range(n)]
    kth = randint(1, n)
    test = sorted(arr)
    test_Select = Select()

    test_Select.QuickSort(arr)
    print_array(arr)
    print(arr == test, len(arr), test_Select.comparisons)

    algo = QuickSelect()
    result = str(algo.run(arr, kth))

    # print array
    arr.sort()
    print_array(arr)

    # print results
    print(f"result:{result}, k:{kth}, arr[{kth}]:{arr[kth - 1]}")
