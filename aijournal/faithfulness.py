"""
Grade the summariser.

`/capture` asks a model to compress an article into two or three sentences. That
step is the whole pipeline: everything downstream searches the summary, not the
source. A summary that quietly drops a hedge or firms up a finding is worse than
no entry, because it is confidently wrong and it is the version you will reread.

Three failures, and they are not equally hard to catch:

  invented number   — deterministic. A figure in the summary that is not in the
                      source is wrong, and no judgment is required to see it.
  dropped hedge     — judgment. "suggests" became "shows"; "in a small sample"
                      vanished.
  inverted finding  — judgment. The summary says the opposite of the source.

So the number check is a gate and the other two go to a model, for the same
reason the gates and the scorer are separate everywhere else: never ask a model
a question that has a right answer you can compute.
"""
import json, re
from dataclasses import dataclass, field

NUMBER = re.compile(r"\b\d[\d,]*\.?\d*\s?%?\b")
HEDGES = ("suggest", "may ", "might ", "could ", "appears", "associated with",
          "correlat", "preliminary", "small sample", "limited", "in one study",
          "self-reported", "not statistically significant")


@dataclass
class Finding:
    kind: str
    detail: str


@dataclass
class Report:
    findings: list = field(default_factory=list)

    @property
    def faithful(self) -> bool:
        return not self.findings


# ── the gate ──────────────────────────────────────────────────────────────────

def _numbers(text):
    return {m.group().strip().rstrip("%").replace(",", "") for m in NUMBER.finditer(text or "")}


def invented_numbers(source: str, summary: str):
    """Figures asserted in the summary that do not appear in the source.

    Deliberately strict about digits and loose about formatting: 1,200 and 1200
    are the same claim, 12% and 12 are the same digits. A false positive here is
    cheap to dismiss; a missed invented statistic is not.
    """
    return sorted(_numbers(summary) - _numbers(source))


def dropped_all_hedges(source: str, summary: str) -> bool:
    """True when the source hedges throughout and the summary hedges nowhere.

    A signal, not a verdict — a summary can legitimately drop one qualifier. The
    model decides; this only says the question is worth asking.
    """
    s, m = source.lower(), summary.lower()
    return any(h in s for h in HEDGES) and not any(h in m for h in HEDGES)


# ── the judgment ──────────────────────────────────────────────────────────────

PROMPT = """Compare a summary against its source.

Report ONLY these failures:
- "dropped_hedge": the source qualifies a claim and the summary states it flatly
- "inverted_finding": the summary asserts something the source contradicts
- "invented_claim": the summary asserts something with no basis in the source

Compression is not a failure. Leaving material out is not a failure. Changing
how certain a claim is, is a failure.

SOURCE
{source}

SUMMARY
{summary}

Return JSON only:
{{"findings": [{{"kind": "...", "detail": "<the specific words>"}}]}}
"""


def parse(raw: str) -> Report:
    m = re.search(r"\{.*\}", raw or "", re.S)
    if not m:
        raise ValueError(f"no JSON object in response: {(raw or '')[:120]!r}")
    obj = json.loads(m.group())
    return Report([Finding(str(f.get("kind", "")), str(f.get("detail", "")))
                   for f in obj.get("findings", [])])


def grade(source: str, summary: str, complete=None) -> Report:
    """Run the gate, then the model if one is supplied.

    Works with no model at all: the number gate alone catches the failure that
    matters most in a knowledge base, which is a statistic that was never said.
    """
    report = Report()
    for n in invented_numbers(source, summary):
        report.findings.append(Finding("invented_number", f"{n} does not appear in the source"))
    if complete is None:
        return report
    model = parse(complete(PROMPT.format(source=source[:6000], summary=summary)))
    report.findings.extend(model.findings)
    return report
