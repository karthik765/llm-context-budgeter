# llm-context-budgeter

Small Python CLI to trim long text files so they fit inside an LLM context budget.

## Why
When sending docs/prompts to models, you usually need to reserve tokens for system instructions and model output. This tool gives a quick, dependency-free pre-trim step.

## Usage
```bash
python3 budgeter.py notes.txt --max-tokens 8000 --reserve 1200 --output prompt_input.txt
```

Example output:
```text
input_tokens_estimate=10542
output_tokens_estimate=6800
max_tokens=8000, reserve=1200, usable=6800
wrote=prompt_input.txt
```

## Notes
- Fast heuristic (`~1 token per 4 chars`) keeps it lightweight.
- Tries to cut on paragraph/line/sentence boundaries when possible.
- No external dependencies.

---
Built with OpenClaw for karthik765.
