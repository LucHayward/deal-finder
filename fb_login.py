#!/usr/bin/env python3
"""Launch Camoufox browser for manual FB login, then save cookies."""
import json
from camoufox.sync_api import Camoufox

COOKIE_FILE = "fb_cookies.json"

with Camoufox(headless=False) as browser:
    ctx = browser.new_context()
    page = ctx.new_page()
    page.goto("https://www.facebook.com/")
    print("Log into Facebook manually, then press Enter here...")
    input()
    cookies = ctx.cookies()
    with open(COOKIE_FILE, "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"Saved {len(cookies)} cookies to {COOKIE_FILE}")
