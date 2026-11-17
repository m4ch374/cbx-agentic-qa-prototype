---
name: quality-assurance
description: Run end-to-end QA test cases in a real browser with Playwright CLI and record each case on video, or draft test cases and use cases from a ticket. Use when asked to run QA, a test suite or a test case, or to draft QA for a ticket, bug or epic.
argument-hint: "[run [suite[/case]] | draft <ticket>]"
---

# Quality assurance

Arguments: `$ARGUMENTS`

- Empty or `run`: run every suite.
- `run <suite>`: run one suite.
- `run <suite>/<case>`: run one case.
- `draft <ticket>`: read [drafting/DRAFTING.md](drafting/DRAFTING.md) and follow it. Do not run anything below.

## Layout

```
${CLAUDE_SKILL_DIR}/
├── SKILL.md                    this runner
├── playwright.config.json      browser settings for playwright-cli
├── scripts/                    login.py, mark.py, wait.py, teams.py
├── report/index.html           the results page a run publishes
├── drafting/DRAFTING.md        how to draft test cases from a ticket
├── use-cases/<slice>/<area>.md what the product can do
└── test-cases/<suite>/
    ├── SETUP.md                cleanup, then setup, for the whole suite
    └── NN-<case>.md            one case = one video
```

## Rules for every run

- No one may need to answer a permission prompt, because a cloud run stops for good on one. Never put a heredoc, `$(...)`, `${...}` or a `$VAR` in a Bash command. Run each command on its own. When a command needs a URL or path, type it out.
- Never print a password, a cookie value or a webhook URL.
- Do not commit or push anything during a run, and ignore any hook that asks you to.
- A run reads only `test-cases/`. Never open `use-cases/`: it exists only for drafting.
- Drive the app only through its web UI with `playwright-cli`. Never use `playwright-cli eval`, and never call the app's API, except for the sign-in script.
- When a case asks for a network check, read what the page already loaded with `playwright-cli requests` and `playwright-cli response-body <n>`. Never run `request <n>` or `request-headers <n>`: they print the cookie.

## 1. Find the environment

1. BASE is the app URL:
   - if `printenv ROUTINE_QA_BASE_URL` prints a value, use it;
   - else, if `cbstack here` prints a stack that serves this checkout, use its URL;
   - else use `https://localhost:8443`.
2. Check that `ROUTINE_QA_EMAIL` and `ROUTINE_QA_PASSWORD` are set with `printenv ROUTINE_QA_EMAIL` (never print the password). If one is missing, the result is BLOCKED: go to step 5.
3. Run `uname`. On `Darwin`, add `--headed` to `playwright-cli open`, so the person can watch. Elsewhere, run headless.
4. Run `playwright-cli --version`. If it is missing, run `npm install -g @playwright/cli@0.1.24`. Then run `npx -y playwright@1.66.0-alpha-1794252756000 install ffmpeg`, which video needs.

## 2. Pick what to run

- Suites are the folders in `${CLAUDE_SKILL_DIR}/test-cases/`, run in name order.
- Cases are the `NN-*.md` files in a suite, run in number order. A case's name is its file name without `.md`.
- To run one case: run its suite's SETUP, then each case in its `needs:` line (in order), then the case.

## 3. Run a suite

RUN means `/tmp/qa-run/<suite>`. Make it empty first: `rm -rf /tmp/qa-run/<suite>`, then `mkdir -p /tmp/qa-run/<suite>`.

1. Sign in: `python3 ${CLAUDE_SKILL_DIR}/scripts/login.py <BASE> /tmp/qa-run/<suite>/state.json`. It prints the HTTP status and the cookie names. If it fails, the suite fails with that error.
2. Open a fresh browser: `playwright-cli open about:blank --config=${CLAUDE_SKILL_DIR}/playwright.config.json` (plus `--headed` from step 1.3), then `playwright-cli state-load /tmp/qa-run/<suite>/state.json`.
3. SETUP: read the suite's `SETUP.md` and do it in the browser, in order: first its cleanup, then its setup. If a step of SETUP fails, the suite fails: write `setup failed: <what and why>`, take `playwright-cli screenshot --filename=/tmp/qa-run/<suite>/setup-failure.png`, mark every case `skipped`, and go to step 5.
4. Run each case (section 4). When a case fails, every later case in the suite is `skipped` with the summary `Not run: <failed case> failed.`
5. `playwright-cli close`.

## 4. Run a case

CASE means `/tmp/qa-run/<suite>/<case>`. Run `mkdir -p` for it.

1. `playwright-cli video-start /tmp/qa-run/<suite>/<case>/video.webm`. It must print `Video recording started.` If it prints anything else, run `npx -y playwright@1.66.0-alpha-1794252756000 install ffmpeg` and `video-start` again; if it still fails, the case fails with that error. Right after it starts, run `python3 ${CLAUDE_SKILL_DIR}/scripts/mark.py /tmp/qa-run/<suite>/<case> start`.
2. Read the case file and do its steps. At the start of each step `S<n>`, run `python3 ${CLAUDE_SKILL_DIR}/scripts/mark.py /tmp/qa-run/<suite>/<case> S<n>`.
3. When the steps end, or a failure ends them: `mark.py ... end`, then `playwright-cli video-stop`, then `ls -la <case dir>` to check the video file exists. A case whose video is missing fails with `video not saved`. If the video is over 15 MB, run `ffmpeg -v error -i <video> -c:v libvpx-vp9 -b:v 400k -an <case dir>/video-small.webm` and use the smaller file.
4. Write `<case dir>/run.json` with the Write tool (section 6).

