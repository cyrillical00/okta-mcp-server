"""
User-related Okta MCP tools.
All operations are read-only.
"""

import os
from datetime import datetime, timezone, timedelta
from typing import Any

import httpx


def _is_demo() -> bool:
    return os.getenv("DEMO_MODE", "false").lower() == "true" or not os.getenv("OKTA_API_TOKEN")


def _okta_headers() -> dict:
    return {
        "Authorization": f"SSWS {os.getenv('OKTA_API_TOKEN')}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _base_url() -> str:
    return os.getenv("OKTA_ORG_URL", "").rstrip("/")


def _format_user(u: dict) -> dict:
    p = u.get("profile", {})
    return {
        "id": u.get("id"),
        "login": p.get("login"),
        "firstName": p.get("firstName"),
        "lastName": p.get("lastName"),
        "status": u.get("status"),
        "lastLogin": u.get("lastLogin"),
        "created": u.get("created"),
        "passwordChanged": u.get("passwordChanged"),
    }


def list_users(limit: int = 25, status: str | None = None, search: str | None = None) -> list[dict]:
    """List users in the Okta org with optional status filter and search."""
    limit = max(1, min(limit, 100))

    if _is_demo():
        from demo.fixtures import USERS
        results = list(USERS)
        if status:
            results = [u for u in results if u.get("status", "").upper() == status.upper()]
        if search:
            s = search.lower()
            results = [
                u for u in results
                if s in u["profile"].get("login", "").lower()
                or s in u["profile"].get("firstName", "").lower()
                or s in u["profile"].get("lastName", "").lower()
                or s in u["profile"].get("email", "").lower()
            ]
        return [_format_user(u) for u in results[:limit]]

    params: dict[str, Any] = {"limit": limit}
    if status:
        params["filter"] = f'status eq "{status.upper()}"'
    if search:
        params["search"] = search
    with httpx.Client() as client:
        resp = client.get(f"{_base_url()}/api/v1/users", headers=_okta_headers(), params=params, timeout=30)
        resp.raise_for_status()
        return [_format_user(u) for u in resp.json()]


def get_user(user_id_or_login: str) -> dict:
    """Get full details for a specific user including group memberships and app assignments."""
    if _is_demo():
        from demo.fixtures import get_user_by_id, get_user_groups, get_user_apps
        u = get_user_by_id(user_id_or_login)
        if not u:
            return {"error": f"User not found: {user_id_or_login}"}
        groups = [
            {"id": g["id"], "name": g["profile"]["name"], "type": g["type"]}
            for g in get_user_groups(u["id"])
        ]
        apps = [
            {"id": a["id"], "name": a["name"], "label": a["label"], "status": a["status"]}
            for a in get_user_apps(u["id"])
        ]
        return {**_format_user(u), "profile": u.get("profile", {}), "groups": groups, "applications": apps}

    with httpx.Client() as client:
        resp = client.get(
            f"{_base_url()}/api/v1/users/{user_id_or_login}",
            headers=_okta_headers(), timeout=30,
        )
        resp.raise_for_status()
        user_data = resp.json()

        groups_resp = client.get(
            f"{_base_url()}/api/v1/users/{user_id_or_login}/groups",
            headers=_okta_headers(), timeout=30,
        )
        groups_resp.raise_for_status()
        groups = [
            {"id": g["id"], "name": g["profile"]["name"], "type": g["type"]}
            for g in groups_resp.json()
        ]

        apps_resp = client.get(
            f"{_base_url()}/api/v1/users/{user_id_or_login}/appLinks",
            headers=_okta_headers(), timeout=30,
        )
        apps_resp.raise_for_status()
        apps = [
            {"id": a.get("appInstanceId"), "name": a.get("appName"), "label": a.get("label")}
            for a in apps_resp.json()
        ]

    return {**_format_user(user_data), "profile": user_data.get("profile", {}), "groups": groups, "applications": apps}


def list_inactive_users(days_inactive: int = 90) -> list[dict]:
    """Find users who have not logged in for N days. Useful for access review and license audits."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_inactive)

    if _is_demo():
        from demo.fixtures import USERS
        results = []
        for u in USERS:
            if u.get("status") != "ACTIVE":
                continue
            last_login_str = u.get("lastLogin")
            if not last_login_str:
                continue
            last_login = datetime.fromisoformat(last_login_str.replace("Z", "+00:00"))
            if last_login < cutoff:
                row = _format_user(u)
                row["daysSinceLogin"] = (datetime.now(timezone.utc) - last_login).days
                results.append(row)
        results.sort(key=lambda x: x["lastLogin"] or "")
        return results

    # Live: use Okta search filter
    filter_str = f'status eq "ACTIVE" and lastLogin lt "{cutoff.strftime("%Y-%m-%dT%H:%M:%S.000Z")}"'
    results = []
    url = f"{_base_url()}/api/v1/users"
    params = {"filter": filter_str, "limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            for u in resp.json():
                last_login_str = u.get("lastLogin")
                row = _format_user(u)
                if last_login_str:
                    last_login = datetime.fromisoformat(last_login_str.replace("Z", "+00:00"))
                    row["daysSinceLogin"] = (datetime.now(timezone.utc) - last_login).days
                results.append(row)
            link_header = resp.headers.get("link", "")
            next_url = None
            for part in link_header.split(","):
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip().strip("<>")
            url = next_url
            params = {}
    results.sort(key=lambda x: x.get("lastLogin") or "")
    return results


def list_users_without_mfa() -> list[dict]:
    """List users with no MFA factors enrolled. Key input for SOC2 CC6.1 and HIPAA access control evidence."""
    if _is_demo():
        from demo.fixtures import USERS, MFA_FACTORS, USERS_WITHOUT_MFA
        results = []
        for u in USERS:
            if u.get("status") != "ACTIVE":
                continue
            if u["id"] not in MFA_FACTORS:
                results.append(_format_user(u))
        return results

    # Live: page through active users and check each user's factors
    results = []
    url = f"{_base_url()}/api/v1/users"
    params = {"filter": 'status eq "ACTIVE"', "limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            for u in resp.json():
                factors_resp = client.get(
                    f"{_base_url()}/api/v1/users/{u['id']}/factors",
                    headers=_okta_headers(), timeout=30,
                )
                factors_resp.raise_for_status()
                active_factors = [f for f in factors_resp.json() if f.get("status") == "ACTIVE"]
                if not active_factors:
                    results.append(_format_user(u))
            link_header = resp.headers.get("link", "")
            next_url = None
            for part in link_header.split(","):
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip().strip("<>")
            url = next_url
            params = {}
    return results
