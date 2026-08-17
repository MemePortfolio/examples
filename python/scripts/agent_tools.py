import re

# ---------------------------------------------------------------------------
# One-time registry: connection details for every MCP server used by ANY agent.
# Keyed by the server "name" exactly as it appears in tools: mcp__<name>__<tool>
# ---------------------------------------------------------------------------
MCP_SERVER_REGISTRY = {
    "memeportfolio-mcp-server": {
        "type": "url",
        "url": "https://mcp.memeportfolio.io/mcp",
        "name": "memeportfolio-mcp-server",
        # x402 pay-per-call — no authorization_token needed
    },
}

# Native (non-MCP) Anthropic tools an agent.md might list under `tools:`
NATIVE_TOOL_DEFS = {
    "WebSearch": {"type": "web_search_20250305", "name": "web_search"},
    "WebFetch": {"type": "web_fetch_20250910", "name": "web_fetch"},
}

MCP_TOOL_RE = re.compile(r"^mcp__([^_].*?)__([^_].*)$")


def parse_tool_names(frontmatter: str) -> list[str]:
    """Extract the comma-separated `tools:` list from agent frontmatter."""
    m = re.search(r"^tools:\s*(.+)$", frontmatter, re.MULTILINE)
    if not m:
        return []
    return [t.strip() for t in m.group(1).split(",") if t.strip()]
