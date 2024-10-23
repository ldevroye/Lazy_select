from enum import Enum
from time import time
from main import *
from datetime import datetime
import json


"""
Desc : Testing part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""


class Algo(Enum):
    quick_select = 1
    lazy_select = 2
    one_b = 1_000_000_000
    hund_m = 100_000_000
    ten_m = 10_000_000
    one_m = 1_000_000
    hund_k = 100_000
    ten_k = 10_000
    one_k = 1_000


def time_to_decimal(input_time: float) -> float:
    return int(input_time * 1000) / 1000


def current_time() -> str:
    return datetime.now().strftime("%Hh%M")


def compare(vec_size: int, sample_size: int) -> tuple[float, float]:
    """
    Compare lazy and quick algorithms
    :return: None
    """

    time_quick: float = time_to_decimal(test_algo(Algo.quick_select, vec_size, sample_size, False, test_assert=False))
    time_lazy: float = time_to_decimal(test_algo(Algo.lazy_select, vec_size, sample_size,  False, test_assert=False))

    time_test: (float, float) = (time_quick, time_lazy)

    print(f"Comparison finished (vec {vec_size}, sample {sample_size}) {current_time()}")

    return time_test


def test(algo):
    test_algo(algo, Algo.hund_k.value, 100)
    test_algo(algo, Algo.one_m.value, 30)
    test_algo(algo, Algo.ten_m.value, 10)
    test_algo(algo, Algo.hund_m.value, 5)

    # one_b takes much much much (much) more time
    # test_lazy(one_b, 1)


def print_test(test: str, print_bool: bool = True) -> None:
    """
    Print test if print_bool is true
    :param test: str to print
    :param print_bool: bool to check
    :return: None
    """
    if print_bool:
        print(test)


def test_algo(algo: Enum, vec_size: int, sample_size: int, print_out: bool = True, test_assert: bool = True) -> float:
    """
    Test the given algorithm 'algo' on an array of size 'vec_size' for 'sample_size' time.
    return the average time to resolve the arrays for the given size
    :param algo:
    :param vec_size:
    :param sample_size:
    :param print_out:
    :param test_assert:
    :return: average time to resolve
    """
    n = vec_size
    ten_n = 10 * n
    start_time = time()

    print_test(f"\nStart testing {sample_size} samples with '{algo.name}' algorithm, vec size:{n}", print_out)

    for i in range(sample_size):
        step_time = time()
        # Define the set S
        S = [randint(-ten_n, ten_n) for _ in range(n)]

        # Define random rank to return
        k = randint(1, n)

        # Find the kth smallest element in S
        result: int
        if algo == Algo.lazy_select:
            result = lazy_select(S, k)
        elif algo == Algo.quick_select:
            result = quick_select_non_recursive(S, 0, len(S) - 1, k)
        else:
            raise Exception("unknown algorithm requested")

        # compare with naive but safe approach
        if test_assert:
            S.sort()
            assert (result == S[k - 1])

        end_step_time = time() - step_time
        print_test(f"Result {i} : {result} for k:{k} in {time_to_decimal(end_step_time)}sec", print_out and sample_size < 50)

    end_time = time() - start_time
    print_test(f"Implementation Test passed in {time_to_decimal(end_time)} sec.\n", print_out)
    return end_time/sample_size


def compare_all():
    time_table: dict[str, tuple[float, float]] = dict[str, tuple[float, float]]()

    vec_size: int = Algo.ten_k.value
    sample_size: int = 2000
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    vec_size: int = Algo.hund_k.value
    sample_size: int = 200
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

    """
    vec_size = Algo.one_m.value
    sample_size = 30
    time_table[str((vec_size, sample_size))] = compare(vec_size, sample_size)

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


if __name__ == '__main__':
    print(f"Starting : {current_time()}")

    #test(Algo.lazy_select)
    #test(Algo.quick_select)

    compare_all()

    print(f"End : {current_time()}")
