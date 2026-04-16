"""
Okta MCP Server
Exposes Okta user, group, application, and policy data to Claude via the Model Context Protocol.
All tools are read-only. This server does not create, update, or delete any Okta resources.
"""

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load .env from the same directory as this file
load_dotenv(Path(__file__).parent / ".env")

mcp = FastMCP(
    "okta",
    instructions=(
        "This server provides read-only access to Okta identity data for the connected org. "
        "Use it to audit users, groups, applications, and authentication policies. "
        "All tools are read-only and will not modify any Okta resources."
    ),
)

# ─── Users ────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_users(
    limit: int = 25,
    status: str | None = None,
    search: str | None = None,
) -> str:
    """
    List users in the Okta org with optional status filter and search.

    Args:
        limit: Number of users to return (1-100, default 25).
        status: Filter by status. One of: ACTIVE, STAGED, DEPROVISIONED, SUSPENDED.
        search: Search string matched against login, firstName, lastName, email.
    """
    from tools.users import list_users as _list_users
    result = _list_users(limit=limit, status=status, search=search)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_user(user_id_or_login: str) -> str:
    """
    Get full details for a specific user including group memberships and app assignments.

    Args:
        user_id_or_login: Okta user ID (e.g. 00u1abc...) or login email address.
    """
    from tools.users import get_user as _get_user
    result = _get_user(user_id_or_login)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_inactive_users(days_inactive: int = 90) -> str:
    """
    Find users who have not logged in for N days. Useful for access review and license audits.

    Args:
        days_inactive: Threshold in days (default 90). Users whose lastLogin is older than
                       this number of days are returned, sorted ascending by lastLogin.
    """
    from tools.users import list_inactive_users as _list_inactive_users
    result = _list_inactive_users(days_inactive=days_inactive)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_users_without_mfa() -> str:
    """
    List users with no MFA factors enrolled.
    Key input for SOC2 CC6.1 and HIPAA access control evidence.
    Only returns ACTIVE users.
    """
    from tools.users import list_users_without_mfa as _list_users_without_mfa
    result = _list_users_without_mfa()
    return json.dumps(result, indent=2)


# ─── Groups ───────────────────────────────────────────────────────────────────

@mcp.tool()
def list_groups(limit: int = 50, search: str | None = None) -> str:
    """
    List groups in the Okta org with member counts.

    Args:
        limit: Number of groups to return (default 50).
        search: Search string matched against group name and description.
    """
    from tools.groups import list_groups as _list_groups
    result = _list_groups(limit=limit, search=search)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_group_members(group_id: str) -> str:
    """
    Get all members of a group.

    Args:
        group_id: Okta group ID (e.g. 00g1abc...).
    """
    from tools.groups import get_group_members as _get_group_members
    result = _get_group_members(group_id)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_empty_groups() -> str:
    """
    Find groups with no members.
    Common hygiene issue in mature Okta tenants.
    """
    from tools.groups import list_empty_groups as _list_empty_groups
    result = _list_empty_groups()
    return json.dumps(result, indent=2)


# ─── Applications ─────────────────────────────────────────────────────────────

@mcp.tool()
def list_applications(limit: int = 50, status: str | None = None) -> str:
    """
    List applications integrated with the Okta org.

    Args:
        limit: Number of applications to return (default 50).
        status: Filter by status. One of: ACTIVE, INACTIVE.
    """
    from tools.applications import list_applications as _list_applications
    result = _list_applications(limit=limit, status=status)
    return json.dumps(result, indent=2)


@mcp.tool()
def get_app_assignments(app_id: str) -> str:
    """
    Get users and groups assigned to an application.

    Args:
        app_id: Okta application ID (e.g. 0oa1abc...).
    """
    from tools.applications import get_app_assignments as _get_app_assignments
    result = _get_app_assignments(app_id)
    return json.dumps(result, indent=2)


@mcp.tool()
def list_apps_with_no_assignments() -> str:
    """
    Find active applications with no user or group assignments.
    These are likely zombie integrations that can be cleaned up.
    """
    from tools.applications import list_apps_with_no_assignments as _list_apps_with_no_assignments
    result = _list_apps_with_no_assignments()
    return json.dumps(result, indent=2)


@mcp.tool()
def list_apps_with_no_recent_logins(days: int = 90) -> str:
    """
    Find apps where no user has authenticated via Okta in the specified window.

    Args:
        days: Lookback window in days (default 90).
    """
    from tools.applications import list_apps_with_no_recent_logins as _list_apps_with_no_recent_logins
    result = _list_apps_with_no_recent_logins(days=days)
    return json.dumps(result, indent=2)


# ─── Policies ─────────────────────────────────────────────────────────────────

@mcp.tool()
def list_sign_on_policies() -> str:
    """
    List Okta sign-on authentication policies with rule counts.
    Includes policy name, priority, status, and number of rules configured.
    """
    from tools.policies import list_sign_on_policies as _list_sign_on_policies
    result = _list_sign_on_policies()
    return json.dumps(result, indent=2)


@mcp.tool()
def get_policy_rules(policy_id: str) -> str:
    """
    Get rules for a sign-on policy with conditions, actions, and priority order.

    Args:
        policy_id: Okta policy ID (e.g. 00p1abc...).
    """
    from tools.policies import get_policy_rules as _get_policy_rules
    result = _get_policy_rules(policy_id)
    return json.dumps(result, indent=2)


@mcp.tool()
def check_mfa_enrollment_rate() -> str:
    """
    Calculate org-wide MFA enrollment rate.
    Returns total active users, count with MFA enrolled, count without, and enrollment percentage.
    Key metric for SOC2 CC6.1 and HIPAA technical safeguards evidence.
    """
    from tools.policies import check_mfa_enrollment_rate as _check_mfa_enrollment_rate
    result = _check_mfa_enrollment_rate()
    return json.dumps(result, indent=2)


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
