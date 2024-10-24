import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from test import *

"""
Desc : Ploting part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""


def plot(dict_input: dict[int, tuple[float, float]], avg_time: bool = True):
    """
    Plots the average running time or number of comparis ons of QuickSelect vs LazySelect as a function of input size.
    :param avg_time: if Turned to True, the Plot is for average time, otherswise for number of comparisons
    :param dict_input: dictionnary of {vector size: (quick_time, lazy_time)}

    ! len(DICT) = len(sizes) ! otherwise will crash
    """
    sizes: List[int] = []
    quick_times: List[float] = []
    lazy_times: List[float] = []
    for key in dict_input.keys():
        elem = dict_input[key]
        sizes.append(key)
        quick_times.append(elem[0])
        lazy_times.append(elem[1])

    expected_times_quick: List[float] = [3.386 * x for x in sizes]  # bound for comparisons of QuickSelect
    expected_times_lazy: List[float] = [4 * x for x in sizes]  # not sure about this one (bound for LazySelect)
    plt.figure(figsize=(10, 6))

    # Adding labels and title
    plt.xlabel('Array Size (n)')

    if avg_time:
        plt.ylabel('Average Running Time')
        plt.title('QuickSelect vs LazySelect: Average Running Time by Size')


    else:  # comparisons
        plt.ylabel('Number of Comparisons')
        plt.title('QuickSelect vs LazySelect: Number of Comparisons by Size')
        plt.plot(sizes, expected_times_quick, marker='x', label='Expected Quick', color='orange')
        plt.plot(sizes, expected_times_lazy, marker='x', label='Expected Lazy', color='r')

    plt.plot(sizes, quick_times, marker='o', label='QuickSelect', color='b')
    plt.plot(sizes, lazy_times, marker='o', label='LazySelect', color='g')

    plt.xscale('log')
    plt.yscale('log')

    plt.legend()
    # Display
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    sample_size = 10

    print(f"Starting plots for {sample_size} samplpes : {current_time()}")

    small_sizes: List[int] = ([Algo.ten_k.value, Algo.ten_k.value*5] +
                              [Algo.hundred_k.value*(i+1) for i in range(0, 10, 2)] +
                              [Algo.one_m.value])

    big_sizes: List[int] = ([Algo.hundred_k.value*(i+1) for i in range(10)] +
                            [Algo.one_m.value*(i+1) for i in range(1, 10, 2)] +
                            [Algo.ten_m.value*(i+1) for i in range(1, 9, 3)])

    to_compare = small_sizes

    print_array(to_compare)
    dict_info: dict[int, tuple[tuple[float, float], tuple[float, float]]] = get_infos(to_compare, sample_size)

    print(f"Ending plots for {sample_size} samples : {current_time()}")
    dict_time = {key: (dict_info[key][0][0], dict_info[key][1][0]) for key in dict_info.keys()}
    dict_nbr_comparisons = {key: (dict_info[key][0][1], dict_info[key][1][1]) for key in dict_info.keys()}

    plot(dict_time)
    plot(dict_nbr_comparisons, False)