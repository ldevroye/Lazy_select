import json

from typing import List
from enum import Enum
from time import time
from datetime import datetime

from main import *



"""
Desc : Testing part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""

# the minimum amout of sample needed to not print every step of algorithms testing (even if print_out is True)
MIN_SAMPLE_TO_PRINT = 10


class Algo(Enum):
    quick_select = 1
    lazy_select = 2
    one_b = 1_000_000_000
    hundred_m = 100_000_000
    ten_m = 10_000_000
    one_m = 1_000_000
    hundred_k = 100_000
    ten_k = 10_000
    one_k = 1_000


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


def add_underscore(value: int) -> str:
    """
    Formate the integer 'num' given by adding '_' to add readability.

    Example : 52658411 -> 52_658_411

    PS: this is not very optimized.
    :param value: value to formate
    :return: the formated string of the value
    """
    num_str: str = str(value)
    ret: List[str] = []

    three_consecutives: int = 0
    for index, elem  in enumerate(reversed(num_str)):
        ret = [elem] + ret[0:]
        three_consecutives += 1

        if three_consecutives == 3 and index < len(num_str)-1:
            ret = ['_'] + ret[0:]
            three_consecutives = 0

    return ''.join(ret)


def get_corresponding_name(value: int) -> str:
    possible_elem = [elem for elem in Algo if elem.value == value]
    if len(possible_elem) <= 0:
        return add_underscore(value)

    return possible_elem[0].name


def int_to_decimal(input_time: float) -> float:
    return int(input_time * 1000) / 1000


def current_time() -> str:
    return datetime.now().strftime("%Hh%M")


def print_test(test: str, print_bool: bool = True) -> None:
    """
    Print test if print_bool is true
    :param test: str to print
    :param print_bool: bool to check
    :return: None
    """
    if print_bool:
        print(test)


def test_algo(algo: Enum, vec_size: int, sample_size: int, print_out: bool = True, test_assert: bool = True) -> (float, int):
    """
    Test the given algorithm 'algo' on an array of size 'vec_size' for 'sample_size' time.
    return the average time to resolve the arrays for the given size
    :param algo:
    :param vec_size:
    :param sample_size:
    :param print_out:
    :param test_assert:
    :return: tuple(average time to resolve, nbr of comparisons made)
    """
    n = vec_size
    ten_n = 10 * n
    start_time = time()
    print_test(f"Start testing {sample_size} samples with algorithm:'{algo.name}', "
               f"vector size:'{get_corresponding_name(vec_size)}'", print_out)

    algorithm = None

    for i in range(sample_size):
        step_time = time()
        # Define the set S
        S = [randint(-ten_n, ten_n) for _ in range(n)]

        # Define random rank to return
        k = randint(1, n)

        # Find the kth smallest element in S
        result: int

        if algo == Algo.lazy_select:
            algorithm = LazySelect()
            result = algorithm.run(S, k)
        elif algo == Algo.quick_select:
            algorithm = QuickSelect()
            result = algorithm.run(S, 0, len(S) - 1, k)
        else:
            raise Exception("unknown algorithm requested")

        # compare with naive but safe approach
        if test_assert:
            S.sort()
            to_assert = S[k-1]
            assert (result == to_assert)

        end_step_time = time() - step_time
        print_test(f"Result {i} : {result} for k:{k} in {int_to_decimal(end_step_time)}sec", print_out and sample_size < MIN_SAMPLE_TO_PRINT)

    end_time = time() - start_time
    print_test(f"Implementation Test passed in {int_to_decimal(end_time)} sec.\n", print_out)
    return int_to_decimal(end_time / sample_size), ceil(algorithm.comparisons / sample_size)


def compare(vec_size: int, sample_size: int) -> tuple[float, float]:
    """
    Compare lazy and quick algorithms
    :return: None
    """

    time_quick: float = int_to_decimal(test_algo(Algo.quick_select, vec_size, sample_size, False, test_assert=False))
    time_lazy: float = int_to_decimal(test_algo(Algo.lazy_select, vec_size, sample_size, False, test_assert=False))

    time_test: (float, float) = (time_quick, time_lazy)

    print(f"Comparison finished (vec {get_corresponding_name(vec_size)}, sample {sample_size}) {current_time()}")

    return time_test


def test(algo):
    test_algo(algo, Algo.hundred_k.value, 100)
    test_algo(algo, Algo.one_m.value, 30)
    test_algo(algo, Algo.ten_m.value, 10)
    #test_algo(algo, Algo.hundred_m.value, 1)

    # one_b takes much much much (much) more time
    # test_lazy(one_b, 1)


def compare_all():
    time_table: dict[str, tuple[float, float]] = dict[str, tuple[float, float]]()

    vec_size: int = Algo.ten_k.value
    sample_size: int = 2000
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    vec_size: int = Algo.hundred_k.value
    sample_size: int = 200
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    vec_size = Algo.one_m.value
    sample_size = 10
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    """
    vec_size = Algo.ten_m.value
    sample_size = 5
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    vec_size = Algo.hund_m.value
    sample_size = 1
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)
    """

    with open('./tests/output.txt', 'a') as file:
        json.dump(time_table, file, indent=4)
        file.write("\n\n")


def get_infos(vec_sizes: List[int], sample_size: int) -> dict[int, tuple[tuple[float, float], tuple[float, float]]]:
    """
    Get the average running time for sample_size times arrays of size vec_sizes
    :param vec_sizes: List of sizes for arrays
    :param sample_size: numbre of sample to do
    :return: the dictionnary as {vec_size : ((quick_avg_time, quick_nbr_comparisons), (lazy_avg_time, lazy_nbc_comparisons))}
    """
    tmp: dict[int, tuple[tuple[float, float], tuple[float, float]]] = dict[int, tuple[tuple[float, float], tuple[float, float]]]()

    for vec_size in vec_sizes:
        quick: tuple[float, float] = test_algo(Algo.quick_select, vec_size, sample_size, False, test_assert=False)
        print("quick :", get_corresponding_name(vec_size), sample_size, quick[0], quick[1])
        lazy: tuple[float, float] = test_algo(Algo.lazy_select, vec_size, sample_size, False, test_assert=False)
        print("lazy :", get_corresponding_name(vec_size), sample_size, lazy[0], lazy[1], "\n")

        tmp[vec_size] = (quick, lazy)
    return tmp


if __name__ == '__main__':
    print(f"Starting test: {current_time()}")
    test(Algo.quick_select)
    #test(Algo.lazy_select)

    # compare_all()

    print(f"End test: {current_time()}")
