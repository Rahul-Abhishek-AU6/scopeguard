import json
from pathlib import Path

def write(output, mode, changed, violations, warnings, required_tests):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    data = {"status": "pass" if not violations else "fail", "mode": mode, "changed_paths": changed,
            "violations": violations, "warnings": warnings, "required_tests": required_tests}
    (output / "scopeguard-result.json").write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    lines = ["# Scopeguard receipt", "", f"- Status: **{data['status']}**", f"- Mode: {mode}", "", "## Changed paths", ""]
    lines += [f"- `{x['path']}` — {x['decision']}" for x in changed] or ["- None"]
    lines += ["", "## Violations", ""] + ([f"- `{x['path']}` — {x['decision']}" for x in violations] or ["- None"])
    lines += ["", "## Warnings", ""] + ([f"- `{x['path']}` — {x['message']}" for x in warnings] or ["- None"])
    lines += ["", "## Required tests (not executed)", ""] + ([f"- `{x}`" for x in required_tests] or ["- None"])
    lines += ["", "Scopeguard validates declared path scope only; it does not prove correctness or security."]
    (output / "scopeguard-receipt.md").write_text("\n".join(lines) + "\n")
    return data
