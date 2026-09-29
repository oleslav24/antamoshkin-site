"""Submit explicitly supplied production URLs to IndexNow.

This script is intentionally separate from the static build. It never submits
localhost or preview URLs and only sends canonical oleslav.com addresses.
"""

from __future__ import annotations

import argparse
import json
from urllib.parse import urlparse
from urllib.request import Request, urlopen


HOST = "oleslav.com"
KEY = "4f8b0c59e8194679b2af098c4d7e3a91"
ENDPOINT = "https://api.indexnow.org/indexnow"


def is_canonical_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.netloc == HOST and not parsed.query and not parsed.fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit changed canonical production URLs to IndexNow.")
    parser.add_argument("urls", nargs="+", help="Canonical https://oleslav.com URLs")
    args = parser.parse_args()
    invalid = [url for url in args.urls if not is_canonical_url(url)]
    if invalid:
        raise SystemExit("Only canonical https://oleslav.com URLs without query strings are allowed: " + ", ".join(invalid))
    payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": args.urls}).encode()
    request = Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=30) as response:
        print(f"INDEXNOW_STATUS={response.status}")


if __name__ == "__main__":
    main()
