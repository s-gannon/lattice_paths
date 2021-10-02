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
equivalent(path_edges_1: Sequence[tuple[int]], path_edges_2: Sequence[tuple[int]], k: int)
    returns a boolean that is True if the paths that the edge sets correspond to
    are k equivalent
equivalent_in_set(path: str, path_set: Sequence[str], k: int)
    returns a boolean that is True if the path is k equivalent to a path in the
    given set of paths
k_distinct(path_set: Sequence[str],k: int)
    returns a boolean that is True if the paths in the given set are all
    k-distinct and False otherwise
greedy_set(m: int, n: int, k: int)
    returns a set of lattice paths with e east steps and n north steps given by
    the greedy algorithm
generate_table(m: int, n: int)
    returns a list of 2-element lists containing the cardinality of the greedy
    sets of e by n lattice paths for all k
all_greedy_size_sets(m: int, n: int, k:int)
    returns a list of sets of k distinct paths that have the same cardinality as
    the set given by the greedy algorithm
find_distinct_set(m: int, n: int, k: int, a: int)
    returns a k-distinct set of size a of lattice paths on an e by n lattice
find_all_distinct_sets(m: int, n: int)
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
    LexOrderer(m: int, n: int)
        Return a LexOrderer iterator that will return the lattice paths with
        m east steps and n north steps in lexicographic order.
    """

    def __init__(self, m, n):
        """
        Parameters
        ----------
        m : int
            number of east steps in the lattice steps
        n : int
            number of north steps in the lattice steps
        """
        self.m = m
        self.n = n
        self.path_length = m + n
        # self.string is the current path in the generator
        # it will look something like: 'EEEENNN'
        self.string = ''
        # self.__first tracks whether we are at the beginning
        # this is important to avoid off-by-one issues
        self.__first = True

    def __iter__(self):
        """
        Start iteration.
        """
        # This method is called before a loop starts getting values from the
        # iterator
        # The following line sets the beginning path (all E's before all N's)
        self.string = 'E'*self.m+'N'*self.n
        self.__first = True
        return self

    def __next__(self):
        """
        Returns the next path in lexicographic order.
        """
        # The following lines check to see if the current string is final
        # (all N's before all E's). If it is, we stop.
        if self.string == 'N'*self.n + 'E'*self.m:
            raise StopIteration
        # If this is the first value, we have already calculated the string, so
        # we can just return it
        if self.__first:
            self.__first = False
            return self.string
        # Otherwise, find where all the e's are
        e_loc = list(self.__find_all_e())
        # then, find how many e's are at the end of the current path
        trail = self.__trailing_e()
        # we will move the last e that has an n after it
        swap = e_loc[-1*trail-1]
        self.string = (self.string[:swap]+self.string[swap+1]+
                          self.string[swap]+self.string[swap+2:])
        # Then, we reverse everything after the move
        self.__reverse(swap+2,self.path_length-1)
        # we have the next string, so we return it
        return self.string

    def __len__(self):
        """
        Number of lattice paths.
        """
        # this function gives the "length" of the iterator, which is the number
        # of possible paths on the given lattice
        return comb(self.m+self.n,self.m)

    def __trailing_e(self):
        """
        Returns the number of trailing e's in the current path string.
        """
        count = 0
        # This loop iterates over the current path string in reverse order
        for x in self.string[-1::-1]:
            # if we encounter an N, we're done
            if x=='N':
                return count
            count+=1
        return count

    def __reverse(self, x, y):
        """
        Reverses the part of the current path string between indices x and y,
        inclusive.
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
        # The optional second argument of string.find() is the index to start
        # looking at. When there are no E's after the index, find() returns -1
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
        # self.path will be of the form "EENEENE"
        self.path = path
        self.length = len(path)
        # self.index tracks our position along the path string
        self.index = 0
        # self.loc tracks our position on the lattice
        self.loc = [0,0]

    def __iter__(self):
        """
        Start iteration.
        """
        # When we start iterating, make sure we start at the beginning
        self.index = 0
        self.loc = [0,0]
        return self

    def __next__(self):
        """
        Returns the next edge in the lattice path.
        """
        # If we've reached the end of the string, stop
        if self.index == self.length:
            raise StopIteration
        # track the previous location
        old_loc = self.loc.copy()
        # if the step letter at the current index is an E, we add an east step
        # to our location
        if self.path[self.index]=='E':
            self.loc[0]+=1
        # if the step letter at the current index is not an E, we add a north
        # step to our location
        else:
            self.loc[1]+=1
        # increment the index
        self.index += 1
        # return the current previous location and the current location as the
        # next edge in the path
        return tuple(old_loc+self.loc)

    def __len__(self):
        """
        Length of the lattice path.
        """
        return self.length

