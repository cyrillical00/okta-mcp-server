# okta-mcp-server

An MCP server that exposes Okta user, group, application, and policy data to Claude via the Model Context Protocol.

> **All tools are read-only. This server does not create, update, or delete any Okta resources.**

Built by [Oleg Strutsovski](https://linkedin.com/in/olegst) — IT Operations Manager

---

## What you can ask Claude

Once connected, ask Claude things like:

- "Find all users who have not logged in for 90 days"
- "What is our MFA enrollment rate?"
- "List all active apps with no user or group assignments"
- "Which apps have had no logins in the last 60 days?"
- "Show me all groups with no members"
- "Get full details for the user alice.chen@apexlabs.io"
- "List all users without MFA enrolled — I need this for our SOC2 evidence"
- "What authentication policies are configured and how many rules does each have?"

---

## Tool Reference

| Tool | Description | Key Parameters |
|---|---|---|
| `list_users` | List users in the Okta org | `limit` (1-100), `status` (ACTIVE/STAGED/DEPROVISIONED/SUSPENDED), `search` |
| `get_user` | Full user details including groups and app assignments | `user_id_or_login` |
| `list_inactive_users` | Users who have not logged in for N days | `days_inactive` (default 90) |
| `list_users_without_mfa` | Active users with no MFA factors enrolled | none |
| `list_groups` | List groups with member counts | `limit`, `search` |
| `get_group_members` | All members of a specific group | `group_id` |
| `list_empty_groups` | Groups with zero members | none |
| `list_applications` | List integrated applications | `limit`, `status` (ACTIVE/INACTIVE) |
| `get_app_assignments` | Users and groups assigned to an app | `app_id` |
| `list_apps_with_no_assignments` | Active apps with no user or group assignments | none |
| `list_apps_with_no_recent_logins` | Apps with no Okta authentications in N days | `days` (default 90) |
| `list_sign_on_policies` | Authentication policies with rule counts | none |
| `get_policy_rules` | Rules for a specific policy | `policy_id` |
| `check_mfa_enrollment_rate` | Org-wide MFA enrollment percentage | none |

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```
OKTA_ORG_URL=https://your-org.okta.com
OKTA_API_TOKEN=your-api-token-here
DEMO_MODE=false
```

To generate an Okta API token: Okta Admin Console > Security > API > Tokens > Create Token.
A read-only admin role is sufficient.

### 3. Configure Claude Desktop

Open your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

#### Live mode (real Okta org)

```json
{
  "mcpServers": {
    "okta": {
      "command": "python",
      "args": ["/path/to/okta-mcp-server/server.py"],
      "env": {
        "OKTA_ORG_URL": "https://your-org.okta.com",
        "OKTA_API_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

#### Demo mode (no credentials required)

```json
{
  "mcpServers": {
    "okta": {
      "command": "python",
      "args": ["/path/to/okta-mcp-server/server.py"],
      "env": {
        "DEMO_MODE": "true"
      }
    }
  }
}
```

Replace `/path/to/okta-mcp-server/server.py` with the absolute path on your machine.

Restart Claude Desktop after saving the config. The `okta` server will appear in Claude's tool panel.

---

## Demo Mode

Demo mode runs without any Okta credentials and returns realistic fixture data for a fictional org called **Apex Labs** (300 users, 45 applications, 60 groups).

Demo mode activates automatically when:
- `DEMO_MODE=true` is set, **or**
- `OKTA_API_TOKEN` is absent

Demo fixtures include:
- 15+ users with lastLogin older than 90 days
- 10 users with no MFA factors enrolled
- 5+ apps with no authentication in 90+ days
- 5 groups with zero members
- 3 active apps with no user or group assignments
- MFA enrollment rate: approximately 91% (273 of 300 active users enrolled)

All fixture field names match real Okta API response shapes.

---

## Security Notes

- The API token is read via environment variable and never logged or returned in tool output.
- `.env` is excluded from version control via `.gitignore`.
- Only read-only Okta API endpoints are called (`GET` requests only).
- The token is sent only to `OKTA_ORG_URL`, which must be an `https://` address. Redirects are not followed, and a pagination link that points anywhere else stops the call with an error.
- IDs and logins passed to a tool are URL-encoded before they are placed in a request path, and a status filter accepts only Okta's own status values, so a crafted argument cannot steer a call to a different endpoint.
- No Okta data is cached to disk.
