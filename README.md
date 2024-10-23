# Lazy select and Quick select

## Description
Implementation of the Lazy select and Quick select algorithms. They both consist in finding the kth smallest element in an array A of size n.

### Quick select
Quick select does so by partitioning the array with a tower pointer algorithms.
### Lazy select 
Lazy select creates a subset R or size  n**3/4, this subset is made of element of A randomly chosen. 
We then sort R. After that we find the left and right bound. We compare every element of A and make a rank (the kth smallest element has rank k) for the bounds. 
We make a subset P with countains every elements of A that are inbetween the bounds. We check that |P| is lower than (4*n^(3/4) + 2) and that k is in between the ranks of the bounds.
If so, we sort P and then we return the (k - rank_lower_bound - 1)th element of P. Otherwise we start over by choosing a new subset R.

! *Lazy select can fail if the array to search is small (|A| < 1000)* !

## Author
Louis Devroye (ldevroye)

## Date
24/10/2024

## Usage
Test file is made of 2 main functions : **compare_all()** and **test(Algo)**.
It is also made of an "enum" sort of class. This is used to have easier acces to big numbers and an enum to the two algorithms name (for the **test_algo** method).

### compare_all()
This is used to compare the two algorithms on a certains *number of test* on arrays with differents *size*.
### test(Algo)
This is used to test one algorithm on a bigger *sample* for more viable tests.
### base methods
**compare(vector_size, sample_size)** : Base method called by **compare_all()** multiple times. This method write in **tests/output.txt** a json dump of the infos
**test_algo(algo, vector_size, sample_size)** : base method for all the tests.

There are some prints here and there that are disabled (or that you can disable) by default parameters.

Don't try vectors that have more than a hundred million elements. (average 11 minutess on my computer, billion ran for over an hour).


