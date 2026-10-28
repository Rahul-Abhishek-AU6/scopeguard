import subprocess

def changed_paths(staged=False):
    command = ["git", "diff", "--name-only"] + (["--cached"] if staged else [])
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "not a Git repository")
    paths = [p for p in result.stdout.splitlines() if p and not p.startswith("../") and "/../" not in p]
    return sorted(set(paths))
