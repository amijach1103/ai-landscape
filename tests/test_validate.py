import sys, os, tempfile
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aijournal.validate import check, parse_frontmatter

GOOD = """---
date: 2026-01-15
projects: [general, tooling]
tags: [agents, evaluation]
source: https://example.com/a
---

# A title

Two sentences about what the source actually claims.

## Why it matters here

One sentence about why it was worth keeping.
"""

def _write(tmp, name, text):
    p = Path(tmp) / name
    p.write_text(text)
    return p

def test_a_well_formed_entry_passes():
    with tempfile.TemporaryDirectory() as t:
        assert check(_write(t, "2026-01-15-a-title.md", GOOD)) == []

def test_catches_a_date_that_contradicts_the_filename():
    """The failure that makes an entry unfindable by the one thing everyone
    sorts on."""
    with tempfile.TemporaryDirectory() as t:
        p = _write(t, "2026-01-20-a-title.md", GOOD)
        assert any("does not match the filename" in x for x in check(p))

def test_catches_a_list_field_written_as_a_string():
    with tempfile.TemporaryDirectory() as t:
        bad = GOOD.replace("projects: [general, tooling]", "projects: general")
        p = _write(t, "2026-01-15-a-title.md", bad)
        assert any("should be a list" in x for x in check(p))

def test_catches_a_missing_required_field():
    with tempfile.TemporaryDirectory() as t:
        bad = GOOD.replace("source: https://example.com/a\n", "")
        p = _write(t, "2026-01-15-a-title.md", bad)
        assert any("missing required field 'source'" in x for x in check(p))

def test_catches_an_entry_that_is_only_a_bookmark():
    """No 'Why it matters here' means nothing was thought, and the summary is
    retrievable from the source anyway."""
    with tempfile.TemporaryDirectory() as t:
        bad = GOOD.replace("## Why it matters here\n\nOne sentence about why it was worth keeping.\n", "")
        p = _write(t, "2026-01-15-a-title.md", bad)
        assert any("Why it matters here" in x for x in check(p))

def test_rejects_a_project_not_in_the_topic_list():
    with tempfile.TemporaryDirectory() as t:
        p = _write(t, "2026-01-15-a-title.md", GOOD)
        assert any("not in topics.yaml" in x for x in check(p, known_topics={"general"}))

def test_frontmatter_must_be_closed():
    with tempfile.TemporaryDirectory() as t:
        p = _write(t, "2026-01-15-a-title.md", "---\ndate: 2026-01-15\n\n# no close\n")
        assert any("not closed" in x for x in check(p))
