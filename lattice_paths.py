"""
A module for handling lattice paths, especially for determining k-equivalence.

...

Classes
-------
LexOrderer
    iterator for lattice paths in lexicographic order
Edges
    iterator for the edges traversed by a lattice path
DistinctSets
    iterator for the k-distinct sets of a particular size on a particular
    lattice

Functions
---------
equivalent(edges1: Sequence[tuple[int]], edges2: Sequence[tuple[int]], k: int)
    returns a boolean that is True if the paths that the edge sets correspond to
    are k equivalent
equivalent_in_set(path: str, path_set: Sequence[str], k: int)
    returns a boolean that is True if the path is k equivalent to a path in the
    given set of paths
k_distinct(path_set: Sequence[str],k: int)
    returns a boolean that is True if the paths in the given set are all
    k-distinct and False otherwise
maximal_set(e: int, n: int, k: int)
    returns a set of lattice paths with e east steps and n north steps given by
    the greedy algorithm, thought to be maximal
generate_table(e: int, n: int)
    returns a list of 2-element lists containing the cardinality of the supposed
    maximal set of e by n lattice paths for all k
all_maximal_sets(e: int, n: int, k:int)
    returns a list of maximal sets of k distinct paths using the greedy
    algorithm
find_distinct_set(e: int, n: int, k: int, a: int)
    returns a k-distinct set of size a of lattice paths on an e by n lattice
find_all_distinct_sets(e: int, n: int)
    generator function that returns all k-distinct sets on the e by n lattice
    for all k
table_str(t: Sequence[Sequence[int]])
    returns a printable string given a table returned by generate_table
set_to_str(t: tuple[str])
    returns a string
"""

import os
from sys import argv
from math import comb, floor
from itertools import combinations
from functools import reduce
from pandas import DataFrame

class LexOrderer:
    """
    A iterator class that returns lattice paths in lexicographic order.

    ...

    Methods
    -------
    LexOrderer(e_num: int, n_num: int)
        Return a LexOrderer iterator that will return the lattice paths with
        e_num east steps and n_num north steps in lexicographic order.
    """

    def __init__(self, e_num, n_num):
        """
        Parameters
        ----------
        e_num : int
            number of east steps in the lattice steps
        n_num : int
            number of north steps in the lattice steps
        """
        self.e_num = e_num
        self.n_num = n_num
        self.path_length = e_num + n_num
        self.string = ''
        self.__first = True

    def __iter__(self):
        """
        Start iteration.
        """
        self.string = 'E'*self.e_num+'N'*self.n_num
        self.__first = True
        return self

    def __next__(self):
        """
        Returns the next path in lexicographic order.
        """
        if self.string == 'N'*self.n_num + 'E'*self.e_num:
            raise StopIteration
        if self.__first:
            self.__first = False
            return self.string
        e_loc = list(self.__find_all_e())
        trail = self.__trailing_e()
        swap = e_loc[-1*trail-1]
        self.string = (self.string[:swap]+self.string[swap+1]+
                          self.string[swap]+self.string[swap+2:])
        self.__reverse(swap+2,self.path_length-1)
        return self.string

    def __len__(self):
        """
        Number of lattice paths.
        """
        return comb(self.e_num+self.n_num,self.e_num)

    def __trailing_e(self):
        """
        Returns the number of trailing e's in the current path string.
        """
        count = 0
        for x in self.string[-1::-1]:
            if x=='N':
                return count
            count+=1
        return count

    def __reverse(self, x, y):
        """
        Reverses the part of the current path string between indeicesx and y.
        """
        s = self.string
        while x < y:
            s = s[:x]+s[y]+s[x+1:y]+s[x]+s[y+1:]
            x += 1
            y -= 1
        self.string = s

    def __find_all_e(self):
        """
        Find the locations of all e's in the current path string.
        """
        s = self.string
        idx = s.find('E')
        while idx != -1:
            yield idx
            idx = s.find('E', idx + 1)

