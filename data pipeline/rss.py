# %%
import feedparser
import pandas as pd
from datetime import datetime
import os

rss_dictionary = {
    'cnbc_finance': "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    'yahoo_finance': 'https://news.yahoo.com/rss/finance',
    'hkgov_finance': 'https://www.news.gov.hk/tc/categories/finance/html/articlelist.rss.xml',
    'rthk_finance': 'https://rthk.hk/rthk/news/rss/c_expressnews_cfinance.xml',
    'scmp_china': 'https://www.scmp.com/rss/4/feed',
    
}
rss_sorting_critiria = ['YYYY', 'MM', 'DD', 'hh', 'mm', 'ss']
rss_header = ['Date', 'Title', 'YYYY', 'MM', 'DD', 'hh', 'mm', 'ss']

def get_feed(url: str):

    # Form the rss feed and the buffer
    feed = feedparser.parse(url)
    feed_buffer : list = []

    if not feed.bozo == 0:  # bozo == 0 means no XML errors, feed is valid
        print("Error: Could not parse the RSS feed. Check the URL.")
        print(feed.bozo_exception)  # Show the specific XML parsing error message.  If you aren't able to run, it is likely the URL no longer is valid.
        return

    for entry in feed.entries:
        """ 
        Variables:

            - entry.title : Stocks making the biggest moves premarket: Nvidia, Box, Dollar Tree, Ford and more
            - entry.published : Wed, 05 Mar 2025 14:21:39 GMT   <-- String
            - entry.published_parsed : (2025, 3, 5, 14 ...      <-- Array-like

        """
        # Put in buffer and sort by the time array
        feed_buffer.append([entry.published, entry.title] + list(entry.published_parsed)[:6])
    
    feed_buffer = zip(*feed_buffer)

    feed_map : dict = {}
    for k, v in zip(rss_header, feed_buffer):
        feed_map[k] = v

    df = pd.DataFrame(feed_map)
    df = df.sort_values(by=rss_sorting_critiria)
    return df

# %%
def buffer_to_csv(buffer: pd.DataFrame) -> str:
    if buffer is None:
        print(f'Dataframe is empty, skipping')
        return        
    # Make sure path is ok
    def dir(path):
        if not os.path.exists(path): 
            os.makedirs(path) 
        return path

    # Good file name
    formatted_time = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')

    # Write to the relative path
    path = dir(r'buffer/') + formatted_time + '.csv'
    df = buffer
    df.to_csv(path, index=False)
    
    print(f"- Written to csv {path}")
    return path

# %%
def find_diff(storage: pd.DataFrame, pending: pd.DataFrame):
    merged = pending.merge(storage, on=list(pending.columns), how='left', indicator=True)
    new_rows = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    return new_rows

# %%
def merge_diff(path: str, pending: pd.DataFrame) -> pd.DataFrame:

    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            storage = pd.read_csv(path, encoding='utf-8-sig')
        except pd.errors.EmptyDataError:
            # File exists but is empty: initialize with feed
            pending.to_csv(path, index=False, encoding='utf-8-sig')
            return
    else:
        # File doesn't exist: create it with feed
        pending.to_csv(path, index=False, encoding='utf-8-sig')
        return
    # Find new rows in feed that are not in storage

    new_rows = find_diff(storage, pending)
    
    if not new_rows.empty:
        # Append only new rows to the CSV
        new_rows.to_csv(path, mode='a', header=False, index=False, encoding='utf-8-sig')


# %%
def fetch_and_merge(url: str, path: str ='merged.csv', create_temp_files: bool = True):
    storage_path = path
    feed = get_feed(url)
    if feed is None:
        print(f'Feed is empty, skipping')
        return
    if create_temp_files:
        buffer_to_csv(feed)

    merge_diff(storage_path, feed)


# %%
def batch_fetch(*urls: str) -> pd.DataFrame:
    source = pd.DataFrame()
    for url in urls:
        diff = find_diff(source, get_feed[url])
        pd.concat([source, diff])
    return source

# %%
from time import sleep


if __name__ == '__main__':
    feed_df_list : list[pd.DataFrame] = []
    for k,v in rss_dictionary.items():
        feed_df_list.append(get_feed(v))
        sleep(.5)
    df = pd.concat(feed_df_list).sort_values(by=rss_sorting_critiria)
    buffer_to_csv(df)
    merge_diff('merged.csv', df)

# %%



