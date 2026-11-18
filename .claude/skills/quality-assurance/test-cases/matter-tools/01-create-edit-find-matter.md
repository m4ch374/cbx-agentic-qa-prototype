# Create, edit and find a matter through the AI Agent

A user asks the AI Agent in chat to open a matter, then asks it in the same chat to change the matter. The changes must show on the board and on the matter page.

## Messages

- S1: `Hi, I'm in-house counsel handling the logistics services agreement with Northwind Freight. They sent back redlines on their own paper. Please open a matter for my review.`
- S2: `Thanks. Please change the contract value to 150,000 USD, move it to Pending response, and set the description to: Northwind wants a 30-day payment term and a liability cap at 1x fees. Also add a note to the matter: Kesnavi to review by Friday.`

## Facts

- The agreement is a logistics services agreement on Northwind Freight's paper.
- Region: North America.
- Value: about 120,000 USD.
- There is no deadline.
- The user approves every change that the S2 message asks for.

## S1 Create the matter in chat

Open the AI Agent named `Ask Kes Anything` and start a chat. Send the S1 message.

Pass: the agent makes a matter, and a reply links to it. Write down that link and the matter's subject as the chat shows it.

## S2 Edit the matter in the same chat

Send the S2 message in the same chat.

Pass: the agent's last reply says it changed the matter. It does not have to name each change: S3 and S4 check the matter itself.

## S3 Find the matter on the board

Open the board named `AI-Aliens`. Search the board for a word from the subject that S1 wrote down, such as `Northwind`. Take a snapshot: the evidence must come from it.

Pass: the row for the matter from S1 shows the status `Pending response`.

Screenshot: `board-search`

## S4 Open the matter and check the description, value and note

Open the matter from that row.

Pass: the matter's description says that Northwind wants a 30-day payment term and a liability cap at 1x fees, and the matter shows a contract value of 150,000 in any number format.

Screenshot: `matter-details`

Then open the part of the matter that shows its notes.

Pass: a note says that Kesnavi is to review by Friday.

Screenshot: `matter-conversations`

The case's `matterUrl` is the URL of the matter page that S4 opens.