class DistinctSets:
    """
    A iterator class that returns the sets of size size of k-disinct paths on
    the e by n lattice.

    This is really not a very good class. I would not recommend using it under
    most circumstances.

    ...

    Methods
    -------
    DistinctSets(e: int, n: int, k: int, size: int)
        Returns a DistinctSets iterator that will return the k-distinct sets of
        size size of lattice paths on the e by n lattice.
    """

    def __init__(self,m,n,k,size):
        """
        Parameters
        ----------
        m : int
            The number of east steps in the lattice.
        n : int
            The number of north steps in the lattice.
        k : int
            The number of edges two paths must share to be equivalent.
        size : int
            The size of set to try to find.
        """
        self.m = m
        self.n = n
        self.k = k
        self.combo_size = size
        # the combos variable will eventually contain all possible combinations
        # of the given size of paths
        self.combos = None
        # index tracks how many combos we've examined
        self.index = 0
        self.num_combos = comb(comb(m+n,m),size)
        self.next_set = None
        self.has_next_set = True

    def __iter__(self):
        """
        Prepare for iteration.
        """
        # generate all possible sets of paths
        self.combos = tuple(combinations(LexOrderer(self.m,self.n),
                                         self.combo_size))
        self.index = 0
        # this tracks whether there are any remaining distinct sets of the given
        # size
        self.has_next_set = True
        # this iterates over all the combinations until it finds one that is
        # distinct
        self.__get_next_distinct_set()
        return self

    def __next__(self):
        """
        Returns the next size-size k-distinct set of lattice paths on the e by n
        lattice.
        """
        # Whenever we get the next distinct set, we indicate if we have one
        # available. While we still do, we return the one we have and find the
        # next one
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
        # if we have gone through all the combos, we are done
        if self.index>=self.num_combos:
            self.has_next_set = False
            self.next_set = None
        else:
            # while the current set is not k distinct, go to the next one
            while not k_distinct(self.combos[self.index],self.k):
                self.index += 1
                if self.index>=self.num_combos:
                    self.has_next_set = False
                    break
            # once we find a distinct set, we store it in self.next_set
            if self.has_next_set:
                self.next_set = self.combos[self.index]
                self.index += 1
            else:
                self.next_set = None

def equivalent(path_edges_1, path_edges_2, k):
    """
    Determines whether or not the lattice paths given by the two edges are
    k-equivalent.

    Parameters
    ----------
    path_edges_1 : Sequence[tuple]
        A list of edges of the form (x1, y1, x2, y2)
    path_edges_2 : Sequence[tuple]
        A list of edges of the form (x1, y1, x2, y2)
    k : int
        The minimum number of shared edges required for two lattice paths to be
        considered equivalent

    Returns
    -------
    boolean
        True if the paths are k-equivalent, False otherwise
    """
    # when k is zero, any paths are equivalent
    if k==0:
        return True
    # variable to track the overlap
    overlap = 0
    # loops over the edges in each path simultaneously
    for edge1, edge2 in zip(path_edges_1,path_edges_2):
        # if the edges are equal, increment the overlap
        if edge1 == edge2:
            overlap+=1
            # if they share k edges, they are equivalent
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
    # Loop over all paths in the path set
    for p in path_set:
        # if our path is equivalent to the current other path, return true
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
    # assume we aren't equivalent
    equiv = False
    # loop over all the paths in the set (with an index variable)
    for i in range(1,len(path_set)):
        # check if the current path is equivalent to any of the following paths
        if equivalent_in_set(path_set[i-1], path_set[i:], k):
            equiv = True
            break
    return not equiv

