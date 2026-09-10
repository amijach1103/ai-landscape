---
date: 2026-01-15
projects: [measurement, tooling]
tags: [agents, evaluation, reliability]
source: manual
---

# Example entry: agent reliability is measured at the wrong layer

Most agent evaluations report task success on a benchmark suite. The gap that
shows up in production is different: an agent that succeeds 95% of the time
fails differently each time, so the failures cannot be handled as a class.

## Why it matters here

This is the argument for grading the summariser in this repo rather than spot
checking it. An aggregate pass rate would hide the one failure that matters —
a confident summary of something the source never said.
