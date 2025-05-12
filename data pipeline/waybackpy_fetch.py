# %%
from time import sleep
import waybackpy
import rss
from datetime import datetime, timedelta

def get_archives(url, year_back=1):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    try:
        # Initialize with timeframe filter
        archive = waybackpy.WaybackMachineCDXServerAPI(
            url=url,
            user_agent=user_agent,
            start_timestamp=(datetime.now() - timedelta(days=365*year_back)).strftime("%Y%m%d"),
            end_timestamp=datetime.now().strftime("%Y%m%d"),
            filters=["statuscode:200"]  # Only successful captures
        )
        
        snapshots = []
        for snapshot in archive.snapshots():
            snapshots.append({
                "timestamp": snapshot.datetime_timestamp,
                "original_url": snapshot.original,
                "archive_url": snapshot.archive_url
            })
        return snapshots
    
    except Exception as e:
        print(f"Error: {e}")
        return []

archived_rss_links = get_archives(rss.rss_dictionary['cnbc_finance'], year_back=2)
print(f'{len(archived_rss_links)} archive(s) are found\n')
input(f'Press Enter to proceed with {len(archived_rss_links)} captures')


for idx, snap in enumerate(archived_rss_links, 1):
    print(f"   Archived at: {snap['timestamp']}")
    print(f"   Snapshot: {snap['archive_url']}\n")
    rss.fetch_and_merge(snap['archive_url'], 'cnbc_merged.csv', create_temp_files=False)
    sleep(1)


# %%



