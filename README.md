# ai-landscape

A capture-to-publish pipeline for things you read, with the summarising step graded.

Save an article from the browser, have it summarised into a structured entry,
search the entries later, publish a digest from them. The part worth looking at
is the third file down: **the summariser is checked against its source**, because
everything downstream reads the summary and nobody rereads the article.

⚠️ **Status: this ran as a real practice from November 2025 to February 2026 —
31 entries and four published editions.**

**Parked June 2026.** Continuous landscape scanning is a discovery-stage input —
it earns its keep while the question is still *what to build*. The projects these
entries fed moved past that stage, and the tagging that made an entry findable had
nothing current to point at. The code and the schema outlived the practice, which
is why they are here and the entries are not. Three example entries stand in.

---

## Why the summariser is graded

`/capture` asks a model to compress an article into two or three sentences. That
step *is* the pipeline. A summary that quietly firms up a hedge or invents a
statistic is worse than no entry at all: it is confidently wrong, it is what you
will reread in six months, and nothing about it looks wrong.

Three failures, and they are not equally hard to catch:

| Failure | How it is caught |
|---|---|
| **Invented number** — a figure in the summary that is not in the source | **Deterministic.** No judgment required, so no model is asked |
| **Dropped hedge** — "suggests" became "shows"; "small sample" vanished | Model, then graded |
| **Inverted finding** — the summary says the opposite | Model, then graded |

Same split as everywhere else in this repo: **never ask a model a question that
has a right answer you can compute.**

```
$ python3 -m aijournal.evals

fixture                          expected               got                    ok
faithful                         ['—']                  ['—']                  ✓
invented-number                  ['invented_number']    ['invented_number']    ✓
dropped-hedge                    ['dropped_hedge']      ['—']                  ✗
inverted-finding                 ['inverted_finding']   ['—']                  ✗
compression-is-not-a-failure     ['—']                  ['—']                  ✓

agreement 3/5 = 60%   threshold 80%
```

That run uses a stub grader that finds nothing. It scores 60% — passing every
case with nothing to find and failing the rest. **That is what having no check
looks like**, and it is the number a real grader has to beat.

---

## The entry format, and why it has two sections

```markdown
---
date: 2026-01-15
projects: [measurement, tooling]
tags: [agents, evaluation]
source: https://…
---

# Title

What the source actually claims.

## Why it matters here

Why it was worth keeping.
```

The summary is what the source said. The second section is what you thought.
Collapsing them is how a knowledge base becomes a pile of link dumps: six months
later the summary is recoverable from the source, and **the only thing that was
ever worth keeping is the sentence you wrote yourself.**

`aijournal/validate.py` fails an entry that is missing it. An entry without that
section is a bookmark, and a bookmark did not need a file.

---

## What's here

| | |
|---|---|
| `extension/` | Chrome extension, Manifest V3. One click to save the current page. No network permissions — it writes to local storage only |
| `skills/capture/` | The `/capture` skill: fetch, summarise, tag, write, validate |
| `aijournal/faithfulness.py` | The grader — a deterministic number gate plus a model for the rest |
| `aijournal/validate.py` | Schema validation. Four fields, no YAML dependency |
| `aijournal/evals.py` | Grades the grader. Non-zero exit below threshold |
| `editions/` | Four published digests, Nov–Dec 2025 |
| `journal/` | Three example entries |

⚠️ **Honest about the seam:** the extension's manifest requests `activeTab` and
`storage` and nothing else, so it saves locally and `import` bridges to the
journal. It is two pieces with a manual step between them, not one system. Any
reviewer who opens `manifest.json` will see that; better to say it here.

## Quickstart

```bash
cp topics.example.yaml topics.yaml
python3 run_tests.py                    # 14 tests, no dependencies
python3 -m aijournal.evals              # no API key needed
python3 -m aijournal.validate journal/
```

No dependencies, standard library only. A tool that needs a virtualenv to save a
link is a tool nobody uses twice.

MIT.

---

The thinking behind this is at [aguedaschwartz.com/practice](https://aguedaschwartz.com/practice).
