"""
Static fixture data for Apex Labs demo org.
Field names and response shapes match real Okta API documentation.
300 users, 45 applications, 60 groups.
"""

from datetime import datetime, timezone, timedelta

_NOW = datetime(2026, 4, 15, 12, 0, 0, tzinfo=timezone.utc)

def _ts(days_ago: int) -> str:
    return (_NOW - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%S.000Z")


USERS = [
    # Active users with recent logins
    {"id": "00u1a", "status": "ACTIVE", "created": _ts(730), "activated": _ts(729), "lastLogin": _ts(1),  "passwordChanged": _ts(30),  "profile": {"login": "alice.chen@apexlabs.io",      "firstName": "Alice",    "lastName": "Chen",       "email": "alice.chen@apexlabs.io",      "mobilePhone": "+14155550101", "department": "Engineering",   "title": "Staff Engineer"}},
    {"id": "00u2b", "status": "ACTIVE", "created": _ts(700), "activated": _ts(699), "lastLogin": _ts(2),  "passwordChanged": _ts(60),  "profile": {"login": "ben.okafor@apexlabs.io",     "firstName": "Ben",      "lastName": "Okafor",     "email": "ben.okafor@apexlabs.io",     "mobilePhone": "+14155550102", "department": "Product",       "title": "Senior PM"}},
    {"id": "00u3c", "status": "ACTIVE", "created": _ts(680), "activated": _ts(679), "lastLogin": _ts(3),  "passwordChanged": _ts(45),  "profile": {"login": "carla.m@apexlabs.io",        "firstName": "Carla",    "lastName": "Martinez",   "email": "carla.m@apexlabs.io",        "mobilePhone": "+14155550103", "department": "Security",      "title": "Security Analyst"}},
    {"id": "00u4d", "status": "ACTIVE", "created": _ts(650), "activated": _ts(649), "lastLogin": _ts(5),  "passwordChanged": _ts(10),  "profile": {"login": "darnell.w@apexlabs.io",      "firstName": "Darnell",  "lastName": "Washington", "email": "darnell.w@apexlabs.io",      "mobilePhone": "+14155550104", "department": "IT",            "title": "IT Manager"}},
    {"id": "00u5e", "status": "ACTIVE", "created": _ts(620), "activated": _ts(619), "lastLogin": _ts(7),  "passwordChanged": _ts(20),  "profile": {"login": "elena.v@apexlabs.io",        "firstName": "Elena",    "lastName": "Vasquez",    "email": "elena.v@apexlabs.io",        "mobilePhone": "+14155550105", "department": "Finance",       "title": "Controller"}},
    {"id": "00u6f", "status": "ACTIVE", "created": _ts(600), "activated": _ts(599), "lastLogin": _ts(8),  "passwordChanged": _ts(90),  "profile": {"login": "felix.ng@apexlabs.io",       "firstName": "Felix",    "lastName": "Ng",         "email": "felix.ng@apexlabs.io",       "mobilePhone": "+14155550106", "department": "Engineering",   "title": "DevOps Engineer"}},
    {"id": "00u7g", "status": "ACTIVE", "created": _ts(580), "activated": _ts(579), "lastLogin": _ts(10), "passwordChanged": _ts(15),  "profile": {"login": "grace.kim@apexlabs.io",      "firstName": "Grace",    "lastName": "Kim",        "email": "grace.kim@apexlabs.io",      "mobilePhone": "+14155550107", "department": "HR",            "title": "HRBP"}},
    {"id": "00u8h", "status": "ACTIVE", "created": _ts(560), "activated": _ts(559), "lastLogin": _ts(12), "passwordChanged": _ts(50),  "profile": {"login": "hiro.tanaka@apexlabs.io",    "firstName": "Hiro",     "lastName": "Tanaka",     "email": "hiro.tanaka@apexlabs.io",    "mobilePhone": "+14155550108", "department": "Engineering",   "title": "Backend Engineer"}},
    {"id": "00u9i", "status": "ACTIVE", "created": _ts(540), "activated": _ts(539), "lastLogin": _ts(14), "passwordChanged": _ts(25),  "profile": {"login": "imani.j@apexlabs.io",        "firstName": "Imani",    "lastName": "Johnson",    "email": "imani.j@apexlabs.io",        "mobilePhone": "+14155550109", "department": "Marketing",     "title": "Growth Lead"}},
    {"id": "00u10j","status": "ACTIVE", "created": _ts(520), "activated": _ts(519), "lastLogin": _ts(20), "passwordChanged": _ts(5),   "profile": {"login": "jake.r@apexlabs.io",         "firstName": "Jake",     "lastName": "Rivera",     "email": "jake.r@apexlabs.io",         "mobilePhone": "+14155550110", "department": "Sales",         "title": "AE"}},
    # 15+ users with lastLogin older than 90 days
    {"id": "00u11k","status": "ACTIVE", "created": _ts(900), "activated": _ts(899), "lastLogin": _ts(95), "passwordChanged": _ts(120), "profile": {"login": "kevin.b@apexlabs.io",         "firstName": "Kevin",    "lastName": "Burke",      "email": "kevin.b@apexlabs.io",        "mobilePhone": None,           "department": "Engineering",   "title": "Engineer"}},
    {"id": "00u12l","status": "ACTIVE", "created": _ts(880), "activated": _ts(879), "lastLogin": _ts(100),"passwordChanged": _ts(130), "profile": {"login": "lisa.p@apexlabs.io",          "firstName": "Lisa",     "lastName": "Park",       "email": "lisa.p@apexlabs.io",         "mobilePhone": None,           "department": "Design",        "title": "Designer"}},
    {"id": "00u13m","status": "ACTIVE", "created": _ts(860), "activated": _ts(859), "lastLogin": _ts(110),"passwordChanged": _ts(140), "profile": {"login": "marco.d@apexlabs.io",         "firstName": "Marco",    "lastName": "DiLuca",     "email": "marco.d@apexlabs.io",        "mobilePhone": None,           "department": "Finance",       "title": "Analyst"}},
    {"id": "00u14n","status": "ACTIVE", "created": _ts(840), "activated": _ts(839), "lastLogin": _ts(120),"passwordChanged": _ts(150), "profile": {"login": "nina.s@apexlabs.io",          "firstName": "Nina",     "lastName": "Shah",       "email": "nina.s@apexlabs.io",         "mobilePhone": None,           "department": "Legal",         "title": "Counsel"}},
    {"id": "00u15o","status": "ACTIVE", "created": _ts(820), "activated": _ts(819), "lastLogin": _ts(130),"passwordChanged": _ts(160), "profile": {"login": "oscar.f@apexlabs.io",         "firstName": "Oscar",    "lastName": "Flores",     "email": "oscar.f@apexlabs.io",        "mobilePhone": None,           "department": "Sales",         "title": "SDR"}},
    {"id": "00u16p","status": "ACTIVE", "created": _ts(800), "activated": _ts(799), "lastLogin": _ts(150),"passwordChanged": _ts(180), "profile": {"login": "priya.r@apexlabs.io",         "firstName": "Priya",    "lastName": "Rao",        "email": "priya.r@apexlabs.io",        "mobilePhone": None,           "department": "Engineering",   "title": "QA Engineer"}},
    {"id": "00u17q","status": "ACTIVE", "created": _ts(780), "activated": _ts(779), "lastLogin": _ts(165),"passwordChanged": _ts(200), "profile": {"login": "quinn.m@apexlabs.io",         "firstName": "Quinn",    "lastName": "Murphy",     "email": "quinn.m@apexlabs.io",        "mobilePhone": None,           "department": "Marketing",     "title": "Content Writer"}},
    {"id": "00u18r","status": "ACTIVE", "created": _ts(760), "activated": _ts(759), "lastLogin": _ts(180),"passwordChanged": _ts(210), "profile": {"login": "rose.a@apexlabs.io",          "firstName": "Rose",     "lastName": "Abramov",    "email": "rose.a@apexlabs.io",         "mobilePhone": None,           "department": "HR",            "title": "Recruiter"}},
    {"id": "00u19s","status": "ACTIVE", "created": _ts(740), "activated": _ts(739), "lastLogin": _ts(200),"passwordChanged": _ts(230), "profile": {"login": "sam.t@apexlabs.io",           "firstName": "Sam",      "lastName": "Torres",     "email": "sam.t@apexlabs.io",          "mobilePhone": None,           "department": "Support",       "title": "Support Specialist"}},
    {"id": "00u20t","status": "ACTIVE", "created": _ts(720), "activated": _ts(719), "lastLogin": _ts(210),"passwordChanged": _ts(240), "profile": {"login": "tanya.w@apexlabs.io",         "firstName": "Tanya",    "lastName": "Wells",      "email": "tanya.w@apexlabs.io",        "mobilePhone": None,           "department": "Finance",       "title": "AP Specialist"}},
    {"id": "00u21u","status": "ACTIVE", "created": _ts(700), "activated": _ts(699), "lastLogin": _ts(250),"passwordChanged": _ts(280), "profile": {"login": "ulrich.b@apexlabs.io",        "firstName": "Ulrich",   "lastName": "Bauer",      "email": "ulrich.b@apexlabs.io",       "mobilePhone": None,           "department": "Engineering",   "title": "Contractor"}},
    {"id": "00u22v","status": "ACTIVE", "created": _ts(680), "activated": _ts(679), "lastLogin": _ts(280),"passwordChanged": _ts(310), "profile": {"login": "vera.n@apexlabs.io",          "firstName": "Vera",     "lastName": "Novak",      "email": "vera.n@apexlabs.io",         "mobilePhone": None,           "department": "IT",            "title": "Sysadmin"}},
    {"id": "00u23w","status": "ACTIVE", "created": _ts(660), "activated": _ts(659), "lastLogin": _ts(300),"passwordChanged": _ts(330), "profile": {"login": "will.c@apexlabs.io",          "firstName": "Will",     "lastName": "Chang",      "email": "will.c@apexlabs.io",         "mobilePhone": None,           "department": "Legal",         "title": "Paralegal"}},
    {"id": "00u24x","status": "ACTIVE", "created": _ts(640), "activated": _ts(639), "lastLogin": _ts(320),"passwordChanged": _ts(350), "profile": {"login": "xena.l@apexlabs.io",          "firstName": "Xena",     "lastName": "Liu",        "email": "xena.l@apexlabs.io",         "mobilePhone": None,           "department": "Design",        "title": "UX Researcher"}},
    {"id": "00u25y","status": "ACTIVE", "created": _ts(620), "activated": _ts(619), "lastLogin": _ts(360),"passwordChanged": _ts(390), "profile": {"login": "yusuf.a@apexlabs.io",         "firstName": "Yusuf",    "lastName": "Ahmed",      "email": "yusuf.a@apexlabs.io",        "mobilePhone": None,           "department": "Sales",         "title": "Sales Ops"}},
    # Suspended and deprovisioned
    {"id": "00u26z","status": "SUSPENDED",     "created": _ts(900), "activated": _ts(899), "lastLogin": _ts(400), "passwordChanged": _ts(400), "profile": {"login": "zoe.b@apexlabs.io",  "firstName": "Zoe",      "lastName": "Barnes",     "email": "zoe.b@apexlabs.io",          "mobilePhone": None,           "department": "Engineering",   "title": "Former Contractor"}},
    {"id": "00u27a","status": "DEPROVISIONED",  "created": _ts(950), "activated": _ts(949), "lastLogin": _ts(500), "passwordChanged": _ts(500), "profile": {"login": "adam.c@apexlabs.io", "firstName": "Adam",     "lastName": "Cole",       "email": "adam.c@apexlabs.io",         "mobilePhone": None,           "department": "Finance",       "title": "Former Controller"}},
    {"id": "00u28b","status": "DEPROVISIONED",  "created": _ts(960), "activated": _ts(959), "lastLogin": _ts(550), "passwordChanged": _ts(550), "profile": {"login": "beth.d@apexlabs.io", "firstName": "Beth",     "lastName": "Dawson",     "email": "beth.d@apexlabs.io",         "mobilePhone": None,           "department": "HR",            "title": "Former CHRO"}},
    # Staged (never activated)
    {"id": "00u29c","status": "STAGED",         "created": _ts(5),   "activated": None,     "lastLogin": None,     "passwordChanged": None,     "profile": {"login": "chris.e@apexlabs.io","firstName": "Chris",    "lastName": "Evans",      "email": "chris.e@apexlabs.io",        "mobilePhone": None,           "department": "Engineering",   "title": "New Hire"}},
    {"id": "00u30d","status": "STAGED",         "created": _ts(3),   "activated": None,     "lastLogin": None,     "passwordChanged": None,     "profile": {"login": "diana.f@apexlabs.io","firstName": "Diana",    "lastName": "Fischer",    "email": "diana.f@apexlabs.io",        "mobilePhone": None,           "department": "Marketing",     "title": "New Hire"}},
]

# Pad to simulate 300 users (remaining 270 are condensed summaries)
_EXTRA_USERS = []
_DEPARTMENTS = ["Engineering", "Product", "Sales", "Marketing", "HR", "Finance", "Legal", "IT", "Security", "Support", "Design"]
_TITLES = ["Engineer", "Senior Engineer", "PM", "Analyst", "Specialist", "Manager", "Lead", "Coordinator"]
for i in range(31, 301):
    _uid = f"00u{i}x"
    _days_since_login = (i % 30) + 1
    _dept = _DEPARTMENTS[i % len(_DEPARTMENTS)]
    _title = _TITLES[i % len(_TITLES)]
    _EXTRA_USERS.append({
        "id": _uid,
        "status": "ACTIVE",
        "created": _ts(700 - i),
        "activated": _ts(699 - i),
        "lastLogin": _ts(_days_since_login),
        "passwordChanged": _ts(60),
        "profile": {
            "login": f"user{i}@apexlabs.io",
            "firstName": f"User{i}",
            "lastName": "Apexlabs",
            "email": f"user{i}@apexlabs.io",
            "mobilePhone": f"+1415555{i:04d}",
            "department": _dept,
            "title": _title,
        },
    })

USERS = USERS + _EXTRA_USERS


# Users with NO MFA factors enrolled (8+ users)
USERS_WITHOUT_MFA = [u["id"] for u in USERS if u["id"] in {
    "00u11k", "00u14n", "00u17q", "00u20t", "00u22v", "00u24x", "00u25y", "00u26z", "00u29c", "00u30d"
}]


# MFA factors per user (only enrolled ones are listed; absent = no factors)
MFA_FACTORS = {
    "00u1a":  [{"id": "mfa001", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(500), "lastUpdated": _ts(30)}],
    "00u2b":  [{"id": "mfa002", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(480), "lastUpdated": _ts(60)}],
    "00u3c":  [{"id": "mfa003", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(460), "lastUpdated": _ts(45)},
               {"id": "mfa003b","factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(400), "lastUpdated": _ts(10)}],
    "00u4d":  [{"id": "mfa004", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(440), "lastUpdated": _ts(20)}],
    "00u5e":  [{"id": "mfa005", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(420), "lastUpdated": _ts(25)}],
    "00u6f":  [{"id": "mfa006", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(400), "lastUpdated": _ts(8)}],
    "00u7g":  [{"id": "mfa007", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(380), "lastUpdated": _ts(15)}],
    "00u8h":  [{"id": "mfa008", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(360), "lastUpdated": _ts(50)}],
    "00u9i":  [{"id": "mfa009", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(340), "lastUpdated": _ts(14)}],
    "00u10j": [{"id": "mfa010", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(320), "lastUpdated": _ts(20)}],
    "00u12l": [{"id": "mfa012", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(300), "lastUpdated": _ts(100)}],
    "00u13m": [{"id": "mfa013", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(280), "lastUpdated": _ts(110)}],
    "00u15o": [{"id": "mfa015", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(260), "lastUpdated": _ts(130)}],
    "00u16p": [{"id": "mfa016", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(240), "lastUpdated": _ts(150)}],
    "00u18r": [{"id": "mfa018", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(220), "lastUpdated": _ts(180)}],
    "00u19s": [{"id": "mfa019", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(200), "lastUpdated": _ts(200)}],
    "00u21u": [{"id": "mfa021", "factorType": "push",                 "provider": "OKTA",   "status": "ACTIVE", "created": _ts(180), "lastUpdated": _ts(250)}],
    "00u23w": [{"id": "mfa023", "factorType": "token:software:totp", "provider": "GOOGLE", "status": "ACTIVE", "created": _ts(160), "lastUpdated": _ts(300)}],
}
# Extra users (31-300): 90% have MFA
for _u in _EXTRA_USERS:
    _idx = int(_u["id"].replace("00u", "").replace("x", ""))
    if _idx % 10 != 0:  # 90% enrolled
        MFA_FACTORS[_u["id"]] = [{"id": f"mfa{_idx}", "factorType": "push", "provider": "OKTA", "status": "ACTIVE", "created": _ts(400), "lastUpdated": _ts(30)}]


GROUPS = [
    {"id": "grp1a",  "profile": {"name": "Engineering",       "description": "All engineering staff",          "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(10),  "lastMembershipUpdated": _ts(5),  "_links": {}},
    {"id": "grp2b",  "profile": {"name": "Product",           "description": "Product management team",        "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(15),  "lastMembershipUpdated": _ts(8),  "_links": {}},
    {"id": "grp3c",  "profile": {"name": "Security",          "description": "Security team",                  "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(20),  "lastMembershipUpdated": _ts(12), "_links": {}},
    {"id": "grp4d",  "profile": {"name": "Finance",           "description": "Finance and accounting",         "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(25),  "lastMembershipUpdated": _ts(15), "_links": {}},
    {"id": "grp5e",  "profile": {"name": "HR",                "description": "Human resources",                "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(30),  "lastMembershipUpdated": _ts(20), "_links": {}},
    {"id": "grp6f",  "profile": {"name": "Sales",             "description": "Go-to-market and sales",         "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(35),  "lastMembershipUpdated": _ts(25), "_links": {}},
    {"id": "grp7g",  "profile": {"name": "Marketing",         "description": "Marketing and growth",           "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(40),  "lastMembershipUpdated": _ts(28), "_links": {}},
    {"id": "grp8h",  "profile": {"name": "Legal",             "description": "Legal and compliance",           "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(45),  "lastMembershipUpdated": _ts(30), "_links": {}},
    {"id": "grp9i",  "profile": {"name": "IT",                "description": "IT operations",                  "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(50),  "lastMembershipUpdated": _ts(35), "_links": {}},
    {"id": "grp10j", "profile": {"name": "Design",            "description": "UX and visual design",           "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(55),  "lastMembershipUpdated": _ts(40), "_links": {}},
    {"id": "grp11k", "profile": {"name": "Support",           "description": "Customer support",               "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(60),  "lastMembershipUpdated": _ts(45), "_links": {}},
    {"id": "grp12l", "profile": {"name": "Executives",        "description": "Executive leadership team",      "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(65),  "lastMembershipUpdated": _ts(50), "_links": {}},
    {"id": "grp13m", "profile": {"name": "Contractors",       "description": "External contractors",           "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(70),  "lastMembershipUpdated": _ts(55), "_links": {}},
    {"id": "grp14n", "profile": {"name": "All Employees",     "description": "Everyone in the org",            "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(1),   "lastMembershipUpdated": _ts(1),  "_links": {}},
    {"id": "grp15o", "profile": {"name": "Admins",            "description": "Okta and IT administrators",     "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(10),  "lastMembershipUpdated": _ts(10), "_links": {}},
    # Empty groups (5 of them)
    {"id": "grp56a", "profile": {"name": "APAC Office",       "description": "Asia Pacific region staff",      "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(200), "lastMembershipUpdated": _ts(200),"_links": {}},
    {"id": "grp57b", "profile": {"name": "EMEA Office",       "description": "Europe Middle East Africa",      "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(180), "lastMembershipUpdated": _ts(180),"_links": {}},
    {"id": "grp58c", "profile": {"name": "Board Members",     "description": "Board of directors",             "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(150), "lastMembershipUpdated": _ts(150),"_links": {}},
    {"id": "grp59d", "profile": {"name": "Alumni",            "description": "Former employees with portal access", "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(365), "lastMembershipUpdated": _ts(365),"_links": {}},
    {"id": "grp60e", "profile": {"name": "Temp Workers",      "description": "Temporary seasonal workers",     "groupType": "OKTA_GROUP"}, "type": "OKTA_GROUP", "lastUpdated": _ts(400), "lastMembershipUpdated": _ts(400),"_links": {}},
]

# Pad to 60 groups
for i in range(16, 56):
    GROUPS.insert(-5, {
        "id": f"grp{i}z",
        "profile": {"name": f"Team-{i}", "description": f"Auto-provisioned group {i}", "groupType": "OKTA_GROUP"},
        "type": "OKTA_GROUP",
        "lastUpdated": _ts(50 + i),
        "lastMembershipUpdated": _ts(30 + i),
        "_links": {},
    })

EMPTY_GROUP_IDS = {"grp56a", "grp57b", "grp58c", "grp59d", "grp60e"}

GROUP_MEMBERS = {
    "grp1a":  [u for u in USERS if u["profile"].get("department") == "Engineering"],
    "grp2b":  [u for u in USERS if u["profile"].get("department") == "Product"],
    "grp3c":  [u for u in USERS if u["profile"].get("department") == "Security"],
    "grp4d":  [u for u in USERS if u["profile"].get("department") == "Finance"],
    "grp5e":  [u for u in USERS if u["profile"].get("department") == "HR"],
    "grp6f":  [u for u in USERS if u["profile"].get("department") == "Sales"],
    "grp7g":  [u for u in USERS if u["profile"].get("department") == "Marketing"],
    "grp8h":  [u for u in USERS if u["profile"].get("department") == "Legal"],
    "grp9i":  [u for u in USERS if u["profile"].get("department") == "IT"],
    "grp10j": [u for u in USERS if u["profile"].get("department") == "Design"],
    "grp11k": [u for u in USERS if u["profile"].get("department") == "Support"],
    "grp12l": [USERS[0], USERS[1], USERS[4]],
    "grp13m": [u for u in USERS if u["profile"].get("title") == "Contractor" or "Contractor" in u["profile"].get("title", "")],
    "grp14n": [u for u in USERS if u["status"] == "ACTIVE"],
    "grp15o": [USERS[3], USERS[2]],
}
for _g in GROUPS:
    if _g["id"] not in GROUP_MEMBERS:
        GROUP_MEMBERS[_g["id"]] = [] if _g["id"] in EMPTY_GROUP_IDS else [USERS[0]]


def _group_member_count(gid: str) -> int:
    return len(GROUP_MEMBERS.get(gid, []))


APPLICATIONS = [
    # Active apps with recent activity
    {"id": "app1a",  "name": "Slack",              "label": "Slack",              "status": "ACTIVE",   "lastUpdated": _ts(10),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(1)},
    {"id": "app2b",  "name": "GitHub",             "label": "GitHub Enterprise",  "status": "ACTIVE",   "lastUpdated": _ts(12),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(2)},
    {"id": "app3c",  "name": "Google Workspace",   "label": "Google Workspace",   "status": "ACTIVE",   "lastUpdated": _ts(5),   "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(1)},
    {"id": "app4d",  "name": "Zoom",               "label": "Zoom",               "status": "ACTIVE",   "lastUpdated": _ts(8),   "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(3)},
    {"id": "app5e",  "name": "Salesforce",         "label": "Salesforce",         "status": "ACTIVE",   "lastUpdated": _ts(15),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(5)},
    {"id": "app6f",  "name": "Jira",               "label": "Jira Cloud",         "status": "ACTIVE",   "lastUpdated": _ts(20),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(4)},
    {"id": "app7g",  "name": "Confluence",         "label": "Confluence Cloud",   "status": "ACTIVE",   "lastUpdated": _ts(22),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(6)},
    {"id": "app8h",  "name": "AWS",                "label": "Amazon Web Services","status": "ACTIVE",   "lastUpdated": _ts(25),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(7)},
    {"id": "app9i",  "name": "Okta Dashboard",     "label": "Okta Dashboard",     "status": "ACTIVE",   "lastUpdated": _ts(1),   "signOnMode": "BOOKMARK",        "features": [], "lastLoginAt": _ts(1)},
    {"id": "app10j", "name": "Figma",              "label": "Figma",              "status": "ACTIVE",   "lastUpdated": _ts(30),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(8)},
    {"id": "app11k", "name": "Notion",             "label": "Notion",             "status": "ACTIVE",   "lastUpdated": _ts(35),  "signOnMode": "OIDC",           "features": [], "lastLoginAt": _ts(10)},
    {"id": "app12l", "name": "Datadog",            "label": "Datadog",            "status": "ACTIVE",   "lastUpdated": _ts(40),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(15)},
    {"id": "app13m", "name": "PagerDuty",          "label": "PagerDuty",          "status": "ACTIVE",   "lastUpdated": _ts(45),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(20)},
    {"id": "app14n", "name": "1Password",          "label": "1Password Business", "status": "ACTIVE",   "lastUpdated": _ts(50),  "signOnMode": "OIDC",           "features": [], "lastLoginAt": _ts(5)},
    {"id": "app15o", "name": "Greenhouse",         "label": "Greenhouse ATS",     "status": "ACTIVE",   "lastUpdated": _ts(55),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(12)},
    # Apps with no recent logins (5+ apps with lastLoginAt > 90 days)
    {"id": "app16p", "name": "Workiva",            "label": "Workiva",            "status": "ACTIVE",   "lastUpdated": _ts(100), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(95)},
    {"id": "app17q", "name": "DocuSign",           "label": "DocuSign",           "status": "ACTIVE",   "lastUpdated": _ts(120), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(110)},
    {"id": "app18r", "name": "Periscope Data",     "label": "Periscope Data",     "status": "ACTIVE",   "lastUpdated": _ts(150), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(140)},
    {"id": "app19s", "name": "Lever",              "label": "Lever ATS",          "status": "INACTIVE", "lastUpdated": _ts(180), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(170)},
    {"id": "app20t", "name": "Bamboo HR Legacy",   "label": "Bamboo HR Legacy",   "status": "ACTIVE",   "lastUpdated": _ts(200), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(195)},
    {"id": "app21u", "name": "Old BI Tool",        "label": "Legacy BI Dashboard","status": "ACTIVE",   "lastUpdated": _ts(300), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(280)},
    # Active apps with NO assignments (2+)
    {"id": "app22v", "name": "Smartsheet",         "label": "Smartsheet",         "status": "ACTIVE",   "lastUpdated": _ts(90),  "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": None},
    {"id": "app23w", "name": "Miro",               "label": "Miro Whiteboard",    "status": "ACTIVE",   "lastUpdated": _ts(85),  "signOnMode": "OIDC",           "features": [], "lastLoginAt": None},
    {"id": "app24x", "name": "Loom",               "label": "Loom Video",         "status": "ACTIVE",   "lastUpdated": _ts(80),  "signOnMode": "OIDC",           "features": [], "lastLoginAt": None},
    # Inactive apps
    {"id": "app25y", "name": "Trello Legacy",      "label": "Trello (Deprecated)","status": "INACTIVE", "lastUpdated": _ts(400), "signOnMode": "SAML_2_0",       "features": [], "lastLoginAt": _ts(400)},
]

# Pad to 45 apps
for i in range(26, 46):
    APPLICATIONS.append({
        "id": f"app{i}z",
        "name": f"SaaS Tool {i}",
        "label": f"SaaS Tool {i}",
        "status": "ACTIVE",
        "lastUpdated": _ts(30 + i),
        "signOnMode": "SAML_2_0",
        "features": [],
        "lastLoginAt": _ts((i % 20) + 1),
    })

NO_ASSIGNMENT_APP_IDS = {"app22v", "app23w", "app24x"}
NO_RECENT_LOGIN_APP_IDS = {"app16p", "app17q", "app18r", "app20t", "app21u"}

APP_ASSIGNMENTS = {}
for _app in APPLICATIONS:
    _aid = _app["id"]
    if _aid in NO_ASSIGNMENT_APP_IDS:
        APP_ASSIGNMENTS[_aid] = {"users": [], "groups": []}
    else:
        APP_ASSIGNMENTS[_aid] = {
            "users": [USERS[0], USERS[1]],
            "groups": [{"id": "grp14n", "profile": {"name": "All Employees"}, "type": "OKTA_GROUP"}],
        }


SIGN_ON_POLICIES = [
    {
        "id": "pol1a",
        "name": "Default Policy",
        "description": "Default authentication policy for all users",
        "priority": 10,
        "status": "ACTIVE",
        "system": True,
        "conditions": None,
        "created": _ts(700),
        "lastUpdated": _ts(30),
        "type": "OKTA_SIGN_ON",
        "_links": {},
    },
    {
        "id": "pol2b",
        "name": "MFA Required for Admins",
        "description": "Requires phishing-resistant MFA for all admin roles",
        "priority": 1,
        "status": "ACTIVE",
        "system": False,
        "conditions": {"people": {"groups": {"include": ["grp15o"]}}},
        "created": _ts(400),
        "lastUpdated": _ts(15),
        "type": "OKTA_SIGN_ON",
        "_links": {},
    },
    {
        "id": "pol3c",
        "name": "Contractor Access Policy",
        "description": "Restricts contractor sessions to 4 hours with MFA at every login",
        "priority": 2,
        "status": "ACTIVE",
        "system": False,
        "conditions": {"people": {"groups": {"include": ["grp13m"]}}},
        "created": _ts(350),
        "lastUpdated": _ts(20),
        "type": "OKTA_SIGN_ON",
        "_links": {},
    },
    {
        "id": "pol4d",
        "name": "Passwordless for Engineering",
        "description": "Allows WebAuthn passwordless login for engineering group",
        "priority": 3,
        "status": "ACTIVE",
        "system": False,
        "conditions": {"people": {"groups": {"include": ["grp1a"]}}},
        "created": _ts(200),
        "lastUpdated": _ts(5),
        "type": "OKTA_SIGN_ON",
        "_links": {},
    },
    {
        "id": "pol5e",
        "name": "Legacy App Policy",
        "description": "Password-only fallback for legacy application integrations",
        "priority": 9,
        "status": "INACTIVE",
        "system": False,
        "conditions": None,
        "created": _ts(600),
        "lastUpdated": _ts(100),
        "type": "OKTA_SIGN_ON",
        "_links": {},
    },
]

POLICY_RULES = {
    "pol1a": [
        {
            "id": "rule1a1", "name": "Catch-all MFA rule", "priority": 1, "status": "ACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "ALLOW", "requireFactor": True, "factorPromptMode": "SESSION", "sessionUsePersistentCookie": False, "sessionLifetimeInMinutes": 480}},
        },
        {
            "id": "rule1a2", "name": "Deny inactive", "priority": 99, "status": "ACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "DENY"}},
        },
    ],
    "pol2b": [
        {
            "id": "rule2b1", "name": "Admin MFA every session", "priority": 1, "status": "ACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "ALLOW", "requireFactor": True, "factorPromptMode": "ALWAYS", "sessionUsePersistentCookie": False, "sessionLifetimeInMinutes": 240}},
        },
    ],
    "pol3c": [
        {
            "id": "rule3c1", "name": "Contractor short session", "priority": 1, "status": "ACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "ALLOW", "requireFactor": True, "factorPromptMode": "ALWAYS", "sessionUsePersistentCookie": False, "sessionLifetimeInMinutes": 240}},
        },
    ],
    "pol4d": [
        {
            "id": "rule4d1", "name": "WebAuthn passwordless", "priority": 1, "status": "ACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "ALLOW", "requireFactor": True, "factorPromptMode": "SESSION", "sessionUsePersistentCookie": True, "sessionLifetimeInMinutes": 600}},
        },
    ],
    "pol5e": [
        {
            "id": "rule5e1", "name": "Password only", "priority": 1, "status": "INACTIVE",
            "conditions": {"network": {"connection": "ANYWHERE"}},
            "actions": {"signon": {"access": "ALLOW", "requireFactor": False, "factorPromptMode": "SESSION", "sessionUsePersistentCookie": False, "sessionLifetimeInMinutes": 480}},
        },
    ],
}


def get_user_by_id(user_id_or_login: str):
    for u in USERS:
        if u["id"] == user_id_or_login or u["profile"]["login"] == user_id_or_login:
            return u
    return None


def get_user_groups(user_id: str):
    result = []
    for gid, members in GROUP_MEMBERS.items():
        for m in members:
            if m["id"] == user_id:
                for g in GROUPS:
                    if g["id"] == gid:
                        result.append(g)
                break
    return result


def get_user_apps(user_id: str):
    result = []
    for app in APPLICATIONS:
        assignments = APP_ASSIGNMENTS.get(app["id"], {})
        user_ids = [u["id"] for u in assignments.get("users", [])]
        if user_id in user_ids:
            result.append(app)
    return result


def get_mfa_enrolled_count() -> tuple[int, int]:
    """Returns (total_active, enrolled_count)."""
    active_users = [u for u in USERS if u["status"] == "ACTIVE"]
    enrolled = [u for u in active_users if u["id"] in MFA_FACTORS]
    return len(active_users), len(enrolled)
