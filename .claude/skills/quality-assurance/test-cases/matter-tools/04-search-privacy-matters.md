# Search matters by type and assignee through the AI Agent

needs: 03-create-privacy-matter-with-file

A user asks the AI Agent for every privacy matter assigned to one person. The reply must list each matching matter, including the one made today, and no other matter.

## Messages

- S2: `Can you show me all the privacy matters assigned to Grace Li?`

This case has no facts: a question from the agent fails S2.

## S1 List the expected matters on the board

Open the board named `AI-Aliens`. Show only the matters with the assignee `Grace Li` and the type `Privacy (Promoted)`. Remove any other filter, so that the board hides no matter because of its status. If the board has pages or loads more rows on scroll, go through all of them.

Pass: the rows include the matter from `03-create-privacy-matter-with-file`. Write down each row's link and subject. This is the expected list.

Screenshot: `expected-matters`

## S2 Ask the agent for the same matters

Open the AI Agent named `Ask Kes Anything` and start a new chat. Send the S2 message.

Pass: all of these are true.

- The reply lists the matter from `03-create-privacy-matter-with-file`.
- Each matter that the reply lists is on the expected list.
- The reply lists each matter on the expected list, unless it says that it shows only some of them.

Other people use this board. If the two lists are different, make the expected list again before you decide, and compare the reply with the new list.

As evidence, copy the reply's line for the matter from `03-create-privacy-matter-with-file`.
