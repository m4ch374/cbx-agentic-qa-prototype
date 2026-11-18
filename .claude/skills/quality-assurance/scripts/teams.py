import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

MARKS = {"passed": ("✓", "Good"), "failed": ("✗", "Attention"), "skipped": ("–", "Default")}


def text(value, **options):
    return {"type": "TextBlock", "text": value, "wrap": True, **options}


def clock(seconds):
    seconds = int(seconds or 0)
    return f"{seconds // 60}:{seconds % 60:02d}"


def load_run(case):
    path = os.path.join(case.get("dir", ""), "run.json")
    if not os.path.exists(path):
        return {}
    with open(path) as handle:
        return json.load(handle)


def step_row(number, step, link):
    status = step.get("status")
    mark, color = MARKS.get(status, MARKS["skipped"])
    title = step.get("title", "")
    if status == "skipped":
        detail = [text(f"S{number} {title} · Not run.", isSubtle=True)]
    else:
        detail = [text(f"**S{number} {title}** {step.get('summary', '')}")]
    if status == "failed":
        note = step.get("error") or step.get("evidence")
        if note:
            detail.append(text(note, isSubtle=True, fontType="Monospace", size="Small", spacing="None"))
    columns = [
        {"type": "Column", "width": "auto", "items": [text(mark, color=color, weight="Bolder")]},
        {"type": "Column", "width": "stretch", "items": detail},
    ]
    if link and status != "skipped" and step.get("offsetSec") is not None:
        columns.append({"type": "Column", "width": "auto",
                        "items": [text(f"[▶ {clock(step['offsetSec'])}]({link}.s{number})", size="Small")]})
    return {"type": "ColumnSet", "separator": True, "columns": columns}


def case_block(index, case, run, link, reason):
    status = case.get("status", "skipped")
    steps = run.get("steps", [])
    mark, color = MARKS.get(status, MARKS["skipped"])
    title = case.get("title") or run.get("title") or case.get("name", "")
    failed_at = next((n for n, step in enumerate(steps, start=1) if step.get("status") == "failed"), None)
    if status == "skipped":
        right = reason
    else:
        passed = sum(step.get("status") == "passed" for step in steps)
        right = f"{passed}/{len(steps)} · {clock(run.get('durationSec'))}"
    target = f"steps-{index}"
    columns = [
        {"type": "Column", "width": "auto", "items": [text(mark, color=color, weight="Bolder", size="Medium")]},
        {"type": "Column", "width": "stretch", "verticalContentAlignment": "Center",
         "items": [text(title, weight="Bolder", isSubtle=status == "skipped")]},
        {"type": "Column", "width": "auto", "verticalContentAlignment": "Center",
         "items": [text(right, isSubtle=True, size="Small")]},
    ]
    if steps:
        for column in columns:
            column["selectAction"] = {"type": "Action.ToggleVisibility", "targetElements": [target]}
    if link and status != "skipped":
        watch = f"[▶ Watch the failure]({link}.s{failed_at})" if failed_at else f"[▶ Watch]({link})"
        columns.append({"type": "Column", "width": "auto", "verticalContentAlignment": "Center",
                        "items": [text(watch, size="Small", weight="Bolder")]})
    items = [{"type": "ColumnSet", "columns": columns}]
    failure = run.get("failure")
    if failure:
        where = f"**S{failed_at} failed at {clock(failure.get('atSec'))}.** " if failed_at else ""
        items.append(text(f"{where}{failure.get('what', '')} {failure.get('why', '')}".strip(), color="Attention"))
    if steps:
        rows = [step_row(n, step, link) for n, step in enumerate(steps, start=1)]
        if run.get("matterUrl"):
            rows.append(text(f"[Open the matter it made ↗]({run['matterUrl']})", size="Small", separator=True))
        items.append({"type": "Container", "id": target, "isVisible": status == "failed", "items": rows})
    return {"type": "Container", "style": "emphasis", "spacing": "Small", "items": items}


