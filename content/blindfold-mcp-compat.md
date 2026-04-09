# Blindfold MCP Compatibility Analysis

**Date:** 2026-04-08
**Branch:** test/blindfold-original
**Verdict:** Incompatible (MCP server launches are outside Blindfold's hook scope)

---

## How MCP Servers Are Configured in Marvin

The `.mcp.json` file defines MCP servers that Claude Code launches directly:

```json
{
  "mcpServers": {
    "google-workspace": {
      "type": "stdio",
      "command": "npx",
      "args": ["dotenv-cli", "-e", ".env", "--", "uvx", "workspace-mcp", "--tools", "gmail", "calendar"],
      "env": {}
    }
  }
}
```

Secrets (OAuth tokens, client IDs) live in `.env` and are loaded by `dotenv-cli` at server startup. The MCP server process then holds those secrets in its environment for its entire lifetime.

## How Blindfold Hooks Work

Blindfold registers two hook types in `hooks.json`:

1. **PreToolUse (Bash, Read)** -- `secret-guard.sh` intercepts Bash commands and Read file paths before execution. On macOS, it wraps Bash commands in `sandbox-exec` to block keychain access.
2. **PostToolUse (Bash)** -- `secret-redact.sh` scans Bash output for leaked secret values and injects a system warning if found.

Both hooks operate on Claude Code's **tool calls** -- specifically the `Bash` and `Read` tools.

## Why MCP Server Launches Are Not Interceptable

MCP servers are **not launched through tool calls**. Claude Code starts MCP servers as child processes during initialization, based on the `.mcp.json` configuration. This happens:

- Before any conversation begins
- Outside the tool-use hook lifecycle
- As a direct process spawn by the Claude Code runtime

Since Blindfold hooks only fire on `PreToolUse` and `PostToolUse` events for `Bash` and `Read` tools, they have **no visibility** into MCP server startup.

### What this means concretely:

| Scenario | Blindfold Coverage |
|----------|-------------------|
| Claude runs `cat .env` via Bash | Covered -- sandbox blocks or redact catches it |
| Claude reads `.env` via Read tool | Covered -- secret-guard can block the path |
| Claude Code launches MCP server with `dotenv-cli -e .env` | NOT covered -- no hook fires |
| MCP server holds secrets in its process environment | NOT covered -- secrets live in memory |
| Claude calls an MCP tool that returns data | NOT covered -- no PostToolUse hook for MCP tools |

## Could `secret-exec.sh` Template Substitution Work for MCP?

`secret-exec.sh` resolves `{{PLACEHOLDER}}` tokens in a command string by fetching secrets from the keychain, injecting them as environment variables, and redacting the output. In theory, `.mcp.json` could use this pattern:

```json
{
  "env": {
    "GOOGLE_CLIENT_ID": "{{GOOGLE_CLIENT_ID}}",
    "GOOGLE_CLIENT_SECRET": "{{GOOGLE_CLIENT_SECRET}}"
  }
}
```

**This does not work** because:

1. `.mcp.json` is parsed by Claude Code's runtime, not by a shell. The `{{}}` syntax has no meaning to the MCP config parser.
2. There is no hook point to intercept and transform the MCP config before server launch.
3. Even if the env vars were resolved, the MCP server process would hold plaintext secrets in its environment -- Blindfold has no way to sandbox or monitor MCP server processes.

## What Adaptation Would Be Needed

To make Blindfold compatible with MCP servers, one of these approaches would be needed:

### Option A: MCP Launch Hooks (requires Claude Code changes)
Claude Code would need to expose a hook point for MCP server launches (e.g., `PreMcpServerStart`). Blindfold could then:
- Resolve `{{SECRET}}` placeholders in env vars
- Inject secrets into the MCP server's environment at launch time
- Apply sandboxing to the MCP server process

This is the cleanest solution but requires upstream Claude Code support.

### Option B: Wrapper Script in `.mcp.json`
Instead of launching the MCP server directly, use a wrapper:

```json
{
  "command": "bash",
  "args": ["path/to/mcp-wrapper.sh", "uvx", "workspace-mcp", "--tools", "gmail", "calendar"]
}
```

Where `mcp-wrapper.sh` would:
1. Read secrets from the keychain using Blindfold's `lib.sh`
2. Export them as environment variables
3. `exec` the actual MCP server command

This removes the need for `.env` files entirely. The wrapper would be a Blindfold-provided script. **This is feasible today** but requires:
- A new `mcp-wrapper.sh` script in Blindfold
- Users to restructure their `.mcp.json` to use the wrapper
- The wrapper to handle the secret-to-env-var mapping (a config file or naming convention)

### Option C: Keep Current `.env` Approach (status quo)
Accept that MCP secrets are outside Blindfold's scope. Continue using `dotenv-cli` with `.env` files for MCP servers, and rely on Blindfold only for protecting secrets accessed through Bash/Read tools. This is the current reality.

## Recommendation

**Short term:** Option C (status quo). MCP server secrets via `.env` + `dotenv-cli` work fine and are already protected by `.gitignore`. Blindfold protects against the LLM reading/leaking those secrets through tool calls, which is its primary threat model.

**Medium term:** Option B (wrapper script). This would let MCP servers pull secrets from the keychain instead of `.env` files, eliminating the flat-file secret risk entirely. This is a natural extension of Blindfold and could be proposed as a feature.

**Long term:** Option A (Claude Code hook support). This would be the most elegant solution but depends on Anthropic adding MCP launch hooks to Claude Code.
