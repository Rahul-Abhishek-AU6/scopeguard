import json
from pathlib import PurePosixPath

def load(path):
    try:
        data = json.loads(open(path).read())
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid policy: {exc}")
    if not isinstance(data, dict): raise ValueError("invalid policy: expected JSON object")
    out = {}
    for key in ("allow", "deny", "sensitive_paths", "required_tests"):
        value = data.get(key, [])
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            raise ValueError(f"invalid policy: {key} must be a string array")
        out[key] = value
    return out

def matches(path, pattern):
    # pathlib's segment-aware match supports the policy's recursive patterns on Python 3.10+.
    return PurePosixPath(path).match(pattern)
