"""
Policy-related Okta MCP tools.
All operations are read-only.
"""

import os
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


def list_sign_on_policies() -> list[dict]:
    """List Okta sign-on authentication policies with rule counts."""
    if _is_demo():
        from demo.fixtures import SIGN_ON_POLICIES, POLICY_RULES
        results = []
        for p in SIGN_ON_POLICIES:
            results.append({
                "id": p["id"],
                "name": p["name"],
                "description": p.get("description", ""),
                "priority": p.get("priority"),
                "status": p.get("status"),
                "system": p.get("system", False),
                "created": p.get("created"),
                "lastUpdated": p.get("lastUpdated"),
                "ruleCount": len(POLICY_RULES.get(p["id"], [])),
            })
        return results

    with httpx.Client() as client:
        resp = client.get(
            f"{_base_url()}/api/v1/policies",
            headers=_okta_headers(),
            params={"type": "OKTA_SIGN_ON"},
            timeout=30,
        )
        resp.raise_for_status()
        policies = resp.json()
        results = []
        for p in policies:
            rules_resp = client.get(
                f"{_base_url()}/api/v1/policies/{p['id']}/rules",
                headers=_okta_headers(), timeout=30,
            )
            rules_resp.raise_for_status()
            results.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "description": p.get("description", ""),
                "priority": p.get("priority"),
                "status": p.get("status"),
                "system": p.get("system", False),
                "created": p.get("created"),
                "lastUpdated": p.get("lastUpdated"),
                "ruleCount": len(rules_resp.json()),
            })
        return results


def get_policy_rules(policy_id: str) -> list[dict]:
    """Get rules for a sign-on policy with conditions, actions, and priority order."""
    if _is_demo():
        from demo.fixtures import POLICY_RULES
        rules = POLICY_RULES.get(policy_id, [])
        if not rules and policy_id not in POLICY_RULES:
            return [{"error": f"Policy not found: {policy_id}"}]
        return [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "priority": r.get("priority"),
                "status": r.get("status"),
                "conditions": r.get("conditions"),
                "actions": r.get("actions"),
            }
            for r in sorted(rules, key=lambda x: x.get("priority", 99))
        ]

    with httpx.Client() as client:
        resp = client.get(
            f"{_base_url()}/api/v1/policies/{policy_id}/rules",
            headers=_okta_headers(), timeout=30,
        )
        resp.raise_for_status()
        return [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "priority": r.get("priority"),
                "status": r.get("status"),
                "conditions": r.get("conditions"),
                "actions": r.get("actions"),
            }
            for r in sorted(resp.json(), key=lambda x: x.get("priority", 99))
        ]


def check_mfa_enrollment_rate() -> dict:
    """Calculate org-wide MFA enrollment rate. Key metric for SOC2 CC6.1 and HIPAA technical safeguards."""
    if _is_demo():
        from demo.fixtures import get_mfa_enrolled_count
        total, enrolled = get_mfa_enrolled_count()
        not_enrolled = total - enrolled
        rate = round((enrolled / total) * 100, 1) if total > 0 else 0.0
        return {
            "totalActiveUsers": total,
            "usersWithMfaEnrolled": enrolled,
            "usersWithoutMfa": not_enrolled,
            "enrollmentPercentage": rate,
            "summary": f"{enrolled} of {total} active users have MFA enrolled ({rate}%)",
        }

    # Live: page through active users and check factors
    total = 0
    enrolled_count = 0
    url = f"{_base_url()}/api/v1/users"
    params: dict[str, Any] = {"filter": 'status eq "ACTIVE"', "limit": 200}
    with httpx.Client() as client:
        while url:
            resp = client.get(url, headers=_okta_headers(), params=params, timeout=30)
            resp.raise_for_status()
            for u in resp.json():
                total += 1
                factors_resp = client.get(
                    f"{_base_url()}/api/v1/users/{u['id']}/factors",
                    headers=_okta_headers(), timeout=30,
                )
                factors_resp.raise_for_status()
                active_factors = [f for f in factors_resp.json() if f.get("status") == "ACTIVE"]
                if active_factors:
                    enrolled_count += 1
            link_header = resp.headers.get("link", "")
            next_url = None
            for part in link_header.split(","):
                if 'rel="next"' in part:
                    next_url = part.split(";")[0].strip().strip("<>")
            url = next_url
            params = {}

    not_enrolled = total - enrolled_count
    rate = round((enrolled_count / total) * 100, 1) if total > 0 else 0.0
    return {
        "totalActiveUsers": total,
        "usersWithMfaEnrolled": enrolled_count,
        "usersWithoutMfa": not_enrolled,
        "enrollmentPercentage": rate,
        "summary": f"{enrolled_count} of {total} active users have MFA enrolled ({rate}%)",
    }
