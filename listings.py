"""Core module for fetching and validating Carbonite listings."""
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def fetch(url, check_only=False):
    """Fetch listing data from URL.
    
    Args:
        url: Listing URL
        check_only: If True, only check status (faster)
    
    Returns:
        dict with listing data or error info
    """
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        if r.status_code == 404:
            return {'url': url, 'status': 'deleted', 'checked_at': datetime.now(timezone.utc).isoformat()}
        
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.title.string.split('|')[0].strip() if soup.title else url
        status = 'sold' if '(sold)' in title.lower() else 'active'
        
        if check_only:
            return {'url': url, 'status': status, 'title': title, 'checked_at': datetime.now(timezone.utc).isoformat()}
        
        data = {'url': url, 'title': title, 'status': status, 'fetched_at': datetime.now(timezone.utc).isoformat()}
        for dl in soup.select('div.blockStatus-message dl[data-field]'):
            field = dl['data-field']
            dd = dl.find('dd')
            if dd:
                data[field] = dd.get_text(strip=True)
        
        return data if len(data) > 4 else {**data, 'error': 'No data block found'}
    except Exception as e:
        return {'url': url, 'error': str(e), 'status': 'error', 'checked_at': datetime.now(timezone.utc).isoformat()}

def validate(records):
    """Validate listing records by checking their current status.
    
    Args:
        records: List of listing dicts with 'url' field
        
    Yields:
        tuple of (index, record, result) for each validation
    """
    for i, rec in enumerate(records):
        result = fetch(rec['url'], check_only=True)
        rec['status'] = result['status']
        rec['checked_at'] = result.get('checked_at')
        yield i, rec, result
