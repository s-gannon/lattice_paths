# Lattice Paths

Code for computation regarding k-equivalent lattice paths in combinatorics.

## The Greedy Algorithm

The [get_data.py](https://github.com/ejyager00/lattice_paths/blob/master/get_data.py) file allows us to generate a table comparing the greedy algorithm to a brute force approach. To get the data in TSV form, run the following on the command line, where `m` and `n` are integers.

There are also optional arguments for file name and incremental saving of results.

```
# python3 get_data.py m n filename.tsv i
```

For example:

```
# python3 get_data.py 4 3
```

```
# python3 get_data.py 4 3 lattice4by3results.tsv i
```

## The Genetic Algorithm

There's two implementations of the genetic algorithm, one in Python and another in C. You can find each in their respective folders `/python/genetic` and `/c/genetic`. The C version requires `make` to build the main program and can be run by issuing:

```
# ./lattice_paths m n k g s
```

where `m, n` denote an m by n lattice, `k` is the k-distinctness we're looking for, `g` is the maximum number of generations to go through, and `s` is the numer of 'people' in our initial population.
