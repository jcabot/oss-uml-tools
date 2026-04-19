"""
take_snapshot.py – Fetch the current list of UML tools from GitHub and save
them as a dated snapshot CSV in the snapshots/ folder.

Usage:
    python take_snapshot.py

The output file is named snapshot-YYYY-MM-DD.csv using today's date and is
written to the snapshots/ directory. The CSV format matches the existing
snapshot files (same columns, same ordering).
"""

import os
import sys
import requests
from datetime import datetime, timedelta
import snapshot_utils

GITHUB_API_URL = "https://api.github.com/search/repositories"

EXCLUDED_REPOS = {
    "awesome-low-level-design",
    "Books-Free-Books",
    "awesome-diagramming",
    "plantuml-examples",
    "hogwarts-artifacts-online",
    "-Enterprise-Architect-16-Crack-renewal-",
    "UoM-Applied-Informatics",
    "UML-Best-Practices",
    "design-pattern-examples-in-python",
    "design-pattern-examples-in-crystal",
    "FreeTakServer",
    "plantuml-icon-font-sprites",
    "snow-owl",
    "StarUML-CrackedAndTranslate",
    "tiro-notes",
    "QuickUMLS",
}


def fetch_repos(query="uml", sort="stars", order="desc", per_page=100, max_pages=10):
    cutoff = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
    full_query = f"{query} stars:>=50 pushed:>={cutoff}"
    all_repos = []

    for page in range(1, max_pages + 1):
        params = {
            "q": full_query,
            "sort": sort,
            "order": order,
            "per_page": per_page,
            "page": page,
        }
        try:
            response = requests.get(GITHUB_API_URL, params=params, timeout=15)
            response.raise_for_status()
            items = response.json().get("items", [])
            if not items:
                break
            all_repos.extend(items)
            print(f"  page {page}: +{len(items)} repos (total {len(all_repos)})")
        except requests.exceptions.RequestException as e:
            print(f"  ERROR on page {page}: {e}", file=sys.stderr)
            break

    return all_repos


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = os.path.join(snapshot_utils.SNAPSHOTS_DIR, f"snapshot-{today}.csv")

    if os.path.exists(output_path):
        print(f"Snapshot for today already exists: {output_path}")
        print("Delete it first if you want to regenerate.")
        sys.exit(0)

    print("Fetching repos from GitHub API...")
    repos = fetch_repos()
    print(f"Fetched {len(repos)} repos total")

    filtered = [r for r in repos if r["name"] not in EXCLUDED_REPOS]
    count = snapshot_utils.repos_to_csv(filtered, output_path)
    print(f"After exclusions: {count} repos")
    print(f"Snapshot saved: {output_path}")


if __name__ == "__main__":
    main()
