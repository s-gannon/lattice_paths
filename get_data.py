from sys import argv
import lattice_paths as lp
from pandas import DataFrame

if __name__=="__main__":
    m = int(argv[1])
    n = int(argv[2])
    if len(argv)>4:
        filename = argv[3]
        incremental = argv[4][0]=='i'
    elif len(argv)>3:
        filename = argv[3]
        incremental = False
    else:
        filename = f"lattice{m}by{n}data.tsv"
        incremental = False
    if incremental:
        results = DataFrame(columns = ['m','n','k','greedy_cardinality',
                                       'max_cardinality','greedy_set',
                                       'max_sets', 'greedy_is_max'])
        for k in range(m+n+1):
            results = results.append(lp.greedy_max_comparison(m,n,k),
                                     ignore_index=True)
            results.to_csv(filename, sep='\t', index=False)
    else:
        results = lp.greedy_max_comparison_table(m,n)
        results.to_csv(filename, sep='\t', index=False)
