from sys import argv
import pandas as pd

def go_output_to_df(filename):
    df = pd.read_csv(filename,sep="\t", header=None,names=["m","n","k","greedy_order","max_order","greedy_is_max","greedy_set","max_sets"])
    df = df.sort_values("k")
    df.reset_index(inplace=True)
    df.drop(columns=["index"],inplace=True)
    df.greedy_set = [x[1:-1].split(", ") for x in df.greedy_set]
    df.max_sets = [[x.split(", ") for x in y[2:-2].split("], [")] for y in df.max_sets]
    return df

def order_go_output(filename):
    results = go_output_to_df(filename)
    results.to_csv(filename[:-4]+"new.tsv", sep='\t', index=False)

if __name__=="__main__":
    order_go_output(argv[1])
