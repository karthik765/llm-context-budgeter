#!/usr/bin/env python3
"""Tiny CLI to fit text into an LLM context budget with low overhead.

Heuristic token estimate: ~1 token per 4 characters.
"""

from __future__ import annotations
import argparse
from pathlib import Path


def estimate_tokens(text: str) -> int:
    return max(1, (len(text) + 3) // 4)


def clip_to_budget(text: str, max_tokens: int, reserve_tokens: int = 0) -> tuple[str, int, int]:
    allowed = max(1, max_tokens - max(0, reserve_tokens))
    total = estimate_tokens(text)
    if total <= allowed:
        return text, total, total

    # Convert token budget back to char budget using same heuristic.
    char_budget = allowed * 4
    clipped = text[:char_budget]

    # Prefer clipping at paragraph/line boundary if possible.
    for sep in ("\n\n", "\n", ". ", " "):
        idx = clipped.rfind(sep)
        if idx > char_budget * 0.6:
            clipped = clipped[: idx + len(sep)].rstrip()
            break

    return clipped, total, estimate_tokens(clipped)


def main() -> None:
    p = argparse.ArgumentParser(description="Fit text into an LLM context budget.")
    p.add_argument("input", help="Path to input text file")
    p.add_argument("--max-tokens", type=int, default=4000, help="Total context window")
    p.add_argument("--reserve", type=int, default=600, help="Reserve tokens for system+response")
    p.add_argument("--output", default="trimmed.txt", help="Output file path")
    args = p.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    trimmed, original_toks, final_toks = clip_to_budget(text, args.max_tokens, args.reserve)
    Path(args.output).write_text(trimmed, encoding="utf-8")

    print(f"input_tokens_estimate={original_toks}")
    print(f"output_tokens_estimate={final_toks}")
    print(f"max_tokens={args.max_tokens}, reserve={args.reserve}, usable={max(1, args.max_tokens-args.reserve)}")
    print(f"wrote={args.output}")


if __name__ == "__main__":
    main()
