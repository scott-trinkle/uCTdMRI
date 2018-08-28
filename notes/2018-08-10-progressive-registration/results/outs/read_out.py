import numpy as np
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt


def parse_outfile(fn):

    # Reads file line-by-line into list
    full_file = [line for line in open(fn, 'r')]

    # Gets start and stop indices for data from all three "stages"
    data_starts = []
    data_stops = []
    for i, line in enumerate(full_file):
        if ('Stage' in line) & ('State' not in line):
            for j in range(20):
                if 'DIAGNOSTIC' in full_file[i + j]:
                    data_starts.append(i + j)
                    break
        if 'Elapsed' in line:
            data_stops.append(i)

    # Length-3 list with lines data section of file
    data_str_all_stages = [full_file[data_starts[i]:data_stops[i]]
                           for i in range(3)]

    dfs = []  # initializing list of dataframes
    for data_str_stage in data_str_all_stages:

        columns = data_str_stage[0].replace('\n', '').split(',')[1:]

        stage = 0
        full_data = []
        for i, line in enumerate(data_str_stage):
            # Results in list of data values for a single line
            line_data = line.replace(', \n', '').replace(
                ' ', '').replace('\n', '').split(',')[1:]

            if np.any(line_data != columns):
                full_data.append([stage] + line_data)
            else:
                stage += 1

        df = pd.DataFrame(data=full_data, columns=['Stage'] + columns).apply(
            pd.to_numeric, errors='ignore')
        df.set_index(['Stage'], inplace=True)
        df[df > 1e300] = np.nan
        dfs.append(df)

    return dfs


# Gets test filename
fns = [fn for fn in glob('*_*.out') if 'sampled' not in fn]

for fn in fns:
    trans, aff, deform = parse_outfile(fn)
    lab = fn.split('.out')[0]
    if (deform.convergenceValue.min() > 1e-6) & (deform.Iteration.iloc[-1] == 20):
        print(lab, '\n')
