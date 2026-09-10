---
name: capture
description: Create a journal entry from a URL or from notes
user_invocable: true
---

# /capture

Turn a thing you read into a structured, searchable entry.

## Usage

- `/capture [URL]` — fetch the article, summarise it, write a tagged entry
- `/capture` — no URL: prompt for topic and notes, write a freeform entry

## Steps

1. **If a URL is given**, fetch and read it. Extract the title, the publication
   date, and the findings. Summarise in two or three sentences.

   ⛔ **Summarise, do not editorialise.** Every hedge in the source survives into
   the summary. "Suggests" does not become "shows"; "in a small sample" does not
   get dropped; no number appears that is not in the source.
   → `aijournal/faithfulness.py` grades exactly these three failures.

2. **Tag it.** Read the project list from `topics.yaml`. Match on what the entry
   is about, not on keyword overlap with the topic name.
   ⛔ Do not invent a project that is not in `topics.yaml`. Use `general`.

3. **Slug** from the title: lowercase, hyphens, six words maximum.

4. **Write** `journal/YYYY-MM-DD-slug.md`:

```markdown
---
date: YYYY-MM-DD
projects: [matched topics from topics.yaml]
tags: [3-5 topic tags]
source: URL, or "manual"
---

# Title

Two or three sentences: what it is, and what is actually claimed.

## Why it matters here

One or two sentences connecting it to the tagged topics. This is the part
future-you searches for, so write the connection, not a second summary.
```

5. **Validate** before finishing: `python3 -m aijournal.validate journal/<file>`.
   A malformed entry is worse than no entry — it will not be found again.

6. Confirm the filename.

## Why the entry has two sections

The summary is what the source said. "Why it matters here" is what you thought.
Collapsing them is how a personal knowledge base becomes a pile of link dumps:
six months later the summary is retrievable from the source, and the only thing
that was ever worth keeping is the sentence you wrote yourself.
