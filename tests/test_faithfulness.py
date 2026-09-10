"""The number gate. It runs with no model, so it is the part that can be tested
here; the judgment half is graded by aijournal.evals against the same fixtures."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aijournal.faithfulness import invented_numbers, dropped_all_hedges, grade

FIX = {f["id"]: f for f in json.load(open(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "fixtures", "faithfulness.json")))}


def test_catches_a_statistic_that_was_never_said():
    f = FIX["invented-number"]
    assert "35" in invented_numbers(f["source"], f["summary"])


def test_does_not_flag_a_number_the_source_states():
    f = FIX["faithful"]
    assert invented_numbers(f["source"], f["summary"]) == []


def test_formatting_is_not_a_difference():
    """1,200 and 1200 are the same claim. A gate that disagrees is noise, and a
    noisy gate gets switched off."""
    assert invented_numbers("We saw 1,200 signups and 14% growth.",
                            "1200 signups, 14 percent growth.") == []


def test_notices_when_every_hedge_disappears():
    f = FIX["dropped-hedge"]
    assert dropped_all_hedges(f["source"], f["summary"]) is True


def test_does_not_fire_when_hedges_survive():
    f = FIX["faithful"]
    assert dropped_all_hedges(f["source"], f["summary"]) is False


def test_grade_runs_with_no_model_at_all():
    """The gate alone is useful. Requiring an API key to check your own notes is
    how a tool stops being used."""
    r = grade(FIX["invented-number"]["source"], FIX["invented-number"]["summary"])
    assert r.faithful is False
    assert r.findings[0].kind == "invented_number"


def test_faithful_summary_passes_the_gate():
    r = grade(FIX["faithful"]["source"], FIX["faithful"]["summary"])
    assert r.faithful is True