def greedy_set(m, n, k):
    """
    Returns a set of k-distinct lattice paths generated by a greedy algorithm.

    Parameters
    ----------
    m : int
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
    # Iterate over the paths in lexicographic order
    for path in LexOrderer(m,n):
        # if the current path is not equivalent to any in our current set, add
        # it to the set
        if not equivalent_in_set(path, path_set, k):
            path_set.append(path)
    return path_set

def generate_table(m, n):
    """
    Returns a set of pairs of k and P(m,n,k) values.

    Parameters
    ----------
    m : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths

    Returns
    -------
    Sequence[Sequence[int]]
        A set of pairs of k and P(m,n,k) values.
    """
    table = []
    # iterates over all possible values of k
    for k in range(m+n+1):
        # record k and the length of the path given by the greedy algorithm
        table.append([k,len(greedy_set(m, n, k))])
    return table

def all_greedy_size_sets(m,n,k):
    """
    Returns a list of sets of k distinct paths with the same cardinality as the
    set given by the greedy algorithm.

    Parameters
    ----------
    m : int
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
    # first, create the greedy set and get its size
    sets = [greedy_set(m, n, k)]
    cardinality = len(sets[0])
    # loop over all possible sets of paths of the same size as the greedy set
    for combo in combinations(LexOrderer(m,n), cardinality):
        # we check to see if its the same as the greedy set so we don't
        # accidentally add it twice
        if reduce(lambda x, y : x and y,
                  map(lambda p, q: p == q,sets[0],combo), True):
            continue
        # check
        if not k_distinct(combo, k):
            sets.append(combo)
    return sets

def find_distinct_set(m,n,k,a):
    """
    Returns a k-distinct set of lattice paths on an m by n lattice. The set will
    be of size a, or None will be returned.

    Parameters
    ----------
    m : int
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
    # loop over all combinations of paths of a give size a
    for combo in combinations(LexOrderer(m,n),a):
        # if the paths are distinct, return the set
        if k_distinct(combo,k):
            return combo
    # if we get through the loop without returning anything, return None (null)
    return None

def find_all_distinct_sets(m,n):
    """
    A generator function that returns all k-distinct sets on the m by n lattice
    for all k.

    Parameters
    ----------
    m : int
        Number of east steps in the lattice paths
    n : int
        Number of north steps in the lattice paths

    Returns
    -------
    Sequence[tuple[int, int, int,int, tuple[str]]]
        a sequence of tuples of the form [m, n, k, P(m,n,k), set], where set is
        of cardinality P and contains k-distinct paths from the e by n lattice
    """
    m_plus_n=m+n
    num_paths = comb(m_plus_n,m)
    # this loop is for all possible sizes of sets of paths
    for size in range(1,num_paths+1):
        count = 0
        # this loop is for all possible k values
        for k in range(m_plus_n+1):
            # this loop is for all distinct sets for the given criteria
            for set_ in DistinctSets(m,n,k,size):
                yield (m,n,k,size,set_)
                count += 1
        # This small optimization tries to check if we get through an entire
        # size of set without finding any k-distinct sets. If that is true, we
        # don't want to check for any bigger sets because we would have found a
        # subset of that one
        if not count:
            break


def generate_data(starting_dimension):
    """
    DEPRECATED. This function is not esepcially useful. Don't use it.

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
            greedies = [tuple(greedy_set(m_plus_n-i,i,k)) for k in
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
            data.to_csv(f'./data/{m_plus_n-i}by{i}lattice.csv',index=False)
        m_plus_n += 1

def table_str(t):
    """
    Returns a string of the table that can be easily printed.

    Parameters
    ----------
    t : Sequence[Sequence[int]]
        A list containing 2-element lists containing the cardinality of the
        greedy set of e by n lattice paths for all k

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
    Returns a string of a set for saving to a file.

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
    pass
