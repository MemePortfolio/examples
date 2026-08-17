"""
MemePortfolio HTTP helper — per-call MCP connection.

Opens a new streamable-HTTP connection for every run() call.
HTTP transport is stateless, so no persistent session is needed.

Access: x402 pay-per-call — no API key required.
An x402-compatible MCP client handles HTTP 402 payment automatically.

Requires:  pip install anthropic mcp>=1.3.0
"""

import os
import asyncio
import threading
import logging

import anthropic
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

from scripts.agent_tools import parse_tool_names, MCP_TOOL_RE, NATIVE_TOOL_DEFS

log = logging.getLogger(__name__)

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
MEMEPORTFOLIO_MCP_URL = os.environ.get(
    "MEMEPORTFOLIO_MCP_URL", "https://mcp.memeportfolio.io/mcp"
)

_client = anthropic.AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

# One event loop in a daemon thread — shared across all run() calls.
_loop = asyncio.new_event_loop()
threading.Thread(target=_loop.run_forever, daemon=True, name="mcp-loop").start()


def _to_anthropic_tool(mcp_tool) -> dict:
    return {
        "name": mcp_tool.name,
        "description": mcp_tool.description or "",
        "input_schema": mcp_tool.inputSchema,
    }


def _tool_content(mcp_resp) -> str:
    parts = [item.text for item in mcp_resp.content if hasattr(item, "text")]
    return "\n".join(parts) if parts else ""


async def _run(
    prompt: str,
    system: str | None,
    model: str,
    allowed_mcp: set[str] | None,
    native_tools: list[dict],
    max_tokens: int,
) -> str:
    async with streamablehttp_client(MEMEPORTFOLIO_MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as sess:
            await sess.initialize()
            listed = await sess.list_tools()
            mcp_tools = [
                _to_anthropic_tool(t)
                for t in listed.tools
                if allowed_mcp is None or t.name in allowed_mcp
            ]
            log.info("MCP tools: %s", [t["name"] for t in mcp_tools])

            all_tools = mcp_tools + native_tools
            messages = [{"role": "user", "content": prompt}]
            extra = {"system": system} if system else {}

            while True:
                response = await _client.messages.create(
                    model=model,
                    max_tokens=max_tokens,
                    tools=all_tools,
                    messages=messages,
                    **extra,
                )
                log.info(
                    "Claude — stop_reason=%s input_tokens=%d output_tokens=%d",
                    response.stop_reason,
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                )

                if response.stop_reason == "end_turn":
                    return "\n\n".join(b.text for b in response.content if b.type == "text")

                if response.stop_reason != "tool_use":
                    log.warning("Unexpected stop_reason: %s", response.stop_reason)
                    return "\n\n".join(b.text for b in response.content if b.type == "text")

                messages.append({"role": "assistant", "content": response.content})

                results = []
                for block in response.content:
                    if block.type != "tool_use":
                        continue
                    log.info("Calling MCP tool: %s  args=%s", block.name, block.input)
                    try:
                        mcp_resp = await sess.call_tool(block.name, block.input)
                        content = _tool_content(mcp_resp)
                        is_error = bool(getattr(mcp_resp, "isError", False))
                    except Exception as exc:
                        content = f"Tool error: {exc}"
                        is_error = True
                        log.error("MCP tool %s failed: %s", block.name, exc)

                    entry = {"type": "tool_result", "tool_use_id": block.id, "content": content}
                    if is_error:
                        entry["is_error"] = True
                    results.append(entry)

                messages.append({"role": "user", "content": results})


def run(
    prompt: str,
    frontmatter: str = "",
    system: str = None,
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 4096,
) -> str:
    """
    Send a prompt to Claude with MemePortfolio MCP tools available.
    Tool access is filtered to those listed in the agent frontmatter.
    """
    tool_names = parse_tool_names(frontmatter)
    allowed_mcp: set[str] = set()
    native_tools: list[dict] = []
    for raw in tool_names:
        m = MCP_TOOL_RE.match(raw)
        if m:
            allowed_mcp.add(m.group(2))
        elif raw in NATIVE_TOOL_DEFS:
            native_tools.append(NATIVE_TOOL_DEFS[raw])

    future = asyncio.run_coroutine_threadsafe(
        _run(prompt, system, model, allowed_mcp or None, native_tools, max_tokens),
        _loop,
    )
    return future.result(timeout=120)


def run_direct(
    prompt: str,
    system: str = None,
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 4096,
) -> str:
    """
    Like run() but with no tool filtering — all MCP tools are available.
    Used by python/MCP/ scripts.
    """
    future = asyncio.run_coroutine_threadsafe(
        _run(prompt, system, model, allowed_mcp=None, native_tools=[], max_tokens=max_tokens),
        _loop,
    )
    return future.result(timeout=120)