def suite_header(suite):
    setup = suite.get("setup", {})
    cases = suite.get("cases", [])
    if setup.get("status") == "failed":
        right = text("setup failed", color="Attention", size="Small")
    else:
        passed = sum(case.get("status") == "passed" for case in cases)
        right = text(f"{passed} of {len(cases)} passed", isSubtle=True, size="Small")
    header = [{"type": "ColumnSet", "spacing": "Large", "columns": [
        {"type": "Column", "width": "stretch", "items": [text(f"**{suite.get('name')}**")]},
        {"type": "Column", "width": "auto", "verticalContentAlignment": "Center", "items": [right]},
    ]}]
    if setup.get("status") == "failed":
        header.append(text(f"Setup failed: {setup.get('error', '')}", color="Attention", size="Small", spacing="None"))
    return header


def build_card(summary, title, artifact, publish_error, mentions):
    suites = summary.get("suites", [])
    runs = [[load_run(case) for case in suite.get("cases", [])] for suite in suites]
    cases = [case for suite in suites for case in suite.get("cases", [])]
    passed = sum(case.get("status") == "passed" for case in cases)
    blocked = summary.get("result") == "BLOCKED"
    if blocked:
        heading = text(f"{title}: BLOCKED", size="Large", weight="Bolder", color="Warning")
    else:
        color = "Good" if summary.get("result") == "PASS" else "Attention"
        heading = text(f"{title}: {passed} of {len(cases)} cases passed", size="Large", weight="Bolder", color=color)
    host = urlparse(summary.get("baseUrl", "")).hostname or ""
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total = sum(run.get("durationSec") or 0 for suite_runs in runs for run in suite_runs)
    meta = " · ".join(part for part in (day, host, clock(total) if total else "") if part)
    body = [heading, text(meta, isSubtle=True, spacing="None")]
    entities = []
    if mentions:
        tags = []
        for name, email in mentions:
            tag = f"<at>{name}</at>"
            tags.append(tag)
            entities.append({"type": "mention", "text": tag, "mentioned": {"id": email, "name": name}})
        body.append(text("cc " + " ".join(tags), spacing="None"))
    if blocked:
        body.append(text(summary.get("blockedReason") or "Nothing could run."))
    index = 0
    for suite, suite_runs in zip(suites, runs):
        body.extend(suite_header(suite))
        setup_failed = suite.get("setup", {}).get("status") == "failed"
        for case, run in zip(suite.get("cases", []), suite_runs):
            link = f"{artifact}#{suite.get('name')}.{case.get('name')}" if artifact else None
            reason = "Not run: setup failed" if setup_failed else case.get("reason") or "Not run"
            body.append(case_block(index, case, run, link, reason))
            index += 1
    if publish_error:
        body.append(text(f"The recording page was not updated: {publish_error}", color="Warning"))
    card = {
        "type": "AdaptiveCard",
        "version": "1.4",
        "msteams": {"width": "Full", "entities": entities},
        "body": body,
    }
    return {"type": "message", "attachments": [{"contentType": "application/vnd.microsoft.card.adaptive", "content": card}]}


def parse_mention(value):
    name, _, email = value.partition("=")
    if not name or not email:
        raise argparse.ArgumentTypeError("use Name=email")
    return name.strip(), email.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("summary")
    parser.add_argument("--title", default="QA")
    parser.add_argument("--artifact")
    parser.add_argument("--publish-error")
    parser.add_argument("--mention", type=parse_mention, action="append", default=[])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    with open(args.summary) as handle:
        summary = json.load(handle)
    message = build_card(summary, args.title, args.artifact, args.publish_error, args.mention)
    if args.dry_run:
        print(json.dumps(message, indent=1, ensure_ascii=False))
        return
    webhook = os.environ.get("ROUTINE_QA_TEAMS_WEBHOOK")
    if not webhook:
        sys.exit("ROUTINE_QA_TEAMS_WEBHOOK is not set")
    request = urllib.request.Request(
        webhook,
        data=json.dumps(message).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            print(response.status)
    except urllib.error.HTTPError as error:
        sys.exit(f"Teams post failed: HTTP {error.code}")


if __name__ == "__main__":
    main()
