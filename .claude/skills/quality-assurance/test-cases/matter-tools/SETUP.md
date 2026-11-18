# Matter tools: setup

The cases in this suite talk to an AI Agent that makes, changes and finds matters and starts workflows. The agent's routing table, the board, the users and the workflow are too large to build through the UI on each run, so this SETUP only checks that they exist and fails when one is missing.

## Cleanup

Remove the matters that earlier runs of this suite made. Delete only these rows, never other matters on the board.

1. Open the board named `AI-Aliens`.
2. Do steps 3 to 5 once for `Northwind` and once for `Fabrikam`.
3. Search the board for the name.
4. Select each row whose subject starts with `{TEST}` and contains the name, and no other row. Delete the selected rows. Before you confirm, compare the number of matters that the app says it will delete with the number of rows you selected. If the numbers are different, cancel: SETUP fails.
5. Search again. That name is done when no such row is left. If there were no such rows, it is done.

## Setup

Check each prerequisite by finding its name in the UI. If one is missing, SETUP fails with `not found: <name>`.

1. An AI Agent named `Ask Kes Anything`.
2. A board named `AI-Aliens`.
3. People named `Kesnavi Parammanandhan` and `Grace Li`, who can be assignees on that board: the board shows each name where a user picks or filters an assignee.
4. A workflow named `[KITBAG] Self Service NDA` in the team `Legal Team`.
5. The file `${CLAUDE_SKILL_DIR}/test-cases/matter-tools/files/Fabrikam_DPA.docx`: check it with `ls`.
