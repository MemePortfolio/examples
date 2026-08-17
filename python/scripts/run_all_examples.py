"""
Run all MemePortfolio example scripts sequentially and print a summary table.

Usage:
    python python/scripts/run_all_examples.py
"""

import subprocess
import sys
import time

DEMO_WALLET = "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU"

EXAMPLES = [
    # (script, args)
    ("python/agents/portfolio_builder.py", []),
    ("python/agents/portfolio_analyzer.py", [DEMO_WALLET]),
    ("python/MCP/portfolio_builder.py", []),
    ("python/MCP/portfolio_analyzer.py", [DEMO_WALLET]),
]

DELAY_BETWEEN = 3  # seconds between scripts


def run_script(script: str, args: list[str]) -> tuple[str, float]:
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, script] + args,
            capture_output=True,
            text=True,
            timeout=120,
        )
        status = "OK" if result.returncode == 0 else f"ERROR ({result.returncode})"
    except subprocess.TimeoutExpired:
        status = "TIMEOUT"
    elapsed = time.time() - start
    return status, elapsed


def main():
    print(f"Running {len(EXAMPLES)} example scripts\n{'=' * 60}")
    results = []
    for i, (script, args) in enumerate(EXAMPLES):
        label = script + (" " + " ".join(args) if args else "")
        print(f"\n[{i + 1}/{len(EXAMPLES)}] {label}")
        status, elapsed = run_script(script, args)
        results.append((label, status, elapsed))
        print(f"  → {status}  ({elapsed:.1f}s)")
        if i < len(EXAMPLES) - 1:
            time.sleep(DELAY_BETWEEN)

    print(f"\n{'=' * 60}\nSummary\n{'=' * 60}")
    print(f"{'Script':<58} {'Status':<12} {'Time':>6}")
    print("-" * 78)
    for label, status, elapsed in results:
        print(f"{label:<58} {status:<12} {elapsed:>5.1f}s")

    ok = sum(1 for _, s, _ in results if s == "OK")
    print(f"\n{ok}/{len(results)} passed")


if __name__ == "__main__":
    main()
