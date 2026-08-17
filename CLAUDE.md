# MemePortfolio Examples — Claude Code Instructions

**Links:** [Website](https://MemePortfolio.io) · [Twitter](https://x.com/MemePortfolio1) · [Blog](https://blog.memeportfolio.io/blog/) · [MCP Repo](https://github.com/MemePortfolio/portfolio-mcp)

## Rules

1. Do not load skills without approval
2. Plan first, then implement

## Project Structure

```
python/agents/          Agent-based examples (load .md as system prompt)
python/MCP/             Direct MCP examples (call tools via user prompt)
python/scripts/         Utility scripts (run_all_examples.py)
python/memeportfolio_http.py  Shared helper — imported by all scripts
.claude/agents/         2 agent definitions pulled from portfolio-mcp repo
```

## MCP Server

**URL:** `https://mcp.memeportfolio.io/mcp`
**Transport:** Streamable HTTP (`POST /mcp`) — not SSE
**Auth:** x402 pay-per-call — no API key, no subscription
**Network:** SOLANA only

### Tools

| Tool ID | Description |
|---------|-------------|
| `create_markowitz_portfolio` | Builds an optimal Markowitz portfolio of Solana meme tokens. Input: `number_of_tokens` (int, default 10, min 2, max 50). |
| `get_portfolio` | Returns balances, prices, USD values, and risk metrics for a Solana wallet's meme holdings. Input: `wallet` (Solana base58 public key, 32–44 chars). |

## Shared Helper

All scripts import `memeportfolio_http` as `memeportfolio` from `python/memeportfolio_http.py`.
Scripts in `python/agents/` and `python/MCP/` must add this to their `sys.path`:

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import memeportfolio_http as memeportfolio
```

`memeportfolio_http` opens a **new streamable-HTTP connection per call** (HTTP is stateless —
no persistent session is needed).
Uses a shared background event loop thread to drive the async MCP client.

Exposes:
- `run(prompt, frontmatter, system, model)` — agentic loop with tool filtering from frontmatter
- `run_direct(prompt, system, model)` — all MCP tools available; used by `python/MCP/` scripts

## Agent Example Pattern

When creating a new agent-based example in `python/agents/`:

1. Load the agent definition from `.claude/agents/<name>.md`
2. Parse frontmatter with `---` split to extract `model`
3. Use the body as the `system` prompt
4. Pass a minimal user message (wallet address or token count only)
5. Call `memeportfolio.run(user_message, frontmatter=frontmatter, system=system_prompt, model=model)`

Standard `load_agent()` function to reuse across all agent scripts:

```python
AGENT_MD = os.path.join(
    os.path.dirname(__file__), "..", "..", ".claude", "agents", "<agent-name>.md"
)

def load_agent(path: str) -> tuple[str, str, str]:
    with open(path) as f:
        content = f.read()
    parts = content.split("---", 2)
    frontmatter = parts[1] if len(parts) >= 3 else ""
    body = parts[2].strip() if len(parts) >= 3 else content.strip()
    m = re.search(r"^model:\s*(.+)$", frontmatter, re.MULTILINE)
    model = m.group(1).strip() if m else "claude-haiku-4-5-20251001"
    return model, body, frontmatter
```

## Existing Agent Examples

| Script | Agent |
|--------|-------|
| `python/agents/portfolio_builder.py` | `memeportfolio-portfolio-builder.md` |
| `python/agents/portfolio_analyzer.py` | `memeportfolio-portfolio-analyzer.md` |

## Agent Definitions

`.claude/agents/` files come from the upstream repo and **must not be hand-edited**.
To refresh both agent definitions from GitHub:

```bash
gh api repos/MemePortfolio/portfolio-mcp/contents/.claude/agents | python3 -c "
import json, sys, base64, subprocess
for f in json.load(sys.stdin):
    data = json.loads(subprocess.run(['gh', 'api', f['url']], capture_output=True, text=True).stdout)
    open(f'.claude/agents/{f[\"name\"]}', 'w').write(base64.b64decode(data['content']).decode())
    print('Updated', f['name'])
"
```

## Environment Variables

```bash
export ANTHROPIC_API_KEY="..."
# MEMEPORTFOLIO_MCP_URL=https://mcp.memeportfolio.io/mcp  # override for local testing
```

Copy `.env.example` to `.env` and fill in your key. `.env` is in `.gitignore`.

MemePortfolio MCP does **not** require an API key — access is x402 pay-per-call.

## Running Examples

Always run from the project root:

```bash
# agent-based (system prompt from .md)
python python/agents/portfolio_builder.py
python python/agents/portfolio_builder.py 5          # 5-token portfolio
python python/agents/portfolio_analyzer.py <wallet>

# direct MCP (all tools available, plain prompt)
python python/MCP/portfolio_builder.py
python python/MCP/portfolio_builder.py 5
python python/MCP/portfolio_analyzer.py <wallet>
```

## Running All Examples

```bash
python python/scripts/run_all_examples.py
```

Runs all 4 example scripts sequentially (3-second delay between each) and prints a
summary table with status and duration.

## x402 Payment

The MCP server returns HTTP 402 when payment is required.
An x402-compatible client handles payment automatically on 402 responses.
To run examples against the live server, configure an x402 client that can
settle payments on behalf of the MCP session.

For local development, run the MCP server locally (`npm run dev` in the
portfolio-mcp repo) and set `MEMEPORTFOLIO_MCP_URL=http://localhost:PORT/mcp`.

## Further Reading

- [Build a Memecoin Portfolio — Beginner's Guide](https://blog.memeportfolio.io/build-memecoin-portfolio-beginners-guide/)
- [Markowitz Portfolio Optimisation for Memecoins](https://blog.memeportfolio.io/markowitz-portfolio-optimization-memecoins/)
- [Best Memecoins to Hold in 2026 — Data-Driven Selection Guide for Solana](https://blog.memeportfolio.io/best-memecoins-to-hold-in-2026-data-driven-selection-guide-for-solana/)
- [Memecoin Risk Management 2026](https://blog.memeportfolio.io/memecoin-risk-management-2026/)
- [Memecoin Portfolio Rebalancing Guide](https://blog.memeportfolio.io/memecoin-portfolio-rebalancing-guide/)
- [Memecoin Portfolio Tracking Guide](https://blog.memeportfolio.io/memecoin-portfolio-tracking-guide/)
