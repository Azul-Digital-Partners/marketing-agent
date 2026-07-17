"""[your product] traffic check via Cloudflare Web Analytics.

Examples
--------
    # last 30 days, app.[your product]app.com (default site tag)
    python tools/[your product]_traffic_check.py

    # since the free-tier launch
    python tools/[your product]_traffic_check.py --since 2026-05-06

    # last 7 days, JSON output
    python tools/[your product]_traffic_check.py --days 7 --json

    # different site (when www.[your product]app.com gets its own beacon)
    python tools/[your product]_traffic_check.py --site-tag <tag> --label www.[your product]app.com

Requires CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in
data_sources/config/.env (see .env.example for setup).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data_sources.modules.cloudflare_web_analytics import (  # noqa: E402
    CloudflareWebAnalytics,
    CloudflareWebAnalyticsError,
)

DEFAULT_SITE_TAG = "your_cloudflare_site_tag_here"  # app.[your product]app.com platform


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Pull traffic for [your product] properties from Cloudflare Web Analytics."
    )
    range_group = p.add_mutually_exclusive_group()
    range_group.add_argument(
        "--days", type=int, default=30, help="Days back from today (default 30)."
    )
    range_group.add_argument(
        "--since", type=str, help="Start date YYYY-MM-DD (end is today)."
    )
    p.add_argument(
        "--site-tag",
        type=str,
        default=DEFAULT_SITE_TAG,
        help="Cloudflare Web Analytics site tag.",
    )
    p.add_argument(
        "--label",
        type=str,
        default="app.[your product]app.com",
        help="Friendly label for the site in human output.",
    )
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return p.parse_args()


def date_range(args: argparse.Namespace) -> tuple[str, str]:
    end = date.today()
    if args.since:
        start = date.fromisoformat(args.since)
    else:
        start = end - timedelta(days=args.days)
    return start.isoformat(), end.isoformat()


def render_human(
    label: str,
    start: str,
    end: str,
    summary: dict,
    daily: list[dict],
    top_pages: list[dict],
    referrers: list[dict],
    countries: list[dict],
) -> None:
    print(f"\n{label} traffic — {start} to {end}")
    print("=" * 60)
    print(f"  Pageviews: {summary['pageviews']:,}")
    print(f"  Visits:    {summary['visits']:,}")
    if summary["visits"]:
        print(f"  Pages/visit: {summary['pageviews'] / summary['visits']:.2f}")
    else:
        print("  Pages/visit: n/a (no visits in window)")

    if daily:
        print(f"\nDaily breakdown ({len(daily)} days with data):")
        peak = max((row["visits"] for row in daily), default=1) or 1
        for row in daily:
            bar_len = int(row["visits"] / peak * 30)
            bar = "█" * bar_len if bar_len else ""
            print(
                f"  {row['date']}  {row['visits']:>5,} v  "
                f"{row['pageviews']:>5,} pv  {bar}"
            )
    else:
        print("\nDaily breakdown: no data in window.")

    if top_pages:
        print("\nTop pages by pageviews:")
        for row in top_pages[:10]:
            print(
                f"  {row['pageviews']:>5,} pv  "
                f"{row['visits']:>5,} v  {row['path']}"
            )

    if referrers:
        print("\nTop referrers:")
        for row in referrers[:10]:
            print(f"  {row['visits']:>5,} v  {row['referrer']}")

    if countries:
        print("\nTop countries:")
        for row in countries[:5]:
            print(f"  {row['visits']:>5,} v  {row['country']}")
    print()


def main() -> int:
    args = parse_args()
    load_dotenv(ROOT / "data_sources" / "config" / ".env")
    load_dotenv(ROOT.parent / ".env")

    try:
        cf = CloudflareWebAnalytics(site_tag=args.site_tag)
    except CloudflareWebAnalyticsError as e:
        print(f"Setup error: {e}", file=sys.stderr)
        env_path = ROOT / "data_sources" / "config" / ".env"
        print(
            f"\nSet CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in:\n  {env_path}",
            file=sys.stderr,
        )
        print(f"(see {env_path}.example for the token-creation walkthrough)", file=sys.stderr)
        return 1

    start, end = date_range(args)

    try:
        summary = cf.summary(start, end)
        daily = cf.daily(start, end)
        top_pages = cf.top_pages(start, end, limit=20)
        referrers = cf.top_referrers(start, end, limit=20)
        countries = cf.top_countries(start, end, limit=10)
    except CloudflareWebAnalyticsError as e:
        print(f"Cloudflare API error: {e}", file=sys.stderr)
        return 2

    if args.json:
        print(
            json.dumps(
                {
                    "label": args.label,
                    "site_tag": args.site_tag,
                    "start": start,
                    "end": end,
                    "summary": summary,
                    "daily": daily,
                    "top_pages": top_pages,
                    "top_referrers": referrers,
                    "top_countries": countries,
                },
                indent=2,
            )
        )
    else:
        render_human(
            args.label, start, end, summary, daily, top_pages, referrers, countries
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
