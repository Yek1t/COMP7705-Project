# News Fetching from Wayback Machine

## Overview

This repository contains scripts for fetching archived RSS feeds from the Wayback Machine and processing them into structured CSV files. The system consists of two main components:

1. `waybackpy_fetch.py` - Wayback Machine archive retrieval
2. `rss.py` - RSS feed processing and data management

## Detailed Component Breakdown

### waybackpy_fetch.py

**Core Functionality:**

- Retrieves historical snapshots of RSS feeds from Internet Archive's Wayback Machine
- Filters for successful HTTP 200 responses only
- Processes each snapshot through the RSS pipeline

**Key Components:**

```python waybackpy_fetch.py
def get_archives(url, year_back=1):
    """Fetches archives with configurable time range (default: 1 year back)"""
    # Uses WaybackMachineCDXServerAPI with:
    # - Custom user agent
    # - Date range filtering
    # - Status code filtering
    # Returns list of snapshot dicts with:
    # - timestamp
    # - original_url
    # - archive_url
```

**Execution Flow:**

1. Fetches 2 years of CNBC finance feed archives (configurable)
2. Processes each snapshot with 1-second delay (rate limiting)
3. Merges results into 'cnbc_merged.csv'

### rss.py

**Core Functionality:**

- RSS feed parsing and normalization
- Temporal data processing
- CSV storage management
- Differential updates

**Key Components:**

#### Feed Configuration

```python rss.py
rss_dictionary = {
    # Predefined RSS feed URLs including:
    'cnbc_finance': "...",
    'yahoo_finance': "...",
    # ... other financial news sources
}

rss_sorting_critiria = ['YYYY', 'MM', 'DD', 'hh', 'mm', 'ss']  # Temporal sorting
rss_header = ['Date', 'Title', 'YYYY', 'MM', 'DD', 'hh', 'mm', 'ss']  # CSV structure
```

#### Core Functions

```python rss.py
def get_feed(url: str):
    """Parses RSS feed into structured DataFrame with:
    - Original published date (string)
    - Title
    - Split temporal components for sorting
    Handles feed validation (bozo detection)
    """

def fetch_and_merge(url: str, path: str ='merged.csv', create_temp_files: bool = True):
    """Orchestrates the complete workflow:
    1. Fetch feed
    2. Optionally create temp CSV
    3. Merge new entries into main storage
    """
```

#### Data Management

```python rss.py
def merge_diff(path: str, pending: pd.DataFrame):
    """Smart merge that:
    - Creates storage file if missing
    - Handles empty file cases
    - Only appends new entries
    - Maintains UTF-8 encoding
    """
```

## Workflow Diagram

```py
[Wayback Machine]
    ↓ (get_archives)
[Snapshot URLs]
    ↓ (fetch_and_merge)
[RSS Parser]
    ↓
[DataFrame Processing]
    ↓
[CSV Storage]
    ├─[Main Storage]
    └─[Temporary Files]
```

## Advanced Features

- **Temporal Precision**: Nanosecond-level timestamp parsing and sorting
- **Differential Updates**: Only stores new entries to avoid duplicates
- **Error Handling**:
  - Invalid feed detection (bozo flag)
  - Empty data safeguards
  - Filesystem checks
- **Modular Design**:
  - Configurable feed sources
  - Adjustable date ranges
  - Optional temp file generation

## Usage Examples

**Single Feed Processing:**

```bash
python waybackpy_fetch.py  # Processes CNBC archives
```

**Custom Feed Processing:**

```python
from rss import fetch_and_merge
fetch_and_merge(rss_dictionary['yahoo_finance'], 'yahoo_news.csv')
```

**Batch Processing:**

```python
from rss import batch_fetch
batch_fetch(*rss_dictionary.values())  # Processes all predefined feeds
```

## Environment

```text
feedparser==6.0.11
pandas==2.2.3
waybackpy==3.0.6
```

## Performance Notes

- Built-in 1-second delay between Wayback requests
- Configurable sleep intervals in main execution
- Memory-efficient DataFrame operations
- Optional temp file generation for debugging

## Error Handling Details

```python rss.py
def get_feed(url: str):
    """Includes comprehensive error handling for:
    - Invalid RSS feeds (bozo flag)
    - Network failures
    - Malformed date formats
    """
    feed = feedparser.parse(url)
    
    {{ Error Handling Section }}
    if not feed.bozo == 0:
        print("Error: Could not parse the RSS feed. Check the URL.")
        print(feed.bozo_exception)
        return None
```

```python waybackpy_fetch.py
def get_archives(url, year_back=1):
    """Handles Wayback Machine API errors including:
    - Rate limiting
    - Invalid URLs
    - Date range errors
    """
    try:
        {{ API Initialization }}
    except Exception as e:
        print(f"Error: {e}")
        return []
```