class Edges:
    """
    A iterator class that returns the edges in a lattice path.

    ...

    Methods
    -------
    Edges(path: str)
        Return an Edges iterator that will return the edges of a particular
        lattice path in order. The edges are in the form (x1, y1, x2, y2).
    """

    def __init__(self, path):
        """
        Parameters
        ----------
        path : str
            The path whose edges will be returned.
        """
        self.path = path
        self.length = len(path)
        self.index = 0
        self.loc = [0,0]

    def __iter__(self):
        """
        Start iteration.
        """
        self.index = 0
        self.loc = [0,0]
        return self

    def __next__(self):
        """
        Returns the next edge in the lattice path.
        """
        if self.index == self.length:
            raise StopIteration
        old_loc = self.loc.copy()
        if self.path[self.index]=='E':
            self.loc[0]+=1
        else:
            self.loc[1]+=1
        self.index += 1
        return tuple(old_loc+self.loc)

    def __len__(self):
        """
        Length of the lattice patha.
        """
        return self.length

class DistinctSets:
    """
    A iterator class that returns the sets of size size of k-disinct paths on
    the e by n lattice.

    ...

    Methods
    -------
    DistinctSets(e: int, n: int, k: int, size: int)
        Returns a DistinctSets iterator that will return the k-distinct sets of
        size size of lattice paths on the e by n lattice.
    """

    def __init__(self,e,n,k,size):
        """
        Parameters
        ----------
        e : int
            The number of east steps in the lattice.
        n : int
            The number of north steps in the lattice.
        k : int
            The number of edges two paths must share to be equivalent.
        size : int
            The size of set to try to find.
        """
        self.e = e
        self.n = n
        self.k = k
        self.combo_size = size
        self.combos = None
        self.index = 0
        self.num_combos = comb(comb(e+n,e),size)
        self.next_set = None
        self.has_next_set = True

    def __iter__(self):
        """
        Prepare for iteration.
        """
        self.combos = tuple(combinations(LexOrderer(self.e,self.n),
                                         self.combo_size))
        self.index = 0
        self.has_next_set = True
        self.__get_next_distinct_set()
        return self

    def __next__(self):
        """
        Returns the next size-size k-distinct set of lattice paths on the e by n
        lattice.
        """
        if self.has_next_set:
            set_to_return = self.next_set
            self.__get_next_distinct_set()
            return set_to_return
        raise StopIteration

    def __get_next_distinct_set(self):
        """
        Indicates whether there are any remaining k-disinct sets to return. If
        there are, sets the the next_set attribute to the next available set of
        k-distinct lattice_paths.
        """
        if self.index>=self.num_combos:
            self.has_next_set = False
            self.next_set = None
        else:
            while not k_distinct(self.combos[self.index],self.k):
                self.index += 1
                if self.index>=self.num_combos:
                    self.has_next_set = False
                    break
            if self.has_next_set:
                self.next_set = self.combos[self.index]
                self.index += 1
            else:
                self.next_set = None

def equivalent(edges1, edges2, k):
    """
    Determines whether or not the lattice paths given by the two edges are
    k-equivalent.

    Parameters
    ----------
    edges1 : Sequence[tuple]
        A list of edges of the form (x1, y1, x2, y2)
    edges2 : Sequence[tuple]
        A list of edges of the form (x1, y1, x2, y2)
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    boolean
        True if the paths are k-equivalent, False otherwise
    """
    if k==0:
        return True
    overlap = 0
    for edge1, edge2 in zip(edges1,edges2):
        if edge1 == edge2:
            overlap+=1
            if overlap==k:
                return True
    return False

def equivalent_in_set(path, path_set, k):
    """
    Determines whether or not the lattice path given is k-equivalent to any
    paths in the given set of paths.

    Parameters
    ----------
    path : str
        A lattice paths
        ex: 'EEENNNN'
    path_set : Sequence[str]
        A set of lattice paths
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    boolean
        True if the path is k-equivalent to one in the set, False otherwise
    """
    for p in path_set:
        if equivalent(Edges(path),Edges(p),k):
            return True
    return False

def k_distinct(path_set,k):
    """
    Determines whether or not the given set of lattice paths is k-distinct.

    Parameters
    ----------
    path_set : Sequence[str]
        A set of lattice paths
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    boolean
        True if the paths are k-distinct, False otherwise
    """
    equiv = False
    for i in range(1,len(path_set)):
        if equivalent_in_set(path_set[i-1], path_set[i:], k):
            equiv = True
            break
    return not equiv

def maximal_set(e, n, k):
    """
    Returns a set of k-distinct lattice paths generated by a greedy algorithm.

    Parameters
    ----------
    e : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    Sequence[str]
        A list of k-distinct lattice paths
    """
    path_set = []
    for path in LexOrderer(e,n):
        if not equivalent_in_set(path, path_set, k):
            path_set.append(path)
    return path_set

