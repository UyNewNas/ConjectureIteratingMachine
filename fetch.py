#!/usr/bin/env python3
"""Snapshot Wikipedia's unsolved mathematics categories via MediaWiki API."""

import csv
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict, deque
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
API = "https://en.wikipedia.org/w/api.php"
SEED = "Category:Unsolved problems in mathematics"
USER_AGENT = "LeanAgent-conjecture-archive/1.0 (research snapshot; MediaWiki API)"
SKIP_SUBCATEGORIES = {"Category:Conjectures"}  # Includes solved conjectures.
NUMBER_THEORY_CATEGORIES = {"Category:Unsolved problems in number theory"}
NUMBER_THEORY_EXTRA_TITLES = {"Generalized Riemann hypothesis", "Grand Riemann hypothesis"}


def api(**params):
    query = {"format": "json", "formatversion": "2", **params}
    url = API + "?" + urllib.parse.urlencode(query)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(request, timeout=40) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code != 429 or attempt == 7:
                raise
            delay = min(120, max(30, int(error.headers.get("Retry-After", "30"))))
            print(f"HTTP 429; waiting {delay}s", flush=True)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            if attempt == 7:
                raise
            time.sleep(min(30, 2 ** attempt))


def category_members(category):
    continuation = {}
    while True:
        result = api(action="query", list="categorymembers", cmtitle=category,
                     cmlimit="max", **continuation)
        yield from result["query"]["categorymembers"]
        continuation = result.get("continue")
        if not continuation:
            break


def batches(items, size):
    for start in range(0, len(items), size):
        yield items[start:start + size]


def filename(pageid):
    return f"{pageid}.wiki"


def write_number_theory_index():
    with (ROOT / "index.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [row for row in reader if row["title"] in NUMBER_THEORY_EXTRA_TITLES or
                NUMBER_THEORY_CATEGORIES.intersection(row["categories"].split("; "))]
        fieldnames = reader.fieldnames
    with (ROOT / "number_theory_index.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"number theory: {len(rows)} pages", flush=True)


def main():
    if sys.argv[1:] == ["--index-only"]:
        write_number_theory_index()
        return
    resume = sys.argv[1:] == ["--resume"]
    categories = defaultdict(set)
    seen_categories = set()
    queue = deque([SEED])
    pages = {}
    while queue:
        category = queue.popleft()
        if category in seen_categories or category in SKIP_SUBCATEGORIES:
            continue
        seen_categories.add(category)
        for member in category_members(category):
            if member["ns"] == 14:
                if member["title"] not in seen_categories:
                    queue.append(member["title"])
            elif member["ns"] == 0:
                pages[member["pageid"]] = member["title"]
                categories[member["pageid"]].add(category)
        print(f"{category}: {len(pages)} pages total", flush=True)

    raw_dir = ROOT / "pages"
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for pageids in batches(sorted(pages), 50):
        result = api(action="query", prop="revisions", pageids="|".join(map(str, pageids)),
                     rvprop="ids|timestamp")
        for page in result["query"]["pages"]:
            if "missing" in page or not page.get("revisions"):
                continue
            revision = page["revisions"][0]
            rows.append({
                "pageid": page["pageid"],
                "title": page["title"],
                "url": "https://en.wikipedia.org/wiki/" + urllib.parse.quote(page["title"].replace(" ", "_")),
                "revision_id": revision["revid"],
                "revision_timestamp": revision["timestamp"],
                "categories": sorted(categories[page["pageid"]]),
                "file": "pages/" + filename(page["pageid"]),
            })
        time.sleep(1)

    missing_ids = [row["pageid"] for row in rows if not resume or
                   not (raw_dir / filename(row["pageid"])).exists()]
    for pageids in batches(missing_ids, 10):
        result = api(action="query", prop="revisions", pageids="|".join(map(str, pageids)),
                     rvprop="content", rvslots="main")
        for page in result["query"]["pages"]:
            if "missing" not in page and page.get("revisions"):
                content = page["revisions"][0]["slots"]["main"].get("content", "")
                (raw_dir / filename(page["pageid"])).write_text(content, encoding="utf-8")
        print(f"saved {len(list(raw_dir.glob('*.wiki')))}/{len(rows)} pages", flush=True)
        time.sleep(1)

    rows.sort(key=lambda row: row["title"].casefold())
    with (ROOT / "index.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["pageid", "title", "url", "revision_id",
                                                     "revision_timestamp", "categories", "file"])
        writer.writeheader()
        for row in rows:
            writer.writerow({**row, "categories": "; ".join(row["categories"])})
    (ROOT / "manifest.json").write_text(json.dumps({
        "source": API,
        "seed_category": SEED,
        "excluded_subcategories": sorted(SKIP_SUBCATEGORIES),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "category_count": len(seen_categories),
        "page_count": len(rows),
        "categories": sorted(seen_categories),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_number_theory_index()
    print(f"complete: {len(rows)} pages across {len(seen_categories)} categories")


if __name__ == "__main__":
    main()
