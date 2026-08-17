"""
MemePortfolio Example: Portfolio Analyzer (direct MCP)
=======================================================
Tool: get_portfolio

Returns token balances, current prices, USD values, and risk metrics
for a Solana wallet's existing meme token holdings.

Use cases:
  - "What meme tokens do I hold?"
  - "Show me the risk metrics for my Solana wallet."
  - "Analyse the portfolio for wallet address ABC123..."

Setup:
    pip install anthropic mcp>=1.3.0
    export ANTHROPIC_API_KEY="your-anthropic-key"
    # x402 payment is handled automatically by compatible MCP clients

Register the MCP server (one-time, for Claude Code / Claude Desktop):
    claude mcp add --transport http memeportfolio-mcp-server https://mcp.memeportfolio.io/mcp

Usage:
    python python/MCP/portfolio_analyzer.py
    python python/MCP/portfolio_analyzer.py <wallet>
"""

import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import memeportfolio_http as memeportfolio

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

DEMO_WALLET = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"


def analyze_portfolio(wallet: str) -> str:
    """
    Analyse a Solana wallet's meme token holdings.

    Uses get_portfolio to return:
      - Per-token: balance, price, USD value, weight, annual return,
        annual volatility, Sharpe ratio, Sortino ratio
      - Portfolio-level metrics and concentration risk assessment
    """
    log.info("Analysing portfolio for wallet=%s", wallet)

    prompt = (
        f"Use the get_portfolio tool to analyse this Solana wallet's meme token holdings.\n\n"
        f"Wallet: {wallet}\n\n"
        f"Return: all token holdings with balances, current prices, USD values, and risk metrics "
        f"(weight, annual return, annual volatility, Sharpe ratio, Sortino ratio). "
        f"Include the aggregate portfolio metrics and flag any concentration risk."
    )

    log.info("Calling get_portfolio via MemePortfolio MCP")
    result = memeportfolio.run_direct(prompt)

    if not result:
        log.warning("No text block found in response")
    else:
        log.info("Analysis complete — report length=%d chars", len(result))

    return result


if __name__ == "__main__":
    wallet = sys.argv[1] if len(sys.argv) > 1 else DEMO_WALLET

    log.info("=== Portfolio Analyzer (direct MCP) starting ===")
    print(f"Analysing portfolio for wallet: {wallet}\n")
    print("=" * 60)

    report = analyze_portfolio(wallet)
    print(report)

    log.info("=== Portfolio Analyzer (direct MCP) done ===")
