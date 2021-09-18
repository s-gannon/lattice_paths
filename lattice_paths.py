"""
A module for handling lattice paths, especially for determining k-equivalence.

...

Classes
-------
LexOrderer
    generator for lattice paths in lexicographic order
Edges
    generator for the edges traversed by a lattice path

Functions
---------
equivalent(edges1: Sequence[tuple[int]], edges2: Sequence[tuple[int]], k: int)
    returns a boolean that is True if the paths that the edge sets correspond to
    are k equivalent
equivalent_in_set(path: str, path_set: Sequence[str], k: int)
    returns a boolean that is True if the path is k equivalent to a path in the
    given set of paths
maximal_set(e: int, n: int, k: int)
    returns a set of lattice paths with e east steps and n north steps given by
    the greedy algorithm, thought to be maximal
generate_table(e: int, n: int)
    returns a list of 2-element lists containing the cardinality of the supposed
    maximal set of e by n lattice paths for all k
table_str(t: Sequence[Sequence[int]])
    returns a printable string given a table returned by generate_table
"""

from math import factorial

class LexOrderer:
    """
    A generator class that returns lattice paths in lexicographic order.

    ...

    Methods
    -------
    LexOrderer(e_num: int, n_num: int)
        Return a LexOrderer generator that will return the lattice paths with
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
        self.string = self.string[:swap]+self.string[swap+1]+
                          self.string[swap]+self.string[swap+2:]
        self.__reverse(swap+2,self.path_length-1)
        return self.string

    def __len__(self):
        """
        Number of lattice paths.
        """
        return factorial(self.e_num+self.n_num)/
                        (factorial(self.e_num)*factorial(self.e_num))

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
    A generator class that returns the edges in a lattice path.

    ...

    Methods
    -------
    Edges(path: str)

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
        Length of the lattice path.
        """
        return self.length

def equivalent(edges1, edges2, k):
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
    for p in path_set:
        if equivalent(Edges(path),Edges(p),k):
            return True
    return False

def maximal_set(e, n, k):
    path_set = []
    for path in LexOrderer(e,n):
        if not equivalent_in_set(path, path_set, k):
            path_set.append(path)
    return path_set

def generate_table(e, n):
    table = []
    for k in range(e+n+1):
        table.append([k,len(maximal_set(e, n, k))])
    return table

def table_str(t):
    matrix = [['k','P']] + t
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)

if __name__=="__main__":
    test = {'e':4,'n':3}
    print(table_str(generate_table(**test)))
