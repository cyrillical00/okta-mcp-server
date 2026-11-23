"""
Shared configuration and request helpers for the Okta tools.

Two rules live here so every tool follows them:

* identifiers supplied by the caller are encoded before they go into a URL;
* the API token is only ever sent to the configured org over HTTPS, including
  when following pagination links.
"""

import os
from urllib.parse import quote, urlsplit

# Okta user and application statuses accepted in a status filter.
USER_STATUSES = frozenset({
    "STAGED", "PROVISIONED", "ACTIVE", "RECOVERY", "LOCKED_OUT",
    "PASSWORD_EXPIRED", "SUSPENDED", "DEPROVISIONED",
})
APP_STATUSES = frozenset({"ACTIVE", "INACTIVE"})

class OktaConfigError(RuntimeError):
    """The server is not configured to talk to an Okta org."""


def is_demo() -> bool:
    return os.getenv("DEMO_MODE", "false").lower() == "true" or not os.getenv("OKTA_API_TOKEN")


def okta_headers() -> dict:
    return {
        "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def base_url() -> str:
    """The org's base URL, as https://host with nothing else attached."""
    raw = os.getenv("OKTA_ORG_URL", "").strip().rstrip("/")
    parts = urlsplit(raw)
    if (
        parts.scheme != "https"
        or not parts.hostname
        or "@" in parts.netloc
        or parts.path
        or parts.query
        or parts.fragment
    ):
        raise OktaConfigError("OKTA_ORG_URL must be the org's HTTPS address, for example https://your-org.okta.com")
    return f"https://{parts.netloc.lower()}"


def path_segment(value) -> str:
    """Encode a caller-supplied identifier as exactly one URL path segment.

    Without this, a value such as "../../logs?x=" or "id/roles" would reach a
    different endpoint than the tool was written to call.
    """
    text = str(value) if value is not None else ""
    if not text or text in (".", ".."):
        raise ValueError(f"Not a valid Okta identifier: {text!r}")
    return quote(text, safe="")


def validate_status(status, allowed) -> str:
    """Upper-cased status if it is one Okta defines, else ValueError."""
    value = str(status).strip().upper()
    if value not in allowed:
        raise ValueError(f"status must be one of: {', '.join(sorted(allowed))}")
    return value


def next_url(resp):
    """URL of the next page from the Link header, or None on the last page.

    The request carries the API token, so the link is followed only when it
    points at the configured org over HTTPS. Anything else is an error rather
    than a silently shortened result.
    """
    org = urlsplit(base_url())
    for part in resp.headers.get("link", "").split(","):
        if 'rel="next"' not in part:
            continue
        candidate = part.split(";")[0].strip().strip("<>")
        target = urlsplit(candidate)
        if target.scheme == "https" and target.netloc.lower() == org.netloc:
            return candidate
        raise RuntimeError("Okta returned a next-page link to another host; not following it.")
    return None
