#!/usr/bin/env python3
"""Run every test with no test framework installed. Standard library only."""
import importlib.util, sys, traceback, pathlib
passed = failed = 0
for path in sorted(pathlib.Path("tests").glob("test_*.py")):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    print(f"\n{path.name}")
    for name, fn in vars(mod).items():
        if name.startswith("test_") and callable(fn):
            try:
                fn(); print(f"  PASS  {name}"); passed += 1
            except Exception as e:
                print(f"  FAIL  {name}  ({type(e).__name__})")
                traceback.print_exc(limit=1); failed += 1
print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
