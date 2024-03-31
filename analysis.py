
from datetime import datetime

import pandas as pd
import numpy as np
from rapidfuzz import fuzz, utils
from rapidfuzz.process import extract

CUTOFF = 85

def get_suffixes(df):
    df['title_split'] = df['Title'].str.split('|')
    df['title_suffix'] = df['title_split'].apply(lambda arr: arr[-1] if len(arr) > 1 else None)
    suffix_ct = df['title_suffix'].value_counts()
    df.drop(columns=['title_split'], inplace=True)
    return suffix_ct

# def get_prefixes(df, delim="-", threshold=2):
#     df['title_split'] = df['Title'].str.split(delim)
#     df['title_suffix'] = df['title_split'].apply(lambda arr: arr[0] if len(arr) > 1 else None)
#     prefix_ct = df['title_suffix'].value_counts()
#     # suffixes = suffix_ct[suffix_ct > threshold].index.tolist()
#     df.drop(columns=['title_split'], inplace=True)
#     return prefix_ct

matches_df = pd.read_csv('./output03-29-2024.csv')
yt_ia_matches = matches_df['YouTube IA Link']
rt_ia_matches = matches_df['RoosterTeeth Site IA Link']


# Get Youtube videos and filter out existing matches
yt_df = pd.read_csv('./ALL_RT_YouTube_Videos_Trimmed.csv')
yt_df = yt_df[~yt_df['IA Link'].isin(yt_ia_matches)]

# Get suffixes and remove any that appear more than twice
yt_suffix_ct = get_suffixes(yt_df)
suffixes = yt_suffix_ct[yt_suffix_ct > 2].index.tolist()
suffixes = ['|'+suffix for suffix in suffixes]
yt_df['title_cleaned'] = yt_df['Title'].copy()
for suffix in suffixes:
    yt_df['title_cleaned'] = yt_df['title_cleaned'].str.replace(suffix, '')

# Get RT site videos and filter out existing matches
rt_df = pd.read_csv('./ALL_RT_Site_Videos.csv')
rt_df = rt_df[~rt_df['IA Link'].isin(rt_ia_matches)]


# https://mlexplained.blog/2023/08/02/fuzzy-match-dataframes-using-rapidfuzz-and-pandas/
# see scorers https://medium.com/@kasperjuunge/rapidfuzz-explained-c26e93b6012d

print(f"Creating join keys: {datetime.now()}")
yt_df['matches'] = yt_df['title_cleaned'].apply(lambda x: extract(query=x, choices=rt_df['Title'], scorer=fuzz.token_sort_ratio, score_cutoff=CUTOFF, processor=utils.default_process))
yt_df["best_match"] = yt_df["matches"].apply(lambda x: x[0][0] if x else np.nan)
# yt_df["likeness"] = yt_df["matches"].apply(lambda x: x[0][1] if x else np.nan)
print(f"Finished join keys: {datetime.now()}")
merged_df = yt_df.merge(rt_df, how="inner", left_on="best_match", right_on="Title", suffixes=['_yt', '_rt'])
print(f"Merged the data: {datetime.now()}")

merged_df.to_csv('./merged.csv', index=False)
print()
