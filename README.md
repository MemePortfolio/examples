# MemePortfolio Examples

Python examples for the [MemePortfolio MCP Server](https://github.com/MemePortfolio/portfolio-mcp) — build optimal Markowitz portfolios of Solana meme tokens and analyse existing wallet holdings.

**Links:** [Website](https://MemePortfolio.io) · [Twitter](https://x.com/MemePortfolio1) · [Blog](https://blog.memeportfolio.io/blog/) · [MCP Repo](https://github.com/MemePortfolio/portfolio-mcp)

---

## MCP Server

| | |
|---|---|
| **URL** | `https://mcp.memeportfolio.io/mcp` |
| **Transport** | Streamable HTTP (`POST /mcp`) |
| **Auth** | x402 pay-per-call — no API key required |
| **Network** | SOLANA |

### Tools

| Tool | Description |
|------|-------------|
| `create_markowitz_portfolio` | Builds an optimal Markowitz mean-variance portfolio of Solana meme tokens. Input: `number_of_tokens` (default 10, min 2, max 50). |
| `get_portfolio` | Returns balances, prices, USD values, and risk metrics for a Solana wallet's meme token holdings. Input: `wallet` (Solana base58 public key). |

---

## Repository Structure

```
python/
  memeportfolio_http.py   shared helper — MCP connection and agentic loop
  agents/                 agent-based examples (agent .md drives behaviour)
    portfolio_builder.py  create_markowitz_portfolio via agent system prompt
    portfolio_analyzer.py get_portfolio via agent system prompt
  MCP/                    direct MCP examples (plain prompt, all tools)
    portfolio_builder.py  create_markowitz_portfolio
    portfolio_analyzer.py get_portfolio
  scripts/
    run_all_examples.py   run all 4 examples and print a summary table
  requirements.txt

.claude/agents/           Claude Code subagent definitions (from portfolio-mcp)
  memeportfolio-portfolio-builder.md
  memeportfolio-portfolio-analyzer.md
```

### Two example patterns

**Agent-based** (`python/agents/`) — the `.md` agent definition is loaded as the system prompt. Tool selection, output format, and thresholds are defined in the `.md`, not in code. Use this pattern when you want behaviour that stays in sync with the upstream agent definition.

**Direct MCP** (`python/MCP/`) — a plain user prompt with all MCP tools available. Use this pattern for quick integrations or when you want full control over the prompt.

---

## Setup

```bash
git clone https://github.com/MemePortfolio/examples.git
cd examples
pip install -r python/requirements.txt
cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY
```

---

## Running Examples

Run all commands from the project root.

```bash
# agent-based
python python/agents/portfolio_builder.py           # 10-token portfolio (default)
python python/agents/portfolio_builder.py 5         # 5-token portfolio
python python/agents/portfolio_analyzer.py <wallet>

# direct MCP
python python/MCP/portfolio_builder.py
python python/MCP/portfolio_builder.py 5
python python/MCP/portfolio_analyzer.py <wallet>

# run all examples
python python/scripts/run_all_examples.py
```

---

## Environment Variables

```bash
export ANTHROPIC_API_KEY="your-anthropic-key"
# MEMEPORTFOLIO_MCP_URL=https://mcp.memeportfolio.io/mcp  # override for local testing
```

MemePortfolio MCP does not require an API key — access is x402 pay-per-call.

---

## Claude Code Setup

Register the MCP server in Claude Code to use the bundled subagents directly:

```bash
claude mcp add --transport http memeportfolio-mcp-server https://mcp.memeportfolio.io/mcp
```

Then copy the agent definitions into your project:

```bash
cp .claude/agents/memeportfolio-*.md your-project/.claude/agents/
```

---

## x402 Payment

The MCP server returns HTTP 402 when payment is required. An x402-compatible client
settles the payment automatically and retries. For local development, run the MCP server
locally (`npm run dev` in the [portfolio-mcp](https://github.com/MemePortfolio/portfolio-mcp)
repo) and set `MEMEPORTFOLIO_MCP_URL=http://localhost:PORT/mcp`.

---

## Further Reading

- [Build a Memecoin Portfolio — Beginner's Guide](https://blog.memeportfolio.io/build-memecoin-portfolio-beginners-guide/)
- [Markowitz Portfolio Optimisation for Memecoins](https://blog.memeportfolio.io/markowitz-portfolio-optimization-memecoins/)
- [Best Memecoins to Hold in 2026 — Data-Driven Selection Guide for Solana](https://blog.memeportfolio.io/best-memecoins-to-hold-in-2026-data-driven-selection-guide-for-solana/)
- [Memecoin Risk Management 2026](https://blog.memeportfolio.io/memecoin-risk-management-2026/)
- [Memecoin Portfolio Rebalancing Guide](https://blog.memeportfolio.io/memecoin-portfolio-rebalancing-guide/)
- [Memecoin Portfolio Tracking Guide](https://blog.memeportfolio.io/memecoin-portfolio-tracking-guide/)
