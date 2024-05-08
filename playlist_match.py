
import pandas as pd
import numpy as np
from rapidfuzz import fuzz, utils
from rapidfuzz.process import extract

CUTOFF = 60

playlist_df = pd.read_csv('./yt_playlists.csv')
# Skip channels that don't have content on the RT site
non_site_channels = ['RT Labs', 'ScrewAttack Live', 'Game Kids', 'GameFails', 'LetsPlay Community']
playlist_df = playlist_df[~playlist_df['yt_channel'].isin(non_site_channels)]

channel_pl_df = playlist_df[['yt_channel','playlist_nm', 'playlist_url']].drop_duplicates()
dupes = channel_pl_df.loc[channel_pl_df['playlist_nm'].duplicated(), 'playlist_nm']
dupe_df = channel_pl_df[channel_pl_df['playlist_nm'].isin(dupes)]

shows_df = pd.read_csv('./rt_watch.csv')
shows_df = shows_df[shows_df['is_sponsors_only'] == False]
# shows_df = shows_df[shows_df['type'] == 'episode']
show_title_df = shows_df[['channel_slug', 'show_title', 'show_url']].drop_duplicates()
rt_dupes = show_title_df.loc[show_title_df.duplicated(subset=['show_title']), 'show_title']
rt_dupe_df = show_title_df[show_title_df['show_title'].isin(rt_dupes)]

channel_pl_df['matches'] = channel_pl_df['playlist_nm'].apply(lambda x: extract(query=x, choices=show_title_df['show_title'], scorer=fuzz.token_sort_ratio, score_cutoff=CUTOFF, processor=utils.default_process))
channel_pl_df["best_match"] = channel_pl_df["matches"].apply(lambda x: x[0][0] if x else np.nan)
# yt_df["likeness"] = yt_df["matches"].apply(lambda x: x[0][1] if x else np.nan)

merged_df = channel_pl_df.merge(show_title_df, how="outer", left_on="best_match", right_on="show_title", suffixes=['_yt', '_rt'])

merged_df.to_csv('./show_title_match.csv', index=False)
print()