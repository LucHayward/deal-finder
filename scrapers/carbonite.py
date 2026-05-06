"""Carbonite.co.za forum scraper."""
import re, time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from scrapers.base import Scraper
from scrapers import register

BASE = "https://carbonite.co.za"
HEADERS = {"User-Agent": "Mozilla/5.0"}


@register("carbonite")
class CarboniteScraper(Scraper):

    def discover(self, url: str, *, pages=1, days=None, known_urls=None, **kw) -> list[dict]:
        """Discover listing URLs from Carbonite forum pages."""
        urls = []
        known_urls = known_urls or set()
        params = "&prefix_id=1"
        if days:
            params += f"&last_days={days}"

        for page in range(1, pages + 1):
            page_url = url + params + (f"&page={page}" if page > 1 else "")
            r = requests.get(page_url, headers=HEADERS, timeout=15)
            matches = re.findall(r'href="(/index\.php\?threads/[^"]+)"', r.text)
            found_known = 0
            for href in matches:
                if "guide-for-safe" in href or "/latest" in href or "/post-" in href:
                    continue
                full_url = BASE + href
                if full_url in known_urls:
                    found_known += 1
                    continue
                if full_url not in urls:
                    urls.append(full_url)
            if found_known > 0:
                break
            time.sleep(1)

        return [{"url": u, "source": "carbonite"} for u in urls]

    def fetch(self, url: str) -> dict:
        """Fetch listing data from a Carbonite thread."""
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 404:
                return {"url": url, "source": "carbonite", "status": "deleted",
                        "checked_at": datetime.now(timezone.utc).isoformat()}

            soup = BeautifulSoup(r.text, "html.parser")
            title = soup.title.string.split("|")[0].strip() if soup.title else url
            status = "sold" if "(sold)" in title.lower() else "active"

            data = {"url": url, "title": title, "status": status, "source": "carbonite",
                    "fetched_at": datetime.now(timezone.utc).isoformat()}
            for dl in soup.select("dl[data-field]"):
                field = dl["data-field"]
                dd = dl.find("dd")
                if dd:
                    data[field] = dd.get_text(strip=True)

            return data if len(data) > 5 else {**data, "error": "No data block found"}
        except Exception as e:
            return {"url": url, "source": "carbonite", "error": str(e),
                    "status": "error", "checked_at": datetime.now(timezone.utc).isoformat()}
