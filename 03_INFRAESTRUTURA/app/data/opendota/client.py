"""Lightweight OpenDota client with XML serialization utilities.

The functions here intentionally avoid hard dependencies so they can be
executed inside Colab/Juniper runtimes with minimal setup.
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, Iterable, List, Optional

import requests


class OpenDotaClient:
    """Simple wrapper around the OpenDota REST API.

    Parameters
    ----------
    api_key:
        Premium API key. If omitted, the client will try to read
        ``OPENDOTA_API_KEY`` from the environment.
    base_url:
        API root. Defaults to the public OpenDota endpoint.
    timeout:
        Request timeout (in seconds).
    max_retries:
        How many times to retry when the API rate limits or responds
        with transient failures.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.opendota.com/api",
        timeout: int = 20,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key or os.getenv("OPENDOTA_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries

    def _request(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = params.copy() if params else {}
        if self.api_key:
            params.setdefault("api_key", self.api_key)

        for attempt in range(1, self.max_retries + 1):
            response = requests.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                return response.json()

            if response.status_code in {401, 403}:
                raise RuntimeError(
                    "OpenDota rejected the request. Check if the premium API key is valid."
                )

            if response.status_code == 429 or 500 <= response.status_code < 600:
                sleep_time = 2 ** (attempt - 1)
                time.sleep(sleep_time)
                continue

            response.raise_for_status()

        raise RuntimeError(
            f"OpenDota request failed after {self.max_retries} attempts: {url}"
        )

    # ---------------------- PUBLIC ENDPOINTS ----------------------
    def get_league_matches(self, league_id: int, limit: int = 2000) -> List[Dict[str, Any]]:
        """Return matches from a given league/tournament."""

        params = {"limit": limit}
        return self._request(f"leagues/{league_id}/matches", params=params)

    def get_match(self, match_id: int) -> Dict[str, Any]:
        """Return full match payload with performance breakdown."""

        return self._request(f"matches/{match_id}")

    def get_player(self, account_id: int) -> Dict[str, Any]:
        """Return profile and performance summary for a player."""

        return self._request(f"players/{account_id}")

    def get_player_matches(
        self, account_id: int, limit: int = 500, is_pro: bool = True
    ) -> List[Dict[str, Any]]:
        """Return the last matches for a player (optionally pro only)."""

        params = {
            "limit": min(limit, 500),
            "significant": 0,
        }
        if is_pro:
            params["is_pro"] = "true"
        return self._request(f"players/{account_id}/matches", params=params)

    def get_heroes(self) -> List[Dict[str, Any]]:
        """Return hero reference data."""

        return self._request("heroes")

    def get_items(self) -> List[Dict[str, Any]]:
        """Return item reference data."""

        return self._request("constants/items")


# ---------------------- XML HELPERS ----------------------
def _iter_items(data: Dict[str, Any]) -> Iterable[tuple[str, Any]]:
    for key, value in data.items():
        yield key, value


def dict_to_xml(tag: str, data: Any) -> str:
    """Convert a mapping/list/primitive to XML.

    The output is intentionally minimal to keep files small while
    remaining human-readable for debugging inside Colab.
    """

    from xml.etree.ElementTree import Element, SubElement, tostring  # Local import

    def build(node: Element, value: Any) -> None:
        if value is None:
            return
        if isinstance(value, (str, int, float, bool)):
            node.text = str(value)
            return
        if isinstance(value, list):
            for item in value:
                child = SubElement(node, "item")
                build(child, item)
            return
        if isinstance(value, dict):
            for child_key, child_value in _iter_items(value):
                child = SubElement(node, child_key)
                build(child, child_value)
            return
        node.text = str(value)

    root = Element(tag)
    build(root, data)
    return tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")


def save_xml(path: str, tag: str, data: Any) -> None:
    """Persist a dictionary/list as an XML document."""

    os.makedirs(os.path.dirname(path), exist_ok=True)
    xml_content = dict_to_xml(tag, data)
    with open(path, "w", encoding="utf-8") as xml_file:
        xml_file.write(xml_content)

