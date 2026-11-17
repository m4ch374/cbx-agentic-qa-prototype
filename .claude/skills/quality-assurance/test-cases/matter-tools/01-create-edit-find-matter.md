# Create, edit and find a matter through the AI Agent

A user asks the AI Agent in chat to open a matter, then asks it in the same chat to change the matter. The changes must show on the board and on the matter page.

## Messages

- S1: `Hi, I'm in-house counsel handling the logistics services agreement with Northwind Freight. They sent back redlines on their own paper. Please open a matter for my review.`
- S2: `Thanks. Grace is out this week, so I'm handing my review to Kesnavi Parammanandhan. Please reassign the matter to Kesnavi, move it to Pending response, and set the description to: Northwind wants a 30-day payment term and a liability cap at 1x fees. Also add a note to the matter: Kesnavi to review by Friday.`
- Follow-up: `Yes, go ahead. It is their paper, a logistics services agreement for North America, about 120,000 USD, no deadline.`

When the agent asks a question instead of acting, send the follow-up, up to 4 replies in a step. Send no other messages. To send a message, fill the chat box with it and submit.

## S1 Create the matter in chat

In the AI Agent section, open the AI Agent named `Ask Kes Anything` and start a chat with it. Send the S1 message.

Pass: a reply shows a link whose URL contains `ticketId=<uuid>`. That uuid is the matter id. Write down the matter's subject as the chat shows it.

## S2 Edit the matter in the same chat

Send the S2 message in the same chat.

Pass: the reply says the matter was reassigned to Kesnavi, moved to Pending response, and given the description and the note.

## S3 Find the matter on the board

From the Matters menu, open the board named `AI-Aliens`. Search for `Northwind Freight` with the board's own search, then take a snapshot. The evidence must come from that snapshot.

Pass: a row links to `/app/ticketing/tickets/<matter id>` and shows `Kesnavi Parammanandhan` and `Pending response`. Then `playwright-cli screenshot --filename=<case dir>/board-search.png`.

## S4 Open the matter and check the description and note

Open the matter from that row.

Pass: the matter page shows `Northwind wants a 30-day payment term and a liability cap at 1x fees`. Then `playwright-cli screenshot --filename=<case dir>/matter-details.png`.

Then open the matter's conversation.

Pass: it shows `Kesnavi to review by Friday`. Then `playwright-cli screenshot --filename=<case dir>/matter-conversations.png`.

The case's `matterUrl` is BASE + `/app/ticketing/tickets/<matter id>`.
