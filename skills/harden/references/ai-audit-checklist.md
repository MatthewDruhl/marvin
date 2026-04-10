<!-- PHASE GATE: Do not read before Scope 2. Load only after completing Scope 1 findings. -->

# AI Audit Checklist

Detailed checks for Scope 2 (AI-Specific Gaps). Read this file before evaluating the AI scope.

> Core checks (1–5) are defined in SKILL.md Scope 2. Start with those, then continue below.

## Extended Checks

### 6. Tool Use Validation
**What to look for:** Are MCP tool results or external tool outputs trusted blindly? Is output from tools sanitized before use?
**Example finding:** Tool returns user-controlled data that gets interpolated into a prompt or executed as code without validation.
**Severity guidance:** High if tool output influences prompts or code execution. Medium if tool output is only displayed.

### 7. Context Window Stuffing / Data Exfiltration
**What to look for:** Can user input inflate context to leak data or cause unexpected behavior? Can crafted input cause the model to echo back system prompts or other context?
**Example finding:** User-provided document gets loaded into context alongside API keys from config files.
**Severity guidance:** Critical if secrets could leak. High if PII could leak. Medium if only non-sensitive data.

### 8. Agent Permission Boundaries
**What to look for:** Are spawned agents or sub-agents scoped appropriately? Can they escalate privileges, access files outside their scope, or perform actions the parent didn't authorize?
**Example finding:** Sub-agent inherits full file system access when it only needs to read one directory.
**Severity guidance:** High if agents can write/delete outside scope. Medium if agents can read outside scope.

### 9. Prompt / System Prompt Leakage
**What to look for:** Can users extract system prompts through crafted inputs? Are system instructions exposed in error messages, logs, or responses?
**Example finding:** Error handler includes the full system prompt in the error message sent to the user.
**Severity guidance:** Medium in most cases. High if the system prompt contains secrets or reveals security architecture.

### 10. RAG Poisoning Risks
**What to look for:** If the system uses retrieval-augmented generation, can poisoned or adversarial documents influence outputs? Are retrieved documents from trusted sources only?
**Example finding:** RAG pipeline indexes user-uploaded documents alongside trusted internal docs with no source distinction.
**Severity guidance:** High if RAG influences decisions (code generation, access control). Medium if RAG only influences informational responses.

### 11. Cost Control
**What to look for:** Are there limits on API calls, token usage, or agent loops? Can a single request trigger unbounded API spend?
**Example finding:** Retry logic has no max attempts — a failing API call loops indefinitely, burning tokens.
**Severity guidance:** High if unbounded spend is possible. Medium if limits exist but are generous. Low if theoretical only.

### 12. Happy Path Bias
**What to look for:** Does AI-generated code only handle the success path? Are error cases, timeouts, and edge cases covered?
**Research context:** Studies show AI introduces logic errors 75% more frequently than human-written code, and error handling is 2x worse.
**Example finding:** AI-generated function processes valid input correctly but silently returns None on malformed input.
**Severity guidance:** High for code touching money, auth, or data integrity. Medium for internal tooling.

### 13. Confidence Without Correctness
**What to look for:** Does the system verify AI outputs before acting on them, or trust plausible-sounding responses? Are there sanity checks on AI-generated values?
**Example finding:** AI generates a SQL query that is syntactically valid but semantically wrong — no validation before execution.
**Severity guidance:** High if AI outputs drive automated actions. Medium if a human reviews before acting.

### 14. Library Hallucination
**What to look for:** Does AI-generated code reference APIs, functions, or libraries that don't exist? Are imports verified?
**Example finding:** Code imports `from utils import sanitize_html` but no such function exists in the project or its dependencies.
**Severity guidance:** High if in production code paths. Low if in test or scaffold code.

### 15. Pattern Attraction / Over-Abstraction
**What to look for:** Does AI-generated code use over-engineered patterns (factory of factories, unnecessary abstractions) where simpler code would work? Does the architecture reflect actual requirements or AI training patterns?
**Example finding:** A simple config loader wrapped in a Strategy pattern with a Factory and an Abstract Base Class for one implementation.
**Severity guidance:** Low in most cases. Medium if the abstraction obscures bugs or makes maintenance harder.

### 16. Token Efficiency
**What to look for:** Are prompts, skill instructions, and file I/O patterns minimizing token consumption? Look for: duplicate instruction files loaded together, sequential reads that could be parallel, verbose templates the model doesn't need, conversation re-scanning when incremental summaries exist, interactive pauses that could be combined into a single prompt.
**Example finding:** A skill loads a 138-line SKILL.md and a 75-line command file with overlapping instructions. Reads 5 state files sequentially instead of in one parallel batch. Re-summarizes the full conversation even when checkpoints exist.
**Severity guidance:** Medium if token waste is consistent across frequent operations (daily skills, session management). Low for rarely-used skills. Consider cumulative cost — a 40% overhead on a skill run 2x/day adds up fast.
**Always-loaded files:** Check CLAUDE.md, system prompts, and other files loaded every session. Content that could live in on-demand skill files (setup instructions, reference tables, detailed procedures) is a per-session tax. Only behavioral guidance and core rules belong in always-loaded files.

### 17. AI-to-Code Offload Opportunities
**What to look for:** Tasks currently performed by multi-step AI reasoning that a script could handle — codebase exploration done turn-by-turn instead of via a recon script, structured data collection (file inventories, git history, dependency graphs) forcing repeated tool calls, post-AI actions (filing issues, updating files) done manually via copy-paste, repeated parsing of the same files across audit phases.
**Example finding:** An audit skill reads 15 files individually to build a picture of the repo. A 50-line recon script could produce the same inventory in one context injection, reducing input tokens by 40-60%.
**Severity guidance:** Medium if the pattern recurs across frequent skill runs. Low for one-off or rarely used skills.
**Tier check:** Not all offloading requires a script. Evaluate which tier each step needs:
- Script — structured data, math, formatting, file I/O
- Cheap model (haiku-class) — pattern scanning, candidate flagging, output formatting
- Full model — judgment calls, ambiguous findings, severity calibration, steel-manning

Flag any step using a full model where a cheaper tier produces equivalent output.

---

*Extended AI checks inspired by research on AI code quality and the [devils-advocate skill](https://github.com/notmanas/claude-code-skills/tree/main/skills/devils-advocate) by notmanas.*
