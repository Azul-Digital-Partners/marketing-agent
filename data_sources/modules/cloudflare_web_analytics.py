"""Cloudflare Web Analytics GraphQL client.

Queries the `rumPageloadEventsAdaptiveGroups` dataset via Cloudflare's GraphQL
Analytics API to return pageviews, visits, daily timeseries, top pages,
referrers, and countries for any site instrumented with the Web Analytics
beacon.

Auth: requires an API token with `Account > Account Analytics > Read` scope
plus the account ID that owns the site. Site tag is the value embedded in the
beacon snippet (`data-cf-beacon='{"token": "..."}'`).
"""

from __future__ import annotations

import os
from typing import Any

import requests

GRAPHQL_ENDPOINT = "https://api.cloudflare.com/client/v4/graphql"


class CloudflareWebAnalyticsError(RuntimeError):
    """Raised on auth, network, or GraphQL errors."""


class CloudflareWebAnalytics:
    def __init__(
        self,
        api_token: str | None = None,
        account_id: str | None = None,
        site_tag: str | None = None,
        timeout: int = 30,
    ) -> None:
        self.api_token = api_token or os.getenv("CLOUDFLARE_API_TOKEN")
        self.account_id = account_id or os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.site_tag = site_tag or os.getenv("CLOUDFLARE_SITE_TAG")
        self.timeout = timeout

        missing = [
            name
            for name, val in [
                ("CLOUDFLARE_API_TOKEN", self.api_token),
                ("CLOUDFLARE_ACCOUNT_ID", self.account_id),
                ("site_tag (CLOUDFLARE_SITE_TAG or constructor arg)", self.site_tag),
            ]
            if not val
        ]
        if missing:
            raise CloudflareWebAnalyticsError(
                f"Missing required config: {', '.join(missing)}"
            )

    def _query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        resp = requests.post(
            GRAPHQL_ENDPOINT,
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json",
            },
            json={"query": query, "variables": variables},
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise CloudflareWebAnalyticsError(
                f"HTTP {resp.status_code}: {resp.text[:500]}"
            )
        body = resp.json()
        if body.get("errors"):
            raise CloudflareWebAnalyticsError(f"GraphQL errors: {body['errors']}")
        return body["data"]

    def _series(self, query: str, variables: dict[str, Any]) -> list[dict[str, Any]]:
        data = self._query(query, variables)
        accounts = data.get("viewer", {}).get("accounts", [])
        if not accounts:
            return []
        return accounts[0].get("series", []) or []

    def _vars(self, start: str, end: str, **extra: Any) -> dict[str, Any]:
        return {
            "accountTag": self.account_id,
            "siteTag": self.site_tag,
            "start": start,
            "end": end,
            **extra,
        }

    def summary(self, start: str, end: str) -> dict[str, int]:
        """Return total pageviews and visits in [start, end] (YYYY-MM-DD inclusive)."""
        query = """
        query Summary($accountTag: String!, $siteTag: String!, $start: String!, $end: String!) {
          viewer {
            accounts(filter: {accountTag: $accountTag}) {
              series: rumPageloadEventsAdaptiveGroups(
                limit: 1
                filter: {siteTag: $siteTag, date_geq: $start, date_leq: $end}
              ) {
                count
                sum { visits }
              }
            }
          }
        }
        """
        rows = self._series(query, self._vars(start, end))
        if not rows:
            return {"pageviews": 0, "visits": 0}
        return {
            "pageviews": int(rows[0]["count"]),
            "visits": int(rows[0]["sum"]["visits"]),
        }

    def daily(self, start: str, end: str) -> list[dict[str, Any]]:
        """Pageviews + visits per day, ascending."""
        query = """
        query Daily($accountTag: String!, $siteTag: String!, $start: String!, $end: String!) {
          viewer {
            accounts(filter: {accountTag: $accountTag}) {
              series: rumPageloadEventsAdaptiveGroups(
                limit: 1000
                filter: {siteTag: $siteTag, date_geq: $start, date_leq: $end}
                orderBy: [date_ASC]
              ) {
                dimensions { date }
                count
                sum { visits }
              }
            }
          }
        }
        """
        rows = self._series(query, self._vars(start, end))
        return [
            {
                "date": row["dimensions"]["date"],
                "pageviews": int(row["count"]),
                "visits": int(row["sum"]["visits"]),
            }
            for row in rows
        ]

    def top_pages(
        self, start: str, end: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        query = """
        query TopPages($accountTag: String!, $siteTag: String!, $start: String!, $end: String!, $limit: Int!) {
          viewer {
            accounts(filter: {accountTag: $accountTag}) {
              series: rumPageloadEventsAdaptiveGroups(
                limit: $limit
                filter: {siteTag: $siteTag, date_geq: $start, date_leq: $end}
                orderBy: [count_DESC]
              ) {
                dimensions { requestPath }
                count
                sum { visits }
              }
            }
          }
        }
        """
        rows = self._series(query, self._vars(start, end, limit=limit))
        return [
            {
                "path": row["dimensions"]["requestPath"] or "(unknown)",
                "pageviews": int(row["count"]),
                "visits": int(row["sum"]["visits"]),
            }
            for row in rows
        ]

    def top_referrers(
        self, start: str, end: str, limit: int = 20
    ) -> list[dict[str, Any]]:
        query = """
        query TopReferrers($accountTag: String!, $siteTag: String!, $start: String!, $end: String!, $limit: Int!) {
          viewer {
            accounts(filter: {accountTag: $accountTag}) {
              series: rumPageloadEventsAdaptiveGroups(
                limit: $limit
                filter: {siteTag: $siteTag, date_geq: $start, date_leq: $end}
                orderBy: [count_DESC]
              ) {
                dimensions { refererHost }
                count
                sum { visits }
              }
            }
          }
        }
        """
        rows = self._series(query, self._vars(start, end, limit=limit))
        return [
            {
                "referrer": row["dimensions"]["refererHost"] or "(direct)",
                "pageviews": int(row["count"]),
                "visits": int(row["sum"]["visits"]),
            }
            for row in rows
        ]

    def top_countries(
        self, start: str, end: str, limit: int = 10
    ) -> list[dict[str, Any]]:
        query = """
        query TopCountries($accountTag: String!, $siteTag: String!, $start: String!, $end: String!, $limit: Int!) {
          viewer {
            accounts(filter: {accountTag: $accountTag}) {
              series: rumPageloadEventsAdaptiveGroups(
                limit: $limit
                filter: {siteTag: $siteTag, date_geq: $start, date_leq: $end}
                orderBy: [count_DESC]
              ) {
                dimensions { countryName }
                count
                sum { visits }
              }
            }
          }
        }
        """
        rows = self._series(query, self._vars(start, end, limit=limit))
        return [
            {
                "country": row["dimensions"]["countryName"] or "(unknown)",
                "pageviews": int(row["count"]),
                "visits": int(row["sum"]["visits"]),
            }
            for row in rows
        ]
