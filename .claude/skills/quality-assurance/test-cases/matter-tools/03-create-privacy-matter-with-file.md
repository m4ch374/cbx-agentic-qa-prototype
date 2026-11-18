# Create a privacy matter with an attached file through the AI Agent

A user attaches a Data Processing Agreement in chat and asks the AI Agent for a legal review. The agent must make a Privacy (Promoted) matter on the right board, for the right person, with the file attached.

## Messages

- S1: `Please open a legal review of the attached Fabrikam Data Processing Agreement and assign it to Grace Li. It covers Australia and New Zealand.`

## Facts

The matter type can have required fields that the message does not give, so the agent can ask for them.

- The agreement is a Data Processing Agreement with Fabrikam.
- It covers Australia and New Zealand.
- For each date that the agent asks for: today's date.
- Time zone: Sydney, Australia.
- The user approves what the S1 message asks for.

## S1 Attach the file and ask for a review

Open the AI Agent named `Ask Kes Anything` and start a chat. Attach the file `${CLAUDE_SKILL_DIR}/test-cases/matter-tools/files/Fabrikam_DPA.docx`: use the chat box's attach control, then `playwright-cli upload <that path>`. Wait until the chat box shows `Fabrikam_DPA.docx`, then send the S1 message.

Pass: the agent makes a matter, and a reply links to it. Write down that link.

## S2 Find the matter on the board

Open the board named `AI-Aliens`. Search the board for `Fabrikam`. Take a snapshot: the evidence must come from it.

Pass: the row for the matter from S1 has a subject that names Fabrikam and the Data Processing Agreement, and it shows the assignee `Grace Li`.

## S3 Open the matter and check its type and file

Open the matter from that row.

Pass: the matter page shows the type `Privacy (Promoted)` and the assignee `Grace Li`.

Screenshot: `privacy-matter`

Then open the part of the matter that shows its files.

Pass: the files include `Fabrikam_DPA.docx`.

Screenshot: `privacy-matter-file`

The case's `matterUrl` is the URL of the matter page that S3 opens.
