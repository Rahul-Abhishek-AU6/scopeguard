# Implementation plan — Scopeguard

## Outcome

Deliver a zero-dependency Python CLI that inspects a local Git diff against a committed, explicit JSON policy and writes a human-readable Markdown receipt plus a stable JSON result. It is deterministic review evidence, never a security verdict or an AI model.

## User flow

```sh
PYTHONPATH=src python -m scopeguard check --policy .scopeguard.json --output-dir evidence
```

The command obtains changed paths from the working tree by default, evaluates them against the policy, prints a concise result, writes `scopeguard-receipt.md` and `scopeguard-result.json`, and returns zero only when all policy checks pass. `--staged` switches to the staged diff. Required test commands are displayed as declared evidence, never executed by Scopeguard.

## Policy schema

Use JSON only in the MVP to preserve the no-dependency guarantee:

```json
{
  "allow": ["src/**", "tests/**", "README.md"],
  "deny": [".github/workflows/**", "infra/**", "migrations/**"],
  "required_tests": ["python -m unittest discover -s tests -v"],
  "sensitive_paths": ["auth/**", "config/**", ".env*"]
}
```

- Empty or omitted `allow` permits all non-denied paths.
- `deny` always wins over `allow`.
- `sensitive_paths` produces a visible warning, not failure, unless also denied.
- Matching is repository-relative POSIX path matching with `*` for one path segment and `**` for recursive paths. Normalize paths and reject paths outside the repository.

## Architecture

```text
src/scopeguard/
  __main__.py     argparse entry point and exit-code mapping
  git.py          Git repository/diff-path adapter
  policy.py       JSON parsing, validation, path matcher
  evaluate.py     deterministic per-path policy decisions
  render.py       stable Markdown and JSON receipt writers
tests/
  test_scopeguard.py  unit and temp-Git integration tests
```

`git diff --name-only` supplies paths. For an untracked/clean-tree edge case, report an empty receipt rather than manufacturing changes. A non-Git working directory or invalid JSON policy is a clear non-zero error with no output files claimed as successful.

## Receipt contract

JSON keys are stable and sorted: `status`, `mode`, `changed_paths`, `violations`, `warnings`, `required_tests`. Each changed path includes `path`, `decision` (`allowed`, `denied`, `outside_allowlist`), and matching rule(s). Markdown contains the same facts, a required-tests section labelled **not executed**, and the explicit limitation that pass status only reflects declared scope policy.

## Security and privacy constraints

- No network requests, API keys, telemetry, subprocess shell evaluation, or dynamically executed policy content.
- Invoke Git through argument arrays, never shell strings.
- Do not execute `required_tests`; they are display-only evidence.
- Avoid including diff contents in reports, so receipts do not leak source or secrets.
- Treat JSON parse errors and Git errors as actionable local errors.

## Build tasks

1. Create package/CLI with `check`, `--policy`, `--output-dir`, and `--staged`.
2. Implement strict policy validation and deterministic recursive glob matcher.
3. Add Git path reader and evaluator with deny precedence.
4. Render Markdown/JSON receipts with a documented result schema.
5. Add README quick start, example policy, limitations, and local test command.
6. Add unit and temporary Git-repository integration tests.

## Acceptance test matrix

| Case | Expected result |
|---|---|
| Allowed `src/app.py` change | exit 0; allowed path in both receipts |
| Denied `.github/workflows/release.yml` change | non-zero; denied rule and path named |
| Changed path outside non-empty allowlist | non-zero; `outside_allowlist` decision |
| Path matching both allow and deny | non-zero; deny wins |
| `auth/session.py` allowed but sensitive | exit 0; warning appears |
| Staged-only change with `--staged` | staged path is reported, unstaged path omitted |
| Required tests policy field | rendered as “not executed”; no subprocess call |
| Invalid policy / non-Git directory | non-zero actionable error |
| Repeated same fixture | byte-stable JSON output |

## Verification command

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The build worker must run this command and retain a safe smoke receipt made from a fixture repository before handing off to independent QA.
