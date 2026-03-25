#!/bin/bash
# Google Workspace Setup for Claude Code
# Created by Sterling Chin
#
# This sets up Google Workspace MCP with the correct scopes
# (excludes Tasks API which has a bug)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Google Workspace Setup for Claude${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get client ID
if [ -z "$GOOGLE_OAUTH_CLIENT_ID" ]; then
    echo -e "${YELLOW}Enter the Google OAuth Client ID${NC}"
    echo "(Get this from Google Cloud Console)"
    echo ""
    read -p "Client ID: " GOOGLE_CLIENT_ID
    echo ""
else
    GOOGLE_CLIENT_ID="$GOOGLE_OAUTH_CLIENT_ID"
fi

if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo -e "${RED}Error: Client ID is required${NC}"
    exit 1
fi

# Get client secret
if [ -z "$GOOGLE_OAUTH_CLIENT_SECRET" ]; then
    echo -e "${YELLOW}Enter the Google OAuth Client Secret${NC}"
    echo "(Get this from Google Cloud Console)"
    echo ""
    read -s -p "Client Secret: " GOOGLE_CLIENT_SECRET
    echo ""
else
    GOOGLE_CLIENT_SECRET="$GOOGLE_OAUTH_CLIENT_SECRET"
fi

if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo -e "${RED}Error: Client secret is required${NC}"
    exit 1
fi

# Check prerequisites
echo ""
echo -e "${BLUE}Checking prerequisites...${NC}"

if command -v uvx &> /dev/null; then
    echo -e "${GREEN}  uv/uvx installed${NC}"
else
    echo -e "${YELLOW}  Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

if command -v claude &> /dev/null; then
    echo -e "${GREEN}  Claude Code installed${NC}"
else
    echo -e "${RED}  Claude Code not found${NC}"
    echo "  Install: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Scope selection
echo ""
echo "Where should this integration be available?"
echo "  1) All projects (user-scoped)"
echo "  2) This project only (project-scoped)"
echo ""
echo -e "${YELLOW}Choice [2]:${NC}"
read -r SCOPE_CHOICE
SCOPE_CHOICE=${SCOPE_CHOICE:-2}

if [[ "$SCOPE_CHOICE" == "1" ]]; then
    SCOPE_FLAG="-s user"
else
    SCOPE_FLAG=""
fi

# Store credentials locally within the project
PROJECT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
CREDS_DIR="$PROJECT_DIR/.google-workspace-credentials"
mkdir -p "$CREDS_DIR"

# Add to .gitignore if git repo
if [ -d "$PROJECT_DIR/.git" ]; then
    if ! grep -q ".google-workspace-credentials" "$PROJECT_DIR/.gitignore" 2>/dev/null; then
        echo ".google-workspace-credentials/" >> "$PROJECT_DIR/.gitignore"
        echo -e "${GREEN}  Added credentials dir to .gitignore${NC}"
    fi
fi

# Tool selection
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Select Google Workspace Tools${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Available tools:"
echo ""
echo "  1) gmail       - Read, search, and send emails"
echo "  2) calendar    - View events, check availability, create meetings"
echo "  3) drive       - Search and read files in Google Drive"
echo "  4) docs        - Read and edit Google Docs"
echo "  5) sheets      - Read and edit Google Sheets"
echo "  6) slides      - Read and edit Google Slides"
echo "  7) chat        - Google Chat messaging"
echo "  8) forms       - Create and manage Google Forms"
echo "  9) contacts    - Access Google Contacts"
echo " 10) search      - Google Search"
echo ""
echo -e "${YELLOW}Enter tool numbers separated by spaces (e.g. 1 2 3)${NC}"
echo -e "${YELLOW}Or press Enter for default [gmail calendar]: ${NC}"
read -r TOOL_SELECTION
TOOL_SELECTION=${TOOL_SELECTION:-"1 2"}

# Map numbers to tool names
SELECTED_TOOLS=""
for num in $TOOL_SELECTION; do
    case $num in
        1) SELECTED_TOOLS="$SELECTED_TOOLS gmail" ;;
        2) SELECTED_TOOLS="$SELECTED_TOOLS calendar" ;;
        3) SELECTED_TOOLS="$SELECTED_TOOLS drive" ;;
        4) SELECTED_TOOLS="$SELECTED_TOOLS docs" ;;
        5) SELECTED_TOOLS="$SELECTED_TOOLS sheets" ;;
        6) SELECTED_TOOLS="$SELECTED_TOOLS slides" ;;
        7) SELECTED_TOOLS="$SELECTED_TOOLS chat" ;;
        8) SELECTED_TOOLS="$SELECTED_TOOLS forms" ;;
        9) SELECTED_TOOLS="$SELECTED_TOOLS contacts" ;;
        10) SELECTED_TOOLS="$SELECTED_TOOLS search" ;;
        *) echo -e "${RED}Unknown option: $num (skipping)${NC}" ;;
    esac
done

# Trim leading space
SELECTED_TOOLS=$(echo "$SELECTED_TOOLS" | xargs)

if [ -z "$SELECTED_TOOLS" ]; then
    echo -e "${RED}Error: No valid tools selected${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Selected tools: $SELECTED_TOOLS${NC}"

# Remove existing MCP if present
echo ""
echo -e "${BLUE}Configuring Google Workspace MCP...${NC}"
claude mcp remove google-workspace 2>/dev/null || true

# GOOGLE_MCP_CREDENTIALS_DIR keeps OAuth tokens local to this project
claude mcp add google-workspace $SCOPE_FLAG \
    --env GOOGLE_OAUTH_CLIENT_ID="$GOOGLE_CLIENT_ID" \
    --env GOOGLE_OAUTH_CLIENT_SECRET="$GOOGLE_CLIENT_SECRET" \
    --env GOOGLE_MCP_CREDENTIALS_DIR="$CREDS_DIR" \
    -- uvx workspace-mcp --tools $SELECTED_TOOLS

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "  1. Start Claude Code: ${YELLOW}claude${NC}"
echo ""
echo "  2. First Google request will open browser for login"
echo ""
echo "  3. Try: ${YELLOW}\"What's on my calendar today?\"${NC}"
echo ""
