# Search matters by type and assignee through the AI Agent

needs: 03-create-privacy-matter-with-file

A user asks the AI Agent for every privacy matter assigned to one person. The reply must list each matching matter, including the one made today, and no other matter.

## Messages

- S2: `Can you show me all the privacy matters assigned to Grace Li?`

Send only this message. To send a message, fill the chat box with it and submit.

## S1 List the expected matters on the board

From the Matters menu, open the board named `AI-Aliens`. Filter it by assignee `Grace Li` and by type `Privacy (Promoted)`, then take a snapshot. If the board pages its rows, go through every page.

Pass: the rows include the matter from `03-create-privacy-matter-with-file`. Write down every row's matter id, the uuid in its link. This is the expected list. Then `playwright-cli screenshot --filename=<case dir>/expected-matters.png`.

## S2 Ask the agent for the same matters

In the AI Agent section, open the AI Agent named `Ask Kes Anything` and start a new chat with it. Send the S2 message.

Pass: the reply links to every matter id on the expected list, and to no other matter. Copy each matter link from the reply as evidence.
