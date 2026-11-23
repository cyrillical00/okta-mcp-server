"""
Application-related Okta MCP tools.
All operations are read-only.
"""

from datetime import datetime, timezone, timedelta
from typing import Any

import httpx


from tools._okta import (
    APP_STATUSES,
    base_url as _base_url,
    is_demo as _is_demo,
    next_url as _next_url,
    okta_headers as _okta_headers,
    path_segment as _seg,
    validate_status as _validate_status,
)


def _format_app(a: dict, assigned_user_count: int | None = None) -> dict:
    result = {
        "id": a.get("id"),
        "name": a.get("name"),
        "label": a.get("label"),
        "status": a.get("status"),
        "lastUpdated": a.get("lastUpdated"),
        "signOnMode": a.get("signOnMode"),
    }
    if assigned_user_count is not None:
        result["assignedUserCount"] = assigned_user_count
    return result


def list_applications(limit: int = 50, status: str | None = None) -> list[dict]:
    """List applications in the Okta org with optional status filter."""
    limit = max(1, min(limit, 200))
    if status:
        # The value goes into an Okta filter expression; only real statuses are accepted.
        status = _validate_status(status, APP_STATUSES)

    if _is_demo():
        from demo.fixtures import APPLICATIONS, APP_ASSIGNMENTS
        results = list(APPLICATIONS)
        if status:
            results = [a for a in results if a.get("status", "").upper() == status.upper()]
        output = []
        for a in results[:limit]:
            assignments = APP_ASSIGNMENTS.get(a["id"], {})
            user_count = len(assignments.get("users", [])) + len(assignments.get("groups", []))
            output.append(_format_app(a, assigned_user_count=user_count))
        return output

    params: dict[str, Any] = {"limit": limit}
    if status:
        params["filter"] = f'status eq "{status}"'
    with httpx.Client() as client:
        resp = client.get(f"{_base_url()}/api/v1/apps", headers=_okta_headers(), params=params, timeout=30)
        resp.raise_for_status()
        return [_format_app(a) for a in resp.json()]


def get_app_assignments(app_id: str) -> dict:
    """Get users and groups assigned to an application."""
    if _is_demo():
        from demo.fixtures import APP_ASSIGNMENTS
        assignments = APP_ASSIGNMENTS.get(app_id, {"users": [], "groups": []})
        return {
            "users": [
                {
                    "id": u["id"],
                    "login": u["profile"]["login"],
                    "firstName": u["profile"]["firstName"],
                    "lastName": u["profile"]["lastName"],
                    "status": u["status"],
                }
                for u in assignments.get("users", [])
            ],
            "groups": [
                {
                    "id": g["id"],
                    "name": g["profile"]["name"],
                    "type": g["type"],
                }
                for g in assignments.get("groups", [])
            ],
        }

    users = []
    url = f"{_base_url()}/api/v1/apps/{_seg(app_id)}/users"
    params: dict[str, Any] = {"limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            for u in resp.json():
                p = u.get("profile", {})
                users.append({
                    "id": u.get("id"),
                    "login": p.get("login"),
                    "firstName": p.get("firstName"),
                    "lastName": p.get("lastName"),
                    "status": u.get("status"),
                })
            url = _next_url(resp)
            params = {}

        groups_resp = client.get(
            f"{_base_url()}/api/v1/apps/{_seg(app_id)}/groups",
            headers=_okta_headers(), params={"limit": 200}, timeout=30,
        )
        groups_resp.raise_for_status()
        groups = [
            {"id": g.get("id"), "priority": g.get("priority")}
            for g in groups_resp.json()
        ]

    return {"users": users, "groups": groups}


def list_apps_with_no_assignments() -> list[dict]:
    """Find active applications with no user or group assignments. Likely zombie integrations."""
    if _is_demo():
        from demo.fixtures import APPLICATIONS, APP_ASSIGNMENTS, NO_ASSIGNMENT_APP_IDS
        results = []
        for a in APPLICATIONS:
            if a.get("status") != "ACTIVE":
                continue
            if a["id"] in NO_ASSIGNMENT_APP_IDS:
                results.append(_format_app(a, assigned_user_count=0))
        return results

    # Live: fetch active apps and check assignments
    all_apps = []
    url = f"{_base_url()}/api/v1/apps"
    params: dict[str, Any] = {"filter": 'status eq "ACTIVE"', "limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            all_apps.extend(resp.json())
            url = _next_url(resp)
            params = {}

    no_assignments = []
    with httpx.Client() as client:
        for a in all_apps:
            users_resp = client.get(
                f"{_base_url()}/api/v1/apps/{_seg(a['id'])}/users",
                headers=_okta_headers(), params={"limit": 1}, timeout=30,
            )
            users_resp.raise_for_status()
            groups_resp = client.get(
                f"{_base_url()}/api/v1/apps/{_seg(a['id'])}/groups",
                headers=_okta_headers(), params={"limit": 1}, timeout=30,
            )
            groups_resp.raise_for_status()
            if len(users_resp.json()) == 0 and len(groups_resp.json()) == 0:
                no_assignments.append(_format_app(a, assigned_user_count=0))
    return no_assignments


def list_apps_with_no_recent_logins(days: int = 90) -> list[dict]:
    """Find apps where no user has authenticated via Okta in the specified window."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    cutoff_str = cutoff.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    if _is_demo():
        from demo.fixtures import APPLICATIONS, NO_RECENT_LOGIN_APP_IDS
        results = []
        for a in APPLICATIONS:
            if a.get("status") != "ACTIVE":
                continue
            last_login = a.get("lastLoginAt")
            if last_login is None:
                continue
            last_login_dt = datetime.fromisoformat(last_login.replace("Z", "+00:00"))
            if last_login_dt < cutoff:
                row = _format_app(a)
                row["lastLoginAt"] = last_login
                row["daysSinceLastLogin"] = (datetime.now(timezone.utc) - last_login_dt).days
                results.append(row)
        results.sort(key=lambda x: x.get("lastLoginAt") or "")
        return results

    # Live: Okta does not expose lastLoginAt directly on app object.
    # Use System Log to find apps with no recent auth events.
    # Filter for app SSO events since the cutoff and collect active app IDs.
    apps_with_recent_logins: set[str] = set()
    url = f"{_base_url()}/api/v1/logs"
    params: dict[str, Any] = {
        "filter": 'eventType eq "app.auth.sso"',
        "since": cutoff_str,
        "limit": 1000,
    }
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=60)
            resp.raise_for_status()
            for event in resp.json():
                target = event.get("target", [])
                for t in target:
                    if t.get("type") == "AppInstance":
                        apps_with_recent_logins.add(t.get("id", ""))
            url = _next_url(resp)
            params = {}

        # Get all active apps and return those not in the recent login set
        all_apps = []
        url = f"{_base_url()}/api/v1/apps"
        params = {"filter": 'status eq "ACTIVE"', "limit": 200}
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            all_apps.extend(resp.json())
            url = _next_url(resp)
            params = {}

    return [_format_app(a) for a in all_apps if a["id"] not in apps_with_recent_logins]
