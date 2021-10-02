from sys import argv
import lattice_paths as lp

if __name__=="__main__":
    m = int(argv[1])
    n = int(argv[2])
    results = lp.greedy_max_comparison(m,n)
    results.to_csv(f"lattice{m}by{n}data.tsv", sep='\t', index=False)
