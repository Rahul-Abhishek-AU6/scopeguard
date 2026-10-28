# Independent verification

Status: **passed** — 2026-10-29.

## Commands and results

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Result: 3 tests passed.

The suite verifies that allowed changes pass while declared required-test commands are not executed; deny rules take precedence over allow rules; and sensitive-path changes emit warnings.

```sh
PYTHONPATH=src python3 -m scopeguard check --policy .scopeguard.json --output-dir reports/qa-smoke
```

Result: completed successfully and produced the stable Markdown/JSON receipt in `reports/qa-smoke/`. The working tree had no changed paths at verification time, so the receipt correctly reports a passing empty change set and preserves the declared required test as unexecuted evidence.

## Conclusion

Scopeguard meets the planned local-only MVP acceptance criteria. It must continue to be described as a path-policy receipt, not a security or correctness guarantee.
