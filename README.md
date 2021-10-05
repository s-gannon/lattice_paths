# Lattice Paths

Code for computation regarding k-equivalent lattice paths in combinatorics.

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
