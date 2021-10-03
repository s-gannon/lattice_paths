from sys import argv
import lattice_paths as lp

if __name__=="__main__":
    m = int(argv[1])
    n = int(argv[2])
    if len(argv>3):
        filename = argv[3]
    else:
        filename = f"lattice{m}by{n}data.tsv"
    results = lp.greedy_max_comparison(m,n)
    results.to_csv(filename, sep='\t', index=False)
