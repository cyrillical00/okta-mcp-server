"""Okta tools: no silent sample data, no path tricks, token only to the org."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import _okta, applications, groups, policies, users  # noqa: E402

ORG = "https://acme.okta.com"
TOKEN = "not-a-real-token"


class _Response:
    def __init__(self, payload=None, status=200, link=None):
        self.status_code = status
        self._payload = payload if payload is not None else []
        self.headers = {"link": link} if link else {}

    def json(self):
        return self._payload

    def raise_for_status(self):
        if not 200 <= self.status_code < 300:
            raise RuntimeError(f"HTTP {self.status_code}")


class _FakeHttp:
    """Stands in for httpx.Client; answers GETs from (substring, response) pairs."""

    def __init__(self, routes=()):
        self.routes = list(routes)
        self.calls = []

    def __call__(self, *args, **kwargs):
        return self

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False

    def get(self, url, headers=None, params=None, timeout=None):
        self.calls.append({"url": url, "headers": headers or {}, "params": params or {}})
        for needle, response in self.routes:
            if needle in url:
                return response(url) if callable(response) else response
        return _Response([])

    @property
    def urls(self):
        return [call["url"] for call in self.calls]


def _env(**values):
    base = {k: v for k, v in os.environ.items() if k not in ("DEMO_MODE", "OKTA_API_TOKEN", "OKTA_ORG_URL")}
    base.update({k: v for k, v in values.items() if v is not None})
    return mock.patch.dict(os.environ, base, clear=True)


def _live(**overrides):
    values = {"OKTA_ORG_URL": ORG, "OKTA_API_TOKEN": TOKEN}
    values.update(overrides)
    return _env(**values)


def _next(url):
    return f'<{url}>; rel="next"'


class DemoModeTests(unittest.TestCase):
    def test_sample_data_is_served_only_when_demo_mode_is_on(self):
        with _env(DEMO_MODE="true"):
            self.assertTrue(_okta.is_demo())
        for value in (None, "false", "", "0", "yes"):
            with _env(DEMO_MODE=value):
                self.assertFalse(_okta.is_demo(), value)

    def test_a_missing_token_is_an_error_not_sample_data(self):
        http = _FakeHttp()
        with _env(OKTA_ORG_URL=ORG), mock.patch("httpx.Client", http):
            for call in (
                lambda: users.list_users(),
                lambda: users.get_user("00u1"),
                lambda: users.list_inactive_users(),
                lambda: users.list_users_without_mfa(),
                lambda: groups.list_groups(),
                lambda: groups.get_group_members("00g1"),
                lambda: groups.list_empty_groups(),
                lambda: applications.list_applications(),
                lambda: applications.get_app_assignments("0oa1"),
                lambda: applications.list_apps_with_no_assignments(),
                lambda: applications.list_apps_with_no_recent_logins(),
                lambda: policies.list_sign_on_policies(),
                lambda: policies.get_policy_rules("00p1"),
                lambda: policies.check_mfa_enrollment_rate(),
            ):
                with self.assertRaises(_okta.OktaConfigError):
                    call()
        self.assertEqual(http.calls, [])

    def test_demo_results_are_labelled_and_live_results_are_not(self):
        with _env(DEMO_MODE="true"):
            wrapped = json.loads(_okta.respond([{"id": "00u1"}]))
        self.assertIs(wrapped["demo"], True)
        self.assertIn("not from a real Okta org", wrapped["notice"])
        self.assertEqual(wrapped["data"], [{"id": "00u1"}])
        with _live():
            self.assertEqual(json.loads(_okta.respond([{"id": "00u1"}])), [{"id": "00u1"}])

    def test_every_server_tool_labels_its_demo_output(self):
        try:
            with _env(DEMO_MODE="true"):
                import server
        except ModuleNotFoundError as exc:  # the MCP SDK installed here has no FastMCP
            self.skipTest(f"server.py cannot be imported: {str(exc)[:60]}")
        calls = {
            "list_users": {}, "get_user": {"user_id_or_login": "nobody"}, "list_inactive_users": {},
            "list_users_without_mfa": {}, "list_groups": {}, "get_group_members": {"group_id": "none"},
            "list_empty_groups": {}, "list_applications": {}, "get_app_assignments": {"app_id": "none"},
            "list_apps_with_no_assignments": {}, "list_apps_with_no_recent_logins": {},
            "list_sign_on_policies": {}, "get_policy_rules": {"policy_id": "none"},
            "check_mfa_enrollment_rate": {},
        }
        with _env(DEMO_MODE="true"):
            for name, kwargs in calls.items():
                out = json.loads(getattr(server, name)(**kwargs))
                self.assertIs(out.get("demo"), True, name)
                self.assertIn("data", out, name)


class ConfigTests(unittest.TestCase):
    def test_org_url_must_be_plain_https(self):
        for good, expected in {
            "https://acme.okta.com": "https://acme.okta.com",
            "https://ACME.okta.com/": "https://acme.okta.com",
            " https://login.example.org ": "https://login.example.org",
        }.items():
            with _live(OKTA_ORG_URL=good):
                self.assertEqual(_okta.base_url(), expected)
        for bad in ("", "acme.okta.com", "http://acme.okta.com", "https://", "https://acme.okta.com/api/v1",
                    "https://user:pw@acme.okta.com", "https://acme.okta.com@evil.example",
                    "https://acme.okta.com?x=1", "ftp://acme.okta.com"):
            with _live(OKTA_ORG_URL=bad):
                with self.assertRaises(_okta.OktaConfigError, msg=bad):
                    _okta.base_url()


class PathTests(unittest.TestCase):
    def test_identifiers_are_encoded_as_one_segment(self):
        self.assertEqual(_okta.path_segment("00u1abc"), "00u1abc")
        self.assertEqual(_okta.path_segment("pat@example.org"), "pat%40example.org")
        self.assertEqual(_okta.path_segment("../../logs?x=1#"), "..%2F..%2Flogs%3Fx%3D1%23")
        self.assertEqual(_okta.path_segment("id/roles"), "id%2Froles")
        for bad in ("", None, ".", ".."):
            with self.assertRaises(ValueError, msg=repr(bad)):
                _okta.path_segment(bad)

    def test_a_crafted_argument_cannot_reach_another_endpoint(self):
        payload = "../../logs?since=2000-01-01&x="
        encoded = "..%2F..%2Flogs%3Fsince%3D2000-01-01%26x%3D"
        cases = [
            (lambda: users.get_user(payload), f"{ORG}/api/v1/users/{encoded}"),
            (lambda: groups.get_group_members(payload), f"{ORG}/api/v1/groups/{encoded}/users"),
            (lambda: applications.get_app_assignments(payload), f"{ORG}/api/v1/apps/{encoded}/users"),
            (lambda: policies.get_policy_rules(payload), f"{ORG}/api/v1/policies/{encoded}/rules"),
        ]
        for call, first_url in cases:
            http = _FakeHttp([
                ("/groups", _Response([])),
                ("/appLinks", _Response([])),
                ("/api/v1/users/", _Response({"id": "x", "profile": {}})),
            ])
            with _live(), mock.patch("httpx.Client", http):
                call()
            self.assertEqual(http.urls[0], first_url)
            self.assertTrue(all("/logs" not in url.split("%")[0] for url in http.urls), http.urls)

    def test_dot_segments_are_refused_without_a_request(self):
        http = _FakeHttp()
        with _live(), mock.patch("httpx.Client", http):
            for call in (lambda: users.get_user(".."), lambda: groups.get_group_members("."),
                         lambda: applications.get_app_assignments(".."), lambda: policies.get_policy_rules("")):
                with self.assertRaises(ValueError):
                    call()
        self.assertEqual(http.calls, [])


class StatusFilterTests(unittest.TestCase):
    def test_only_okta_statuses_reach_the_filter(self):
        http = _FakeHttp()
        with _live(), mock.patch("httpx.Client", http):
            users.list_users(status="active")
            applications.list_applications(status="Inactive")
        self.assertEqual(http.calls[0]["params"]["filter"], 'status eq "ACTIVE"')
        self.assertEqual(http.calls[1]["params"]["filter"], 'status eq "INACTIVE"')

    def test_a_filter_injection_is_refused_without_a_request(self):
        http = _FakeHttp()
        with _live(), mock.patch("httpx.Client", http):
            for bad in ('ACTIVE" or profile.login sw "a', "ACTIVE or 1 eq 1", "ANY", '"'):
                with self.assertRaises(ValueError, msg=bad):
                    users.list_users(status=bad)
                with self.assertRaises(ValueError, msg=bad):
                    applications.list_applications(status=bad)
            with self.assertRaises(ValueError):
                applications.list_applications(status="SUSPENDED")
        self.assertEqual(http.calls, [])

    def test_the_same_rule_applies_in_demo_mode(self):
        with _env(DEMO_MODE="true"):
            self.assertTrue(users.list_users(status="suspended") is not None)
            with self.assertRaises(ValueError):
                users.list_users(status='x" or "')


class PaginationTests(unittest.TestCase):
    def test_same_host_links_are_followed(self):
        def members(url):
            if "after=p2" in url:
                return _Response([{"id": "u2", "profile": {}}])
            return _Response([{"id": "u1", "profile": {}}], link=_next(f"{ORG}/api/v1/groups/00g1/users?after=p2&limit=200"))

        http = _FakeHttp([("/api/v1/groups/00g1/users", members)])
        with _live(), mock.patch("httpx.Client", http):
            result = groups.get_group_members("00g1")
        self.assertEqual([m["id"] for m in result], ["u1", "u2"])
        self.assertTrue(all(call["headers"]["Authorization"] == f"SSWS {TOKEN}" for call in http.calls))

    def test_a_link_to_another_host_is_never_followed(self):
        hostile = (
            "https://evil.example/api/v1/users?after=p2",
            "http://acme.okta.com/api/v1/users?after=p2",
            "https://acme.okta.com.evil.example/api/v1/users?after=p2",
            "https://acme.okta.com@evil.example/api/v1/users?after=p2",
            "https://acme.okta.com:8443/api/v1/users?after=p2",
        )
        paged = (
            lambda: users.list_inactive_users(),
            lambda: users.list_users_without_mfa(),
            lambda: groups.get_group_members("00g1"),
            lambda: groups.list_empty_groups(),
            lambda: applications.get_app_assignments("0oa1"),
            lambda: applications.list_apps_with_no_assignments(),
            lambda: applications.list_apps_with_no_recent_logins(),
            lambda: policies.check_mfa_enrollment_rate(),
        )
        for link in hostile:
            for call in paged:
                http = _FakeHttp([("/api/v1/", _Response([], link=_next(link)))])
                with _live(), mock.patch("httpx.Client", http):
                    with self.assertRaises(RuntimeError, msg=link):
                        call()
                self.assertEqual(len(http.calls), 1, link)
                self.assertTrue(http.urls[0].startswith(ORG + "/"), link)

    def test_last_page_has_no_next_link(self):
        with _live():
            self.assertIsNone(_okta.next_url(_Response([])))
            self.assertIsNone(_okta.next_url(_Response([], link=f'<{ORG}/api/v1/users>; rel="self"')))


if __name__ == "__main__":
    unittest.main()
