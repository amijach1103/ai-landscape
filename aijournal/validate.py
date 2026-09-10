"""
Entry schema validation.

Thirty-one entries written by hand over four months drift. A field gets renamed,
a date format slips, a list becomes a string. None of it fails loudly; it just
means the entry stops being findable, which is the only thing an entry is for.

    python3 -m aijournal.validate journal/            # whole directory
    python3 -m aijournal.validate journal/foo.md      # one file
"""
import re, sys, datetime
from pathlib import Path

REQUIRED = ("date", "projects", "tags", "source")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
FILENAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def parse_frontmatter(text):
    """Minimal YAML-ish frontmatter reader. Deliberately not a YAML dependency:
    the schema is four scalar-or-list fields and a real parser would be the only
    thing in this repo you had to install."""
    if not text.startswith("---"):
        raise ValueError("no frontmatter block")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("frontmatter block is not closed")
    out = {}
    for line in text[3:end].strip().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"frontmatter line is not key: value → {line.strip()!r}")
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        out[k.strip()] = v
    return out, text[end + 4:]


def check(path: Path, known_topics=None):
    """Return a list of problems. Empty list means the entry is well formed."""
    problems = []
    if not FILENAME.match(path.name):
        problems.append(f"filename should be YYYY-MM-DD-slug.md, got {path.name!r}")
    try:
        fm, body = parse_frontmatter(path.read_text())
    except ValueError as e:
        return [str(e)]

    for field in REQUIRED:
        if field not in fm:
            problems.append(f"missing required field {field!r}")

    d = fm.get("date", "")
    if isinstance(d, str) and d and not DATE.match(d):
        problems.append(f"date should be YYYY-MM-DD, got {d!r}")
    elif DATE.match(str(d)):
        try:
            datetime.date.fromisoformat(d)
        except ValueError:
            problems.append(f"date {d!r} is not a real date")
        if not path.name.startswith(d):
            problems.append(f"date {d!r} does not match the filename")

    for field in ("projects", "tags"):
        if field in fm and not isinstance(fm[field], list):
            problems.append(f"{field} should be a list in [brackets], got {fm[field]!r}")

    if known_topics is not None:
        for p in (fm.get("projects") or []):
            if p not in known_topics:
                problems.append(f"project {p!r} is not in topics.yaml")

    # The entry's whole value is the second section. An entry without it is a
    # bookmark, and a bookmark did not need a file.
    if "## Why it matters here" not in body:
        problems.append("missing the 'Why it matters here' section")
    return problems


def main(argv):
    target = Path(argv[1]) if len(argv) > 1 else Path("journal")
    files = sorted(target.glob("*.md")) if target.is_dir() else [target]
    if not files:
        print(f"no entries found at {target}")
        return 1
    bad = 0
    for f in files:
        problems = check(f)
        if problems:
            bad += 1
            print(f"✗ {f.name}")
            for p in problems:
                print(f"    {p}")
        else:
            print(f"✓ {f.name}")
    print(f"\n{len(files) - bad}/{len(files)} entries valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