def generate_table(e, n):
    """
    Returns a set of pairs of k and P(e,n,k) values.

    Parameters
    ----------
    e : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths

    Returns
    -------
    Sequence[Sequence[int]]
        A set of pairs of k and P(e,n,k) values.
    """
    table = []
    for k in range(e+n+1):
        table.append([k,len(maximal_set(e, n, k))])
    return table

def all_maximal_sets(e,n,k):
    """
    Returns a list of maximal sets of k distinct paths.

    Parameters
    ----------
    e : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    list[list[str]]
        a list of lists of k-distinct paths that have the same cardinality as
        that given by the greedy algorithm
    """
    sets = [maximal_set(e, n, k)]
    cardinality = len(sets[0])
    for combo in combinations(LexOrderer(e,n), cardinality):
        add = True
        if reduce(lambda x, y : x and y,
                  map(lambda p, q: p == q,sets[0],combo), True):
            continue
        for i in range(1,len(combo)):
            if equivalent_in_set(combo[i-1], combo[i:], k):
                add = False
                break
        if add:
            sets.append(combo)
    return sets

def find_distinct_set(e,n,k,a):
    """
    Returns a k-distinct set of lattice paths on an e by n lattice. The set will
    be of size a, or None will be returned.

    Parameters
    ----------
    e : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent
    a : int
        The size of the k-distinct set to generate

    Returns
    -------
    tuple[str]
        a tuple containing a k-distinct lattice paths, or None if none exists
    """
    for combo in combinations(LexOrderer(e,n),a):
        if k_distinct(combo,k):
            return combo
    return None

def find_all_distinct_sets(e,n):
    """
    A generator function that returns all k-distinct sets on the e by n lattice
    for all k.

    Parameters
    ----------
    e : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths

    Returns
    -------
    Sequence[tuple[int, int, int,int, tuple[str]]]
        a sequence of tuples of the form [e, n, k, P(e,n,k), set], where set is
        of cardinality P and contains k-distinct paths from the e by n lattice
    """
    e_plus_n=e+n
    num_paths = comb(e_plus_n,e)
    for size in range(1,num_paths+1):
        count = 0
        for k in range(e_plus_n+1):
            for set_ in DistinctSets(e,n,k,size):
                yield (e,n,k,size,set_)
                count += 1
        if not count:
            break


def generate_data(starting_dimension):
    """
    Continually generates sets of distinct lattice paths and saves them in
    files.

    Parameters
    ----------
    starting_dimension : int
        starting sum of the north and east steps
    """
    m_plus_n = starting_dimension
    if not os.path.exists('./data'):
        os.mkdir('./data')
    while True:
        for i in range(1,floor(m_plus_n/2)+1):
            data = DataFrame(columns = ['E', 'N', 'k', 'C','paths','is_greedy'])
            greedies = [tuple(maximal_set(m_plus_n-i,i,k)) for k in
                                                              range(m_plus_n+1)]
            for set_data in find_all_distinct_sets(m_plus_n-i,i):
                new_data = {
                    'E': set_data[0],
                    'N': set_data[1],
                    'k': set_data[2],
                    'C': set_data[3],
                    'paths': set_to_str(set_data[4]),
                    'is_greedy': set_data[4] in greedies
                }
                data = data.append(new_data, ignore_index=True)

            #data['is_greedy'] = [row.paths in greedies for i,row in
            #                                                    data.iterrows()]
            #data['paths'] = data['paths'].map(set_to_str)
            #print(data)
            data.to_csv(f'./data/{m_plus_n-i}by{i}lattice.csv',index=False)
        m_plus_n += 1

def table_str(t):
    """
    Returns a string of the table that can be printed.

    Parameters
    ----------
    t : Sequence[Sequence[int]]
        A list containing 2-element lists containing the cardinality of the
        supposed maximal set of e by n lattice paths for all k

    Returns
    -------
    str
        A string of the table for pretty-printing.
    """
    matrix = [['k','P']] + t
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)

def set_to_str(set_):
    """
    Returns a string for storing in a csv.

    Parameters
    ----------
    set_ : tuple[str]
        A set of lattice paths

    Returns
    -------
    str
        A string of lattice paths
    """
    return str(set_).replace('(','{').replace(')','}').replace('\'','')

if __name__=="__main__":
    generate_data(int(argv[1]))
