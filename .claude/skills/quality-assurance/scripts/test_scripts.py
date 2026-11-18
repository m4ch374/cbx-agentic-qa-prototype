import json
import os
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from login import is_local, parse_cookies
from teams import build_card

HERE = os.path.dirname(__file__)


def test_parse_cookies():
    cookies = parse_cookies(["cb_access_token=abc; Path=/; HttpOnly", "cb_refresh_token=x=y; Secure"], "dev.example")
    assert [c["name"] for c in cookies] == ["cb_access_token", "cb_refresh_token"]
    assert cookies[1]["value"] == "x=y"
    assert cookies[0]["domain"] == "dev.example"


def test_is_local():
    assert is_local("localhost") and is_local("henry-kong-1.orb.local")
    assert not is_local("dev.checkbox.ninja")


def test_mark():
    case_dir = tempfile.mkdtemp()
    mark = os.path.join(HERE, "mark.py")
    for name in ("start", "S1", "end"):
        subprocess.run([sys.executable, mark, case_dir, name], check=True, capture_output=True)
    with open(os.path.join(case_dir, "marks.json")) as handle:
        assert set(json.load(handle)) == {"S1", "end"}


def write_run(run):
    case_dir = tempfile.mkdtemp()
    with open(os.path.join(case_dir, "run.json"), "w") as handle:
        json.dump(run, handle)
    return case_dir


def test_card():
    good = write_run({"matterUrl": "https://dev.example/app/ticketing/tickets/1", "failure": None, "durationSec": 75,
                      "steps": [{"title": "Create", "status": "passed", "summary": "Made it.", "offsetSec": 1.0}]})
    bad = write_run({"failure": {"what": "No reply.", "why": "Spinner stayed.", "atSec": 9.0}, "durationSec": 20, "steps": [
        {"title": "Edit", "status": "failed", "summary": "Did not.", "error": "no reply", "offsetSec": 9.0},
        {"title": "Check", "status": "skipped", "summary": "Not run."},
    ]})
    summary = {"result": "FAIL", "baseUrl": "https://dev.example", "suites": [
        {"name": "s", "setup": {"status": "passed"}, "cases": [
            {"name": "01-good", "title": "Good", "status": "passed", "dir": good},
            {"name": "02-bad", "title": "Bad", "status": "failed", "dir": bad},
            {"name": "03-later", "title": "Later", "status": "skipped", "reason": "Not run: 02 failed", "dir": "/nowhere"},
        ]}]}
    card = build_card(summary, "QA", "https://claude.ai/artifact/x", None, [("Ann", "ann@example.com")])["attachments"][0]["content"]
    texts = json.dumps(card, ensure_ascii=False)
    assert card["body"][0]["text"] == "QA: 1 of 3 cases passed" and card["body"][0]["color"] == "Attention"
    assert "1:35" in card["body"][1]["text"]
    blocks = [item for item in card["body"] if item["type"] == "Container"]
    assert [b["style"] for b in blocks] == ["emphasis"] * 3
    assert blocks[0]["items"][-1]["isVisible"] is False and blocks[1]["items"][-1]["isVisible"] is True
    assert "[▶ Watch](https://claude.ai/artifact/x#s.01-good)" in texts
    assert "[▶ 0:01](https://claude.ai/artifact/x#s.01-good.s1)" in texts
    assert "[▶ Watch the failure](https://claude.ai/artifact/x#s.02-bad.s1)" in texts and "03-later" not in texts
    assert "[Open the matter it made ↗](https://dev.example/app/ticketing/tickets/1)" in texts
    assert "**S1 failed at 0:09.** No reply. Spinner stayed." in texts and "no reply" in texts
    assert "Not run: 02 failed" in texts and "S2 Check · Not run." in texts and "1 of 3 passed" in texts
    assert card["msteams"]["entities"][0]["text"] == "<at>Ann</at>" and "actions" not in card
    broken = build_card({"result": "FAIL", "suites": [{"name": "x", "setup": {"status": "failed", "error": "no channel"},
                         "cases": [{"name": "01-a", "status": "skipped"}]}]}, "QA", None, None, [])
    assert "Setup failed: no channel" in json.dumps(broken) and "Not run: setup failed" in json.dumps(broken)
    blocked = build_card({"result": "BLOCKED", "blockedReason": "no creds", "suites": []}, "QA", None, None, [])
    assert "no creds" in json.dumps(blocked)


if __name__ == "__main__":
    for name, test in list(globals().items()):
        if name.startswith("test_"):
            test()
    print("ok")
