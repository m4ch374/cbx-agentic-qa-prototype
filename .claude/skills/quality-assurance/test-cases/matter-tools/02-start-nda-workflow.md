# Start an NDA workflow through the AI Agent

A user asks the AI Agent in chat for an NDA without saying whose template or which region. The agent must ask, then start the right workflow in the right team.

## Messages

- S1: `Hi, we're about to share pricing with Contoso Supplies Pty Ltd and need an NDA in place first. Can you get one started?`
- Follow-up: `Use our own template. They're in Australia.`

When the agent asks a question instead of acting, send the follow-up, up to 4 replies in the step. Send no other messages. To send a message, fill the chat box with it and submit.

## S1 Ask for an NDA in chat

In the AI Agent section, open the AI Agent named `Ask Kes Anything` and start a chat with it. Send the S1 message.

Pass: before it starts anything, the agent asks whose template to use and which region. After the follow-up, a reply says it started an NDA for `Contoso Supplies Pty Ltd` and shows a link to the workflow. The reply does not have to name the workflow: S2 checks the link goes to the right one.

## S2 Open the started workflow

Open the workflow from the link in that reply. If it opens a new tab, move it to the first tab as the run rules say.

Pass: the page shows `Contoso` and shows the workflow as not complete. Then `playwright-cli screenshot --filename=<case dir>/nda-workflow.png`.

Network check: in `playwright-cli requests`, find the response that describes this assessment. It must name the workflow `[KITBAG] Self Service NDA`.

## S3 Find it under its workflow

From the Workflows menu, open Project Teams, then the team `Legal Team`, then the workflow `[KITBAG] Self Service NDA`.

Pass: its list of assessments has a row that opens the same page as the link from S1. Then `playwright-cli screenshot --filename=<case dir>/nda-workflow-list.png`.
