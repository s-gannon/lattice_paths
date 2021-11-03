from sys import argv
import pandas as pd

def go_output_to_df(filename):
    df = pd.read_csv(filename,sep="\t", header=None,names=["m","n","k","greedy_order","max_order","greedy_is_max","greedy_set","max_sets"])
    df = df.sort_values("k").reset_index()
    df.greedy_set = [x[1:-1].split(", ") for x in df.greedy_set]
    df.max_sets = [x.split(", ") for y in df.max_sets for x in y[2:-2].split("], [")]
    return df

if __name__=="__main__":
    print(go_output_to_df(argv[1]))
