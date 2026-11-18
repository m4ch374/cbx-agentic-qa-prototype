# Start an NDA workflow through the AI Agent

A user asks the AI Agent in chat for an NDA without saying whose template or which region. The agent must ask, then start the right workflow in the right team.

## Messages

- S1: `Hi, we're about to share pricing with Contoso Supplies and need an NDA in place first. Can you get one started?`

## Facts

- Template: our own.
- Contoso Supplies is in Australia.

## S1 Ask for an NDA in chat

Open the AI Agent named `Ask Kes Anything` and start a chat. Send the S1 message.

Pass: before it starts anything, the agent asks whose template to use and which region, in one question or in more. After the answers, a reply says it started the NDA and links to the workflow. The reply does not have to name the workflow: S2 checks that the link goes to the right one.

## S2 Open the started workflow

Open the workflow from the link in that reply.

Pass: the page is for `Contoso` and shows that the workflow is not complete.

Screenshot: `nda-workflow`

Network check: among the responses that this page loaded, find the one that describes this started workflow. It must name the workflow `[KITBAG] Self Service NDA`.

## S3 Find it under its workflow

Find the workflow `[KITBAG] Self Service NDA` of the team `Legal Team`, and open its list of started workflows. The app can call them assessments or submissions.

Pass: a row in that list is for the same record as the link from S1. If the row is not on the first page, use the list's search, sort or pages to find it.

Screenshot: `nda-workflow-list`
