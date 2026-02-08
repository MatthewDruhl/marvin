# D&D Coding Project

Last updated: 2026-02-07

---

## D&D Campaign MCP (COMPLETE)
- **Location:** `/Users/matthewdruhl/Code/AI/DnDProject/dnd-campaign-mcp`
- **Status:** Built and connected to Claude.ai Desktop
- **Tools:** Character management (HP, XP) + Inventory (items, wealth)
- **Features:** Multi-character support with active character system
- **Next:** Test in live session, consider mobile sync pattern

## D&D Character Sheet Web App (Phase 3 COMPLETE)
- **Location:** `/Users/matthewdruhl/Code/AI/DnDProject/dnd-character-sheet`
- **Status:** Phase 3 COMPLETE - Backend API functional and tested
- **Branch:** feature/phase3-backend-api
- **Tech Stack:** React (Vite) + FastAPI + PostgreSQL (Docker)
- **Architecture:** REST API wrapper, shared database with MCP
- **Ports:** Backend on 8001, Frontend on 5173, MCP on 8000, Postgres on 5432
- **Using:** uv for Python, modern pyproject.toml setup
- **Database:** 10 tables (characters -> character_class, items, inventory, wealth, vault, bank, bags system)
- **Advanced Features:** Bag of Holding system (individual tracking, 4 sizes, capacity limits)
- **Environment:** .env and .env.example configured, timezone-aware timestamps
- **DevOps:** Management scripts (monitor.sh, start-all.sh, stop-all.sh)
- **VS Code:** Workspace configured with proper settings, extensions, and debug configs
- **Phase 3 Complete:** config.py (Pydantic Settings), database.py (SQLAlchemy engine/sessions), models.py (10 ORM models), schemas.py (27 Pydantic schemas), routes/characters.py (5 CRUD endpoints), main.py (FastAPI app wired and tested)
- **Next Phase Options:** Migrate MCP to PostgreSQL (share database) or start frontend development
- **Educational Material:** Phase3-Remaining-Pieces.md guide in ~/Documents/marvin/
- **Learning approach:** Senior dev -> junior dev teaching style, Matt writes code with guidance

## DND Combat Engine (EXISTING)
- **Location:** `/Users/matthewdruhl/Code/AI/DnDProject/dnd-combat-engine`
- **Status:** 65 tests passing, core mechanics complete
- **Tech:** Python, pytest, TDD approach
- **Note:** Could integrate with MCP server in future, kept separate from web app
