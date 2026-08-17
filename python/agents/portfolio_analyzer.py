"""
MemePortfolio Example: Portfolio Analyzer
==========================================
Agent: memeportfolio-portfolio-analyzer
Source: .claude/agents/memeportfolio-portfolio-analyzer.md

Analyses existing meme token holdings for a Solana wallet — balances,
prices, USD values, and risk metrics (Sharpe, Sortino, volatility, return).
Behaviour and output format are driven by the agent definition .md file.

Setup:
    pip install anthropic mcp>=1.3.0
    export ANTHROPIC_API_KEY="your-anthropic-key"
    # x402 payment is handled automatically by compatible MCP clients

Usage:
    python python/agents/portfolio_analyzer.py <wallet>
    python python/agents/portfolio_analyzer.py 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
"""

import logging
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import memeportfolio_http as memeportfolio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

AGENT_MD = os.path.join(
    os.path.dirname(__file__), "..", "..", ".claude", "agents",
    "memeportfolio-portfolio-analyzer.md"
)
DEMO_WALLET = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"


def load_agent(path: str) -> tuple[str, str, str]:
    with open(path) as f:
        content = f.read()
    parts = content.split("---", 2)
    frontmatter = parts[1] if len(parts) >= 3 else ""
    body = parts[2].strip() if len(parts) >= 3 else content.strip()
    m = re.search(r"^model:\s*(.+)$", frontmatter, re.MULTILINE)
    model = m.group(1).strip() if m else "claude-haiku-4-5-20251001"
    return model, body, frontmatter


def analyze_portfolio(wallet: str) -> str:
    log.info("Analysing portfolio for wallet=%s", wallet)
    model, system_prompt, frontmatter = load_agent(AGENT_MD)

    user_message = (
        f"Analyse the meme token portfolio for this Solana wallet.\n\n"
        f"Wallet: {wallet}"
    )

    log.info(
        "Calling get_portfolio via memeportfolio-portfolio-analyzer agent (model=%s)", model
    )
    result = memeportfolio.run(
        user_message, system=system_prompt, model=model, frontmatter=frontmatter
    )

    if not result:
        log.warning("No text block found in response")
    else:
        log.info("Analysis complete — report length=%d chars", len(result))

    return result


if __name__ == "__main__":
    wallet = sys.argv[1] if len(sys.argv) > 1 else DEMO_WALLET

    log.info("=== Portfolio Analyzer starting ===")
    print(f"Analysing portfolio for wallet: {wallet}\n")
    print("=" * 60)

    report = analyze_portfolio(wallet)
    print(report)

    log.info("=== Portfolio Analyzer done ===")
