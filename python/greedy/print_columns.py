from sys import argv
from convert_go_data import go_output_to_df

def print_columns(filename, k, is_go_data=True):
    if is_go_data:
        df = go_output_to_df(filename)
    gs = df.loc[k]['greedy_set']
    mss = df.loc[k]['max_sets']
    for max_set in mss:
        for i, x in enumerate(max_set):
            if i<len(gs):
                print(gs[i]+"\t\t"+x)
            else:
                print(' '*len(str(gs[0]))+"\t\t"+x+"\n")

if __name__=="__main__":
    args = argv[1:]
    if len(args)==2:
        print_columns(args[0], int(args[1]), is_go_data=True)
    elif len(args)==3:
        print_columns(args[0], int(args[1]), is_go_data=(args[2].lower in s.lower() in ['true', '1', 't', 'y', 'yes']))
