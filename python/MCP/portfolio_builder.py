"""
MemePortfolio Example: Portfolio Builder (direct MCP)
======================================================
Tool: create_markowitz_portfolio

Builds an optimal Markowitz mean-variance portfolio of Solana meme tokens.
Selects and weights tokens to maximise the Sharpe ratio.

Use cases:
  - "Build me an optimal Solana meme token portfolio."
  - "What is the best 10-token meme coin allocation right now?"
  - "Create a Markowitz portfolio with 5 Solana meme tokens."

Setup:
    pip install anthropic mcp>=1.3.0
    export ANTHROPIC_API_KEY="your-anthropic-key"
    # x402 payment is handled automatically by compatible MCP clients

Register the MCP server (one-time, for Claude Code / Claude Desktop):
    claude mcp add --transport http memeportfolio-mcp-server https://mcp.memeportfolio.io/mcp

Usage:
    python python/MCP/portfolio_builder.py
    python python/MCP/portfolio_builder.py 5   # 5-token portfolio
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


def build_portfolio(number_of_tokens: int = 10) -> str:
    """
    Build an optimal Markowitz portfolio of Solana meme tokens.

    Uses create_markowitz_portfolio to return:
      - Per-token weights, annual return, volatility, Sharpe, Sortino
      - Portfolio-level metrics (Sharpe, Sortino, return, volatility)
    """
    log.info("Building Markowitz portfolio — number_of_tokens=%d", number_of_tokens)

    prompt = (
        f"Use the create_markowitz_portfolio tool to build an optimal Solana meme token portfolio.\n\n"
        f"Number of tokens: {number_of_tokens}\n\n"
        f"Return: the full allocation table sorted by weight (highest first), "
        f"portfolio-level Sharpe ratio, annual return and volatility, "
        f"and a brief risk/return summary."
    )

    log.info("Calling create_markowitz_portfolio via MemePortfolio MCP")
    result = memeportfolio.run_direct(prompt)

    if not result:
        log.warning("No text block found in response")
    else:
        log.info("Portfolio built — report length=%d chars", len(result))

    return result


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    log.info("=== Portfolio Builder (direct MCP) starting ===")
    print(f"Building optimal Solana meme token portfolio ({n} tokens)\n")
    print("=" * 60)

    report = build_portfolio(n)
    print(report)

    log.info("=== Portfolio Builder (direct MCP) done ===")
