from .policy import matches

def evaluate(paths, policy):
    changed, violations, warnings = [], [], []
    for path in paths:
        denied = [p for p in policy["deny"] if matches(path, p)]
        allowed = [p for p in policy["allow"] if matches(path, p)]
        sensitive = [p for p in policy["sensitive_paths"] if matches(path, p)]
        if denied:
            decision, rules = "denied", denied
            violations.append({"path": path, "decision": decision, "rules": rules})
        elif policy["allow"] and not allowed:
            decision, rules = "outside_allowlist", []
            violations.append({"path": path, "decision": decision, "rules": rules})
        else:
            decision, rules = "allowed", allowed
        entry = {"path": path, "decision": decision, "rules": rules}
        changed.append(entry)
        if sensitive:
            warnings.append({"path": path, "rules": sensitive, "message": "sensitive path: human review recommended"})
    return changed, violations, warnings
