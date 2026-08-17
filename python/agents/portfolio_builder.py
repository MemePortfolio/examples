"""
MemePortfolio Example: Portfolio Builder
========================================
Agent: memeportfolio-portfolio-builder
Source: .claude/agents/memeportfolio-portfolio-builder.md

Builds an optimal Markowitz mean-variance portfolio of Solana meme tokens.
Behaviour — token selection, output format, Sharpe ratio thresholds — is
driven entirely by the agent definition .md file, not by code.

Setup:
    pip install anthropic mcp>=1.3.0
    export ANTHROPIC_API_KEY="your-anthropic-key"
    # x402 payment is handled automatically by compatible MCP clients

Usage:
    python python/agents/portfolio_builder.py
    python python/agents/portfolio_builder.py 5   # 5-token portfolio
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
    "memeportfolio-portfolio-builder.md"
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


def build_portfolio(number_of_tokens: int = 10) -> str:
    log.info("Building Markowitz portfolio — number_of_tokens=%d", number_of_tokens)
    model, system_prompt, frontmatter = load_agent(AGENT_MD)

    user_message = (
        f"Build me an optimal Solana meme token portfolio with {number_of_tokens} tokens."
    )

    log.info(
        "Calling create_markowitz_portfolio via memeportfolio-portfolio-builder agent (model=%s)",
        model,
    )
    result = memeportfolio.run(
        user_message, system=system_prompt, model=model, frontmatter=frontmatter
    )

    if not result:
        log.warning("No text block found in response")
    else:
        log.info("Portfolio built — report length=%d chars", len(result))

    return result


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10

    log.info("=== Portfolio Builder starting ===")
    print(f"Building optimal Solana meme token portfolio ({n} tokens)\n")
    print("=" * 60)

    report = build_portfolio(n)
    print(report)

    log.info("=== Portfolio Builder done ===")
