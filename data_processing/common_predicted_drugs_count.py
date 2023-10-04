#!/usr/bin/env python3

"""
This script compares predictions of two models on the same data.
For each prediction file (100 predicted interactions for a specific drug/food), it counts the number of common predicted drugs/foods.
Finally, it returns an average of all counts of common predicted drugs/foods.
"""



import pandas as pd
import sys
from os import listdir
import re


model1 = sys.argv[1]
model2 = sys.argv[2]
path = sys.argv[3]


def common_drugs_count(path1, path2):
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    drugs1 = set(df1.tail_label.values)
    drugs2 = set(df2.tail_label.values)

    common_drugs = drugs1.intersection(drugs2)

    if len(common_drugs) > 30:
        pattern = r'_(FDB\d+|DB\d+)_'
        match = re.search(pattern, path1)
        if match:
            extracted_id = match.group(1)
            print(f'Number of common predicted drugs for {extracted_id}: {len(common_drugs)}')

    return len(common_drugs)

def avg_common_drugs(model1, path):
    files = listdir(path)

    model1_files = []
    model2_files = []

    for file in files:
        if model1 in file:
            model1_files.append(file)
        else:
            model2_files.append(file)

    pairs = []
    pattern = r'_(FDB\d+|DB\d+)_'
    for file1 in model1_files:
        match = re.search(pattern, file1)
        if match:
            extracted_id = match.group(1)
        else:
            continue

        for file2 in model2_files:
            if extracted_id in file2:
                pairs.append((file1, file2))
                break

    
    avg_common_drugs_count = 0
    for file1, file2 in pairs:
        avg_common_drugs_count += common_drugs_count(path + file1, path + file2)

    avg_count = avg_common_drugs_count / len(pairs)

    print("Average common drugs count:", avg_count)

avg_common_drugs(model1, path)