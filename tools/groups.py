"""
Group-related Okta MCP tools.
All operations are read-only.
"""

from typing import Any

import httpx


from tools._okta import (
    base_url as _base_url,
    is_demo as _is_demo,
    next_url as _next_url,
    okta_headers as _okta_headers,
    path_segment as _seg,
)


def _format_group(g: dict, member_count: int | None = None) -> dict:
    p = g.get("profile", {})
    result = {
        "id": g.get("id"),
        "name": p.get("name"),
        "description": p.get("description"),
        "type": g.get("type"),
        "lastUpdated": g.get("lastUpdated"),
        "lastMembershipUpdated": g.get("lastMembershipUpdated"),
    }
    if member_count is not None:
        result["memberCount"] = member_count
    return result


def list_groups(limit: int = 50, search: str | None = None) -> list[dict]:
    """List groups in the Okta org with optional search."""
    limit = max(1, min(limit, 200))

    if _is_demo():
        from demo.fixtures import GROUPS, GROUP_MEMBERS
        results = list(GROUPS)
        if search:
            s = search.lower()
            results = [
                g for g in results
                if s in g["profile"].get("name", "").lower()
                or s in g["profile"].get("description", "").lower()
            ]
        output = []
        for g in results[:limit]:
            count = len(GROUP_MEMBERS.get(g["id"], []))
            output.append(_format_group(g, member_count=count))
        return output

    params: dict[str, Any] = {"limit": limit}
    if search:
        params["q"] = search
    with httpx.Client() as client:
        resp = client.get(f"{_base_url()}/api/v1/groups", headers=_okta_headers(), params=params, timeout=30)
        resp.raise_for_status()
        return [_format_group(g) for g in resp.json()]


def get_group_members(group_id: str) -> list[dict]:
    """Get all members of a group."""
    if _is_demo():
        from demo.fixtures import GROUP_MEMBERS
        members = GROUP_MEMBERS.get(group_id, [])
        return [
            {
                "id": u["id"],
                "login": u["profile"]["login"],
                "firstName": u["profile"]["firstName"],
                "lastName": u["profile"]["lastName"],
                "status": u["status"],
            }
            for u in members
        ]

    results = []
    url = f"{_base_url()}/api/v1/groups/{_seg(group_id)}/users"
    params: dict[str, Any] = {"limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            for u in resp.json():
                p = u.get("profile", {})
                results.append({
                    "id": u.get("id"),
                    "login": p.get("login"),
                    "firstName": p.get("firstName"),
                    "lastName": p.get("lastName"),
                    "status": u.get("status"),
                })
            url = _next_url(resp)
            params = {}
    return results


def list_empty_groups() -> list[dict]:
    """Find groups with no members. Common hygiene issue in mature Okta tenants."""
    if _is_demo():
        from demo.fixtures import GROUPS, GROUP_MEMBERS, EMPTY_GROUP_IDS
        results = []
        for g in GROUPS:
            if g["id"] in EMPTY_GROUP_IDS or len(GROUP_MEMBERS.get(g["id"], [])) == 0:
                results.append(_format_group(g, member_count=0))
        return results

    # Live: fetch all groups and filter those with zero members
    all_groups = []
    url = f"{_base_url()}/api/v1/groups"
    params: dict[str, Any] = {"limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            all_groups.extend(resp.json())
            url = _next_url(resp)
            params = {}

    empty = []
    with httpx.Client() as client:
        for g in all_groups:
            members_resp = client.get(
                f"{_base_url()}/api/v1/groups/{_seg(g['id'])}/users",
                headers=_okta_headers(),
                params={"limit": 1},
                timeout=30,
            )
            members_resp.raise_for_status()
            if len(members_resp.json()) == 0:
                empty.append(_format_group(g, member_count=0))
    return empty
