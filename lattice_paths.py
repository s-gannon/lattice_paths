class LexOrderer:

    def __init__(self, e_num, n_num):
        self.e = e_num
        self.n = n_num
        self.length = e_num + n_num
        self.string = 'E'*self.e+'N'*self.n
        self.first = True

    def __iter__(self):
        self.string = 'E'*self.e+'N'*self.n
        self.first = True
        return self

    def __next__(self):
        if self.string == 'N'*self.n + 'E'*self.e:
            raise StopIteration
        if self.first:
            self.first = False
            return self.string
        e_loc = list(self.find_all_e())
        trail = self.trailing_e()
        swap = e_loc[-1*trail-1]
        self.string = self.string[:swap]+self.string[swap+1]+self.string[swap]+self.string[swap+2:]
        self.reverse(swap+2,self.length-1)
        return self.string

    def trailing_e(self):
        count = 0
        for x in self.string[-1::-1]:
            if x=='N':
                return count
            count+=1
        return count

    def reverse(self, x, y):
        s = self.string
        while x < y:
            s = s[:x]+s[y]+s[x+1:y]+s[x]+s[y+1:]
            x += 1
            y -= 1
        self.string = s

    def find_all_e(self):
        s = self.string
        idx = s.find('E')
        while idx != -1:
            yield idx
            idx = s.find('E', idx + 1)

class Edges:

    def __init__(self, path):
        self.path = path
        self.length = len(path)
        self.index = 0
        self.loc = [0,0]

    def __iter__(self):
        self.index = 0
        self.loc = [0,0]
        return self

    def __next__(self):
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
