# Drafting test cases from a ticket

Use this while a person works on a ticket. You draft or change test cases and use cases in this skill folder. The person opens a PR on the QA repo; a draft becomes a fixed test case only when that PR merges.

`${CLAUDE_SKILL_DIR}` is a link into the person's clone of the QA repo, so edits made here land in that clone.

## Use cases and test cases

- A **use case** says what the product can do, never how. Good: "Legal Front Door lets users create AI Agents." Bad: "Users open the dashboard and click Create agent."
- Use cases exist only so you can draft test cases. A run never reads them.
- A **test case** says what a user does and what must then be true: the messages to type, the named things to open, and the result to check. It does not say where a control is. It stands alone and never cites a use case, a PRD or a requirement ID.
- So a UI change that only moves or renames a control touches nothing. A change to a journey touches only test cases. A use case changes only when the product gains or loses a capability.

## 1. Read the context

Read everything you can find about the change. Ask the person only for what you cannot find.

- The ticket: use the Atlassian connector for a Jira key, or read what the person pasted.
- The code: the branch diff against its base, and the files it touches.
- The PRD or spec the ticket links to.
- `${CLAUDE_SKILL_DIR}/use-cases/`: what the product can already do, by product slice.
- `${CLAUDE_SKILL_DIR}/test-cases/`: the suites and cases that exist.

## 2. Decide

Pick one and tell the person which and why:

| Ticket | Result |
|---|---|
| A journey changed, the capability did not | Change the cases that cover it. Leave use cases alone |
| A control moved or got a new label | No change, unless a case names that label: then remove the label from the case |
| A bug with no case that would catch it | Add a case that fails before the fix and passes after it |
| A new feature or a greenfield epic | Add use-case lines and a case, in a new suite if no suite fits |
| A feature is removed | Delete its use-case lines and the cases that cover it |
| No change a user can see (refactor, infra, tooling) | No QA needed: say why |

## 3. Find the steps in the UI

Open the live UI on the person's local stack and do the journey once. Take the how from the UI only, never from a use case or the PRD. Write down the names that a user gives or that an admin set (an AI Agent, a board, a person, a status), not the menus and buttons on the way.

## 4. Write

- **Use case.** Edit `use-cases/<product-slice>/<area>.md` only for a new or removed capability. Write each line as "<product> lets users <do what>", plus a link to the PRD. Never write UI labels, screen or page names, routes, URLs, selectors, configuration names or click order. If you find any of these in a use case you read, rewrite that line as a capability.
- **Case.** One file is one video: one user journey from start to end. Name it `NN-<what-it-does>.md` in its suite, numbered after the last case. Write it the way `test-cases/matter-tools/01-create-edit-find-matter.md` is written:
  - a title and one or two sentences on the journey;
  - the exact messages to type, and a `## Facts` list of what the user knows, for the questions an AI Agent can ask. Do not write fixed answers: the agent's questions change;
  - steps `S1`, `S2`, … that each say what the user does, then `Pass:` and what must be true;
  - names in backticks, not IDs, URLs or menu paths, for the things it opens (an AI Agent, a board, a person);
  - a check of the record in the product (a board row, a matter page) for each thing an AI Agent says it did. Never pass a step on the wording of a reply;
  - backticks in a `Pass:` line only for text that the product must show exactly, such as a name or a status. Write text that an AI Agent composes (a subject, a description, a note) in plain words, so that it passes on meaning;
  - records that are found by their link, not by their text, because an earlier run can leave the same text;
  - a result that stays true on a shared environment: take an expected list from the product during the run, never from a fixed count;
  - a `Screenshot: <name>` line where a picture helps the reader;
  - a `needs: <case>` line under the title only when it uses what an earlier case made;
  - no link to, or mention of, a use case, a PRD or a requirement ID.
- **SETUP.** A new suite needs `SETUP.md`: first a cleanup that deletes only what earlier runs of this suite made, then the setup that makes or checks each prerequisite by name. A case never creates its own prerequisites.

## 5. Check the draft

Run it on the person's local stack: `run <suite>/<case>`. Fix the draft until it passes on the fixed code. For a bug, it should also fail on the code before the fix, when that is easy to check.

## 6. Hand over

Tell the person which files you changed in the QA repo clone, and that a PR on the QA repo makes the draft a fixed test case.
