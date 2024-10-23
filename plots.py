import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from main import *
from test import *

"""
Desc : Ploting part of : Implementation and testing of 2 random bases algorithms : lazy select and quick select
Author : Louis Devroye
Date : 22/10/24
License : Free of use, "AS IS" : no warranty, credits
"""


def plot_running_time(sizes: List[int], dict_input: dict[int, tuple[float, float]]):
    """
    Plots the average running time of QuickSelect vs LazySelect as a function of input size.
    :param dict_input: dictionnary of {vector size: (quick_time, lazy_time)}
    """
    quick_times: List[float] = []
    lazy_times: List[float] = []
    for key in dict_input.keys():
        elem = dict_input[key]
        quick_times.append(elem[0])
        lazy_times.append(elem[1])

    plt.figure(figsize=(10, 6))

    # Plot QuickSelect times
    plt.plot(sizes, quick_times, marker='o', label='QuickSelect', color='b')

    # Plot LazySelect times
    plt.plot(sizes, lazy_times, marker='o', label='LazySelect', color='g')

    plt.xscale('log')

    # Adding labels and title
    plt.xlabel('Input Size (n)')
    plt.ylabel('Average Running Time (seconds)')
    plt.title('QuickSelect vs LazySelect: Running Time Comparison')

    # Add a legend
    plt.legend()

    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Display the plot
    plt.grid(True)
    plt.show()


def plot_comparison_number(sizes: List[int], dict_input: dict[int, tuple[float, float]]):
    """
    Plots the average running time of QuickSelect vs LazySelect as a function of input size.
    :param dict_input: dictionnary of {vector size: (quick_time, lazy_time)}
    """
    quick_times: List[float] = []
    lazy_times: List[float] = []
    for key in dict_input.keys():
        elem = dict_input[key]
        quick_times.append(elem[0])
        lazy_times.append(elem[1])

    plt.figure(figsize=(10, 6))

    # Plot QuickSelect times
    plt.plot(sizes, quick_times, marker='o', label='QuickSelect', color='b')

    # Plot LazySelect times
    plt.plot(sizes, lazy_times, marker='o', label='LazySelect', color='g')

    plt.xscale('log')
    plt.yscale('log')


    # Adding labels and title
    plt.xlabel('Array Size (n)')
    plt.ylabel('Average Number of Comparisons')
    plt.title('QuickSelect vs LazySelect: Running Time Comparison')

    # Add a legend
    plt.legend()

    plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

    # Display the plot
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    print(f"Starting plots : {current_time()}")

    small_sizes: List[int] = ([Algo.ten_k.value, Algo.ten_k.value*5] +
                              [Algo.hundred_k.value*(i+1) for i in range(0, 10, 2)] +
                              [Algo.one_m.value])

    big_sizes: List[int] = ([Algo.hundred_k.value*(i+1) for i in range(10)] +
                            [Algo.one_m.value*(i+1) for i in range(0, 10, 2)] +
                            [Algo.ten_m.value*(i+1) for i in range(0, 10, 3)])

    dict_times: dict[int, tuple[float, float]] = get_times(big_sizes, 10)

    print(f"Ending plots : {current_time()}")

    plot_running_time(big_sizes, dict_times)