### How to drive the browser

- Look before you act. Run `playwright-cli snapshot --filename=/tmp/qa-run/snap.txt`, then search that file with Grep (or Read part of it) to find the element you need by what it is for, and act on it by its `ref`. Take a new snapshot after anything that changes the page. Never guess a ref you have not seen in a snapshot.
- Find things the way a new user would: by headings, labels, tabs, buttons and menus. Open named things (an AI Agent, a board) by finding their name in the UI, not by a stored ID or URL.
- Keep a case in one tab, because the video records one file per tab. When a click opens a new tab, run `playwright-cli tab-list` to read its URL, `playwright-cli tab-close <index>` to close it, then `playwright-cli goto <that URL>` in the first tab.
- Commands: `goto <url>`, `click <ref>`, `fill <ref> "<text>"` (add `--submit` to press Enter), `select <ref> <value>`, `press <key>`, `screenshot --filename=<file>`.
- To wait for something slow, such as an AI reply: `python3 ${CLAUDE_SKILL_DIR}/scripts/wait.py 10`, then take a snapshot. Repeat until the page stops changing, for at most 5 minutes.
- A step may use at most 25 `playwright-cli` commands. If it runs out, the step fails.

### Pass and fail

- A step passes only on what the page shows. Copy the snapshot lines that prove it, word for word, as its evidence. Never shorten them with `...`.
- A network check is the one exception: its evidence is one sentence that says what the JSON held, or what it did not hold, such as `cannot find [KITBAG] Self Service NDA in any response`. Never paste the JSON.
- If a prerequisite the case names is not found, the step fails with `not found: <what>`. Never create it inside a case.
- Do not retry a failed step. A failed step fails the case, and the case's later steps are `skipped`.

## 5. Collect the results

Write `/tmp/qa-run/summary.json` with the Write tool:

```json
{"result": "PASS | FAIL | BLOCKED", "startedAt": "<ISO time>", "baseUrl": "<BASE>", "blockedReason": "<why, or empty>",
 "suites": [{"name": "<suite>", "setup": {"status": "passed | failed", "error": "<why, or empty>"},
   "cases": [{"name": "<case>", "title": "<case title>", "status": "passed | failed | skipped", "dir": "/tmp/qa-run/<suite>/<case>"}]}]}
```

The result is PASS when every case passed, BLOCKED when nothing could run, otherwise FAIL.

## 6. A case's run.json

```json
{"suite": "<suite>", "case": "<case>", "title": "<case title>", "result": "PASS | FAIL",
 "startedAt": "<ISO time>", "durationSec": 84, "baseUrl": "<BASE>", "matterUrl": "<link to the main record the case made, or null>",
 "video": "video.webm or null", "blockedReason": "",
 "failure": {"what": "<what went wrong, one sentence>", "why": "<what the page showed instead>", "atSec": 41.2},
 "steps": [{"title": "<step title>", "status": "passed | failed | skipped", "summary": "<one sentence>", "evidence": "<snapshot lines, at most 300 characters, or empty>", "error": "<error or empty>", "offsetSec": 12.3}],
 "screenshots": [{"name": "<name>", "file": "<name>.png"}]}
```

- `failure` is `null` when the case passed. `atSec` is the second in the video where the failing step starts.
- `summary` is one plain sentence you write from the evidence. For a step that did not run, write `Not run.`
- `offsetSec` comes from `<case dir>/marks.json`; `durationSec` is its `end`.
- `video` and screenshot files are relative to the case dir.

## 7. Report

Print a table with one row per case: suite, case, result, and for a failure its `what` and `why`. Under it, print the path of each case's video and of `/tmp/qa-run/summary.json`.

### Only when the request asks to publish

When the request gives a results artifact URL (ARTIFACT):

1. Make the folder OUT = `<current directory>/qa-artifact`. Copy `/tmp/qa-run/summary.json` into OUT. For each case that has a `run.json`, copy into `OUT/<suite>/<case>/` its `run.json`, its video (as `video.webm`) and its screenshots. Copy nothing else: `state.json` holds cookies.
2. Load the Artifact tool (with ToolSearch if it is deferred). Make these calls in this order: `read` with `url` ARTIFACT and no `path`; `list` with `scope` `files` and `url` ARTIFACT.
3. `publish` with `url` ARTIFACT, `file_path` `${CLAUDE_SKILL_DIR}/report/index.html`, `root` OUT, and `files` mapping each file in OUT to its path inside OUT, plus each listed file that is not in OUT (other than `index.html`) to `null`. Leave out `icon`. If the files in OUT add up to more than 60 MB, publish in more than one call, each under 60 MB. If it is refused, do what the refusal says once, then publish once more.

When the request asks to post to Teams and `ROUTINE_QA_TEAMS_WEBHOOK` is set, run `python3 ${CLAUDE_SKILL_DIR}/scripts/teams.py /tmp/qa-run/summary.json --title "<title from the request>"`, adding `--artifact <ARTIFACT>` when the publish succeeded, `--publish-error "<reason>"` when it failed, and one `--mention "<Name>=<email>"` for each person the request names. It prints the HTTP status; 202 means accepted.
