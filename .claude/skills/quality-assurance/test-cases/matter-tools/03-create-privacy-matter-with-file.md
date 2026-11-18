# Create a privacy matter with an attached file through the AI Agent

A user attaches a Data Processing Agreement in chat and asks the AI Agent for a legal review. In one reply, the agent must make a Privacy (Promoted) matter on the right board, for the right person, with the file attached.

## Messages

- S1: `Please open a legal review of the attached Fabrikam Data Processing Agreement and assign it to Grace Li. It covers Australia and New Zealand.`

Send only this message. The step fails if the agent asks a question instead of making the matter. To send a message, fill the chat box with it and submit.

## S1 Attach the file and ask for a review

In the AI Agent section, open the AI Agent named `Ask Kes Anything` and start a chat with it. Click the chat box's attach control, then run `playwright-cli upload ${CLAUDE_SKILL_DIR}/test-cases/matter-tools/files/Fabrikam_DPA.docx`. Wait until the chat box shows `Fabrikam_DPA.docx`, then send the S1 message.

Pass: the first reply shows a link to the new matter. The uuid in that link's URL is the matter id.

## S2 Find the matter on the board

From the Matters menu, open the board named `AI-Aliens`. Search for `Fabrikam` with the board's own search, then take a snapshot. The evidence must come from that snapshot.

Pass: a row whose link contains the matter id has the subject `{TEST} Legal review of Fabrikam Data Processing Agreement` and shows `Grace Li`.

## S3 Open the matter and check its type and file

Open the matter from that row.

Pass: the matter page shows the type `Privacy (Promoted)` and the assignee `Grace Li`. Then `playwright-cli screenshot --filename=<case dir>/privacy-matter.png`.

Then open the matter's attachments.

Pass: they list `Fabrikam_DPA.docx`. Then `playwright-cli screenshot --filename=<case dir>/privacy-matter-file.png`.

The case's `matterUrl` is the URL of the matter page that S3 opens.
