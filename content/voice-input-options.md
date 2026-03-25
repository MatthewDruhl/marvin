# Voice Input for Claude Code on macOS

**Added:** 2026-03-09
**Status:** Research complete, not yet implemented

---

## 1. Claude Code Native `/voice` (Built-in)
**Cost:** Free | **Status:** Rolling out (started Mar 3, 2026 — ~5% of users)

- Type `/voice` to toggle on, hold **Space** to speak
- No setup required
- Check availability: type `/voice` — if available, you'll see it

---

## 2. Superwhisper
**Cost:** $9.99/month or $99/year (free trial) | **Install:** `brew install --cask superwhisper`

- Offline voice-to-text built on whisper.cpp
- Custom modes for code dictation, understands programming terminology
- Works in any app including terminal
- Privacy-first (no data leaves your Mac)

---

## 3. Wispr Flow
**Cost:** Free tier, Pro $10/month | **Install:** [wisprflow.ai](https://wisprflow.ai)

- AI dictation with auto-editing — converts speech to polished text
- Native IDE extensions for Cursor, Windsurf, Replit (works system-wide too)
- Learns programming terminology via personal dictionary
- SOC 2 Type II + HIPAA compliant

---

## 4. VoiceMode MCP Server
**Cost:** Free (open source) | **Install:** `claude mcp add --scope user voicemode -- uvx --refresh voice-mode`

- Adds voice mode to Claude Code as an MCP server
- Local Whisper STT + Kokoro TTS for two-way voice conversations
- All processing happens locally
- Requires Python/uvx + Whisper model download

---

## 5. macOS Built-in Dictation
**Cost:** Free | **Setup:** System Settings > Keyboard > Dictation > Turn On

- Double-tap Fn to dictate anywhere including Terminal
- On-device recognition on Apple Silicon (no internet needed)
- Not code-aware — decent for natural language prompts only

---

## Quick Comparison

| Option | Cost | Offline | Code-Aware | Setup | Two-Way |
|--------|------|---------|------------|-------|---------|
| `/voice` native | Free | N/A | Yes | None | No |
| Superwhisper | $10/mo | Yes | Yes | Low | No |
| Wispr Flow | Free-$10/mo | No | Yes | Low | No |
| VoiceMode MCP | Free | Yes | Yes | Medium | Yes |
| macOS Dictation | Free | Yes* | No | None | No |

## Recommendation

1. Try `/voice` first — if available, done
2. If not, install **Superwhisper** for best dev experience
3. Or try **macOS Dictation** (free, zero setup) to test the workflow first
