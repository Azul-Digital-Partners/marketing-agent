"""
Plausible Analytics Integration

Fetches traffic, referral, and engagement data from Plausible-tracked sites
via the Plausible Stats API v1.

Plausible is already installed on [yourdomain.com] (site script
pa-G3TH7KACfrP3_TpkZnSbl.js). This module is the canonical Marketing read
path for that site until/unless GA4 provisioning lands.

Auth: Bearer token from Plausible Settings -> API Keys. Stored as
PLAUSIBLE_API_KEY in Marketing/data_sources/config/.env.

Stats API reference: https://plausible.io/docs/stats-api
"""

import os
from typing import Dict, List, Optional, Any

import requests


PLAUSIBLE_BASE_URL = "https://plausible.io/api/v1"


class PlausibleAnalytics:
    """Plausible Stats API v1 reader."""

    def __init__(
        self,
        site_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = PLAUSIBLE_BASE_URL,
    ):
        """
        Initialize Plausible reader.

        Args:
            site_id: Plausible site identifier (the bare domain, e.g.
                "[yourdomain.com]"). Defaults to PLAUSIBLE_SITE_ID env var.
            api_key: Plausible API key. Defaults to PLAUSIBLE_API_KEY env var.
            base_url: API base URL (override only for self-hosted instances).
        """
        self.site_id = site_id or os.getenv("PLAUSIBLE_SITE_ID")
        api_key = api_key or os.getenv("PLAUSIBLE_API_KEY")

        if not self.site_id:
            raise ValueError(
                "PLAUSIBLE_SITE_ID must be provided or set in environment"
            )
        if not api_key:
            raise ValueError(
                "PLAUSIBLE_API_KEY must be provided or set in environment"
            )

        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _get(self, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        params = {"site_id": self.site_id, **params}
        resp = self._session.get(f"{self.base_url}{path}", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()

    # ---------- aggregate -----------------------------------------------

    def get_aggregate(
        self,
        period: str = "30d",
        metrics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Top-line totals for the period.

        Args:
            period: "day" | "7d" | "30d" | "month" | "6mo" | "12mo" | "custom"
            metrics: subset of ["visitors","visits","pageviews","views_per_visit",
                "bounce_rate","visit_duration","events"]. Defaults to the core set.

        Returns:
            Dict with each metric -> {"value": number}
        """
        metrics = metrics or [
            "visitors",
            "visits",
            "pageviews",
            "bounce_rate",
            "visit_duration",
        ]
        data = self._get(
            "/stats/aggregate",
            {"period": period, "metrics": ",".join(metrics)},
        )
        return data.get("results", {})

    # ---------- timeseries ----------------------------------------------

    def get_timeseries(
        self,
        period: str = "30d",
        interval: str = "date",
        metrics: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Per-bucket time series for the period.

        Args:
            period: same vocabulary as get_aggregate.
            interval: "date" (daily) or "month".
            metrics: defaults to ["visitors","pageviews","visits"].
        """
        metrics = metrics or ["visitors", "pageviews", "visits"]
        data = self._get(
            "/stats/timeseries",
            {
                "period": period,
                "interval": interval,
                "metrics": ",".join(metrics),
            },
        )
        return data.get("results", [])

    # ---------- breakdown -----------------------------------------------

    def get_breakdown(
        self,
        property_: str,
        period: str = "30d",
        metrics: Optional[List[str]] = None,
        limit: int = 25,
        page: int = 1,
    ) -> List[Dict[str, Any]]:
        """
        Group results by a Plausible dimension (a "property").

        Common properties:
          - "event:page"             top pages
          - "visit:source"           referral source (e.g. "Direct", "google")
          - "visit:referrer"         full referrer URL
          - "visit:utm_source" / "visit:utm_medium" / "visit:utm_campaign"
          - "visit:country" / "visit:device" / "visit:browser"
          - "visit:entry_page" / "visit:exit_page"

        Args:
            property_: the Plausible property to group by.
            period: same vocabulary as get_aggregate.
            metrics: defaults to ["visitors","pageviews","bounce_rate"].
            limit: max rows.
            page: 1-indexed pagination.
        """
        metrics = metrics or ["visitors", "pageviews", "bounce_rate"]
        data = self._get(
            "/stats/breakdown",
            {
                "period": period,
                "property": property_,
                "metrics": ",".join(metrics),
                "limit": limit,
                "page": page,
            },
        )
        return data.get("results", [])

    # ---------- convenience helpers -------------------------------------

    def get_top_pages(self, period: str = "30d", limit: int = 20) -> List[Dict[str, Any]]:
        """Top pages by visitors for the period."""
        return self.get_breakdown(
            "event:page",
            period=period,
            metrics=["visitors", "pageviews", "bounce_rate"],
            limit=limit,
        )

    def get_traffic_sources(self, period: str = "30d", limit: int = 25) -> List[Dict[str, Any]]:
        """Referral sources (Direct, Google, social, etc.) by visitors."""
        return self.get_breakdown(
            "visit:source",
            period=period,
            metrics=["visitors", "visits", "bounce_rate"],
            limit=limit,
        )

    def get_referrers(self, period: str = "30d", limit: int = 25) -> List[Dict[str, Any]]:
        """Full referrer URLs by visitors."""
        return self.get_breakdown(
            "visit:referrer",
            period=period,
            metrics=["visitors", "visits"],
            limit=limit,
        )

    def get_utm_campaigns(self, period: str = "30d", limit: int = 25) -> List[Dict[str, Any]]:
        """UTM campaign attribution rollup."""
        return self.get_breakdown(
            "visit:utm_campaign",
            period=period,
            metrics=["visitors", "visits", "bounce_rate"],
            limit=limit,
        )

    def get_realtime_visitors(self) -> int:
        """Number of visitors on the site in the last 5 minutes."""
        resp = self._session.get(
            f"{self.base_url}/stats/realtime/visitors",
            params={"site_id": self.site_id},
            timeout=15,
        )
        resp.raise_for_status()
        # Endpoint returns a bare integer body.
        try:
            return int(resp.json())
        except ValueError:
            return int(resp.text.strip())


# Example usage / smoke test
if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv("data_sources/config/.env")

    plausible = PlausibleAnalytics()
    print(f"Site: {plausible.site_id}\n")

    print("Realtime visitors (last 5 min):", plausible.get_realtime_visitors())

    print("\n30-day aggregate:")
    for metric, payload in plausible.get_aggregate(period="30d").items():
        print(f"  {metric}: {payload.get('value')}")

    print("\nTop 5 traffic sources (30d):")
    for row in plausible.get_traffic_sources(period="30d", limit=5):
        print(f"  {row.get('source','?'):<20} {row.get('visitors',0)} visitors")

    print("\nTop 5 pages (30d):")
    for row in plausible.get_top_pages(period="30d", limit=5):
        print(f"  {row.get('page','?'):<40} {row.get('visitors',0)} visitors")
