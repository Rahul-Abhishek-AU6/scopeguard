import json, os, subprocess, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
ENV = {**os.environ, "PYTHONPATH": str(ROOT / "src")}

class ScopeguardTests(unittest.TestCase):
    def fixture(self, path, policy):
        subprocess.run(["git", "init", "-q"], cwd=path, check=True); subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=path, check=True); subprocess.run(["git", "config", "user.name", "Test"], cwd=path, check=True)
        (path / ".scopeguard.json").write_text(json.dumps(policy)); (path / "src").mkdir(); (path / "src/app.py").write_text("one\n")
        subprocess.run(["git", "add", "."], cwd=path, check=True); subprocess.run(["git", "commit", "-qm", "base"], cwd=path, check=True); (path / "src/app.py").write_text("two\n")
    def invoke(self, path):
        return subprocess.run(["python3", "-m", "scopeguard", "check", "--policy", ".scopeguard.json", "--output-dir", "evidence"], cwd=path, env=ENV, text=True, capture_output=True)
    def test_allowed_and_required_tests_not_run(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); self.fixture(p,{"allow":["src/**"],"required_tests":["false"]}); result=self.invoke(p)
            self.assertEqual(result.returncode,0); self.assertIn("not executed",(p/"evidence/scopeguard-receipt.md").read_text())
    def test_deny_wins(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); self.fixture(p,{"allow":["**"],"deny":["src/**"]}); result=self.invoke(p)
            self.assertEqual(result.returncode,1); self.assertIn("denied",(p/"evidence/scopeguard-result.json").read_text())
    def test_sensitive_warning(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); self.fixture(p,{"allow":["src/**"],"sensitive_paths":["src/**"]}); result=self.invoke(p)
            self.assertEqual(result.returncode,0); self.assertIn("sensitive path",(p/"evidence/scopeguard-result.json").read_text())
