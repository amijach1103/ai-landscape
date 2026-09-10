"""
Grade the grader.

The number gate is tested in tests/. The judgment half — dropped hedges and
inverted findings — needs a model, so it is graded here against the same
fixtures, with a threshold and a non-zero exit.

    python3 -m aijournal.evals           # stub, no key, checks the harness
    python3 -m aijournal.evals --live    # supply a real completion function

A summariser nobody grades drifts silently: it keeps producing fluent summaries
long after it stopped producing faithful ones, and nothing in the output says so.
"""
import json, sys
from pathlib import Path
from aijournal.faithfulness import grade

THRESHOLD = 0.80
ROOT = Path(__file__).resolve().parent.parent


def stub(prompt: str) -> str:
    """Finds nothing, ever. Scores exactly as well as having no check at all,
    which is the comparison worth seeing."""
    return json.dumps({"findings": []})


def run(complete=stub):
    fixtures = json.loads((ROOT / "fixtures" / "faithfulness.json").read_text())
    rows, agree = [], 0
    for fx in fixtures:
        report = grade(fx["source"], fx["summary"], complete)
        got = sorted({f.kind for f in report.findings})
        want = sorted(set(fx["expect"]))
        # invented_number is the gate's name for what the model calls invented_claim
        ok = got == want or (want == ["invented_number"] and "invented_number" in got)
        agree += ok
        rows.append((fx["id"], want, got, ok))

    print(f"\n{'fixture':<32} {'expected':<22} {'got':<22} ok")
    print("─" * 84)
    for fid, want, got, ok in rows:
        print(f"{fid:<32} {str(want or ['—']):<22} {str(got or ['—']):<22} {'✓' if ok else '✗'}")
    rate = agree / len(rows) if rows else 0
    print(f"\nagreement {agree}/{len(rows)} = {rate:.0%}   threshold {THRESHOLD:.0%}")
    return rate


if __name__ == "__main__":
    rate = run()
    if "--live" not in sys.argv:
        print("\n(stub grader: finds nothing. It passes the cases with nothing to find and "
              "fails the rest, which is what having no check looks like. Use --live to grade "
              "a real one.)")
        sys.exit(0)
    sys.exit(0 if rate >= THRESHOLD else 1)
