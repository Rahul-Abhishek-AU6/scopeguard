# Research — Scopeguard

Date: 2026-10-29

## Selected problem

AI coding agents make it easy to produce a plausible patch that quietly edits the wrong part of a repository: generated files, deployment configuration, authentication paths, migrations, or files outside the task boundary. Reviewers must reconstruct that scope manually, often after a large agent-generated diff already exists.

**Scopeguard** will be a local, zero-dependency CLI that checks a Git diff against a small, reviewable `.scopeguard.yml` policy. It reports: changed paths, matching allow/deny rules, sensitive-path warnings, required test commands, and a machine-readable pass/fail result. It does not run unapproved commands or call a model/API.

## Demand signals

- Stack Overflow’s 2026 survey says daily AI coding-assistant use is common, while its analysis notes that code review, DevOps/SRE, security, and infrastructure are taking the downstream load. [Stack Overflow, Oct. 2026](https://stackoverflow.blog/2026/10/06/the-results-of-the-2026-developer-survey-are-here/); [analysis, May 2026](https://stackoverflow.blog/2026/05/21/coding-agents-are-giving-everyone-decision-fatigue)
- Stack Overflow’s 2025 AI survey identifies “almost right” output as the leading frustration (66%) and debugging AI-generated code as another major cost (45%). [Survey results](https://survey.stackoverflow.co/2025/ai)
- Sonar’s 2026 State of Code report says 96% of surveyed developers do not fully trust AI-generated code to be functionally correct. [Report](https://www.sonarsource.com/state-of-code-developer-survey-report.pdf)
- GitLab research reported review and validation, not code creation, as the main constraint for AI-assisted delivery. [Summary](https://www.techradar.com/pro/speed-without-control-is-a-liability-not-an-advantage-gitlab-study-reveals-ai-code-generation-is-outpacing-controls)

These signals point to an urgent developer workflow problem: cheap code generation amplifies the cost of deciding whether a patch stayed within its intended safety boundary.

## Target user and job

The first user is an individual developer or small team using Codex, Claude Code, Copilot, or another agent in a Git repository. Before opening a PR or accepting an agent’s changes, they want one command that answers: **did this patch touch forbidden or high-risk areas, and what explicit verification does this repository require?**

## Why this MVP is viable

- Python standard library plus the installed Git CLI are sufficient.
- A simple YAML-compatible policy subset can avoid a third-party YAML dependency: allow JSON syntax in `.scopeguard.json` for MVP, document YAML as future work.
- The policy is committed beside code, transparent in review, and requires no keys, network, telemetry, or hosted service.
- It can work in a dirty tree, staged changes, or a PR checkout using explicit Git ref arguments.

## Alternatives and gap

| Alternative | Useful for | Gap Scopeguard fills |
|---|---|---|
| CI / branch protection | Enforcing merged workflow | Often slow and post-push; does not give a local agent-scope receipt |
| Linting / SAST | Language and vulnerability findings | Does not express task-local allowed/denied paths or required evidence |
| AI code review | Natural-language commentary | Adds another model/trust surface; can be non-deterministic or paid |
| Handwritten PR template | Team communication | Easy to skip and does not inspect the actual diff |

## MVP acceptance criteria

1. `scopeguard check` reads changed Git paths and a committed JSON policy.
2. It exits non-zero when a denied path changes or an allowlist is violated.
3. It emits a human Markdown receipt and JSON result, with per-path rule explanations.
4. It shows required test commands as review evidence without executing them by default.
5. Tests cover clean failure, staged/working-tree diffs, glob matching, deny precedence, and output stability.

## Risks and boundaries

- It is a review gate, not security proof; policies can be incomplete.
- Glob behavior must be documented and deterministic.
- It must never treat a passing path policy as proof of functional correctness.
- No external publishing is authorized for this project yet.
