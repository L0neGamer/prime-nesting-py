from cmath import inf
from itertools import takewhile
from operator import index
import sys
from typing import Dict, List
from sympy import isprime

# implementation of https://oeis.org/A346642


def remove_dup(seq):
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def get_int(s, d=0):
    try:
        return int(s)
    except:
        return d


def get_list(lst, i, d=None):
    if i >= len(lst):
        return d
    return lst[i]


prepend_items = [str(i) for i in range(1, 10)]
append_items = [str(i) for i in range(1, 10, 2)]

zeroes = "-z" in sys.argv and get_int(get_list(sys.argv,
                                      sys.argv.index("-z")+1), inf)
ancestors = "-a" in sys.argv

# given an integer, generate all children of it that are prime
# first gets all the prepend items, then all the append items
# uses a generator to be slightly better in general


def get_prime_children(i: str):
    for j in prepend_items:
        k = j+i
        if isprime(int(k)):
            yield k
    if zeroes:
        if zeroes == inf:
            yield "0" + i
        elif len(list(takewhile(lambda x: x == "0", i))) < zeroes:
            yield "0" + i
    if i[0] != "0":
        for j in append_items:
            k = i+j
            if isprime(int(k)):
                yield k

# given a list of integers, return all of their children (tupled with the parent)
# this tupling with the parent lets us quickly search back through the ancestry


def get_all_prime_children(i_list: List[int]):
    for i in i_list:
        for j in get_prime_children(i):
            yield (j, int(i))

# given a list of integers to start the list off on, continuously get all prime
# nesting options.
# combines parent lists together if and when it is required


def driver(i_list: List[str]):
    while i_list:
        init_children = get_all_prime_children(i_list)
        temp_children = {}
        for (c, p) in init_children:
            tc = temp_children.get(c)
            if tc:
                temp_children[c].append(p)
            else:
                temp_children[c] = [p]

        children = sorted([(i, temp_children[i])
                          for i in temp_children.keys()])

        for i in children:
            if i[0][0] != "0":
                yield (int(i[0]), i[1])

        i_list = list(map(lambda v: v[0], children))

# get the full ancestry of a given value


def get_ancestors(full_family: Dict[int, List[int]], descendant):
    full_ancestors = [descendant]
    ancestors = [descendant]

    while ancestors:
        ancestors = [i for j in map(
            lambda i:full_family.get(i), ancestors) if j is not None for i in j]
        full_ancestors += ancestors

    return remove_dup(full_ancestors)

# given an integer and a function that outputs, output the pairings and also
# return the child - parent dict


def main(n: int, out):
    start_primes = list(filter(lambda x: isprime(int(x)), prepend_items))

    d = driver(start_primes)

    value_parent = None

    if ancestors:
        value_parent = {}

    start_range, end_range = len(start_primes), n
    for (pos, i) in zip(range(min(len(start_primes), n)), start_primes):
        out(f"{pos}: {i}")
        if ancestors:
            value_parent[int(i)] = None

    for (pos, i) in zip(range(start_range, end_range), d):
        out(f"{pos}: {i}")
        if ancestors:
            value_parent[int(i[0])] = i[1]

    if ancestors:
        return value_parent


# run using `python3 prime-nesting.py 100`
# adding `-f` to the parameters makes the output go to file instead
# adding `-z` means zeroes can be prepended. if a number follows, up to that many zeroes are allowed
# adding `-a` to the parameters means that the ancestors are generated. this is required for the following options
# adding `-p` to the parameters makes all ancestors of the following number get output
# adding `-l` to the parameters makes the program loop on stdin, letting the user input primes to get parents of
if __name__ == "__main__":
    v = None
    out = print
    if "-f" in sys.argv:
        with open("output.txt", "w") as f:
            def out(s): return f.write(s + "\n")
            v = main(int(sys.argv[1]), out)
    else:
        v = main(int(sys.argv[1]), out)

    if not ancestors:
        exit()

    if "-p" in sys.argv:
        pindex = sys.argv.index("-p")
        prime = int(sys.argv[pindex+1])
        print(get_ancestors(v, prime))

    if "-l" in sys.argv:
        inp = input(">")
        while inp:
            print(get_ancestors(v, int(inp)))
            inp = input(">")


"""
> python3 prime-nesting.py 873295 -f -a -p 8939662423123592347173339993799
[8939662423123592347173339993799, 939662423123592347173339993799, 93966242312359234717333999379, 3966242312359234717333999379, 966242312359234717333999379, 66242312359234717333999379, 6624231235923471733399937, 624231235923471733399937, 24231235923471733399937, 2423123592347173339993, 242312359234717333999, 42312359234717333999, 2312359234717333999, 231235923471733399, 31235923471733399, 3123592347173339, 312359234717333, 31235923471733, 1235923471733, 235923471733, 23592347173, 3592347173, 359234717, 59234717, 5923471, 923471, 92347, 2347, 347, 47, 7]
"""
