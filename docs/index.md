# 🌳 Prompt Bonsai

> **Cut your LLM token costs by 30–70% without losing meaning.**

Prompt Bonsai intelligently compresses prompts for Large Language Models (LLMs), reducing token usage and API costs while preserving semantic meaning and output quality.

## Why Prompt Bonsai?

| Problem | Solution |
|---------|----------|
| Token costs eating your budget? | **30–70% token reduction** with quality guarantees |
| Context window too small? | Fit more content in limited context |
| Prompts full of filler? | Remove semantic redundancy automatically |
| JSON/code bloating tokens? | Structural optimization preserves syntax |
| Worried about quality loss? | Built-in quality assessment with configurable thresholds |

## Installation

```bash
pip install prompt-bonsai
```

## Quick Start

```python
from prompt_bonsai import compress

long_prompt = "I would like to kindly request your assistance with..."
short = compress(long_prompt, ratio=0.5)
print(f"Saved {len(long_prompt) - len(short)} characters")
```

## Features

- **Three compression strategies**: Semantic, Structural, and Hybrid (auto-detect)
- **Quality guarantees**: Rejects compression if meaning degrades below threshold
- **Template-safe**: Preserve `{variables}` and other patterns during compression
- **Multi-backend tokenization**: tiktoken, HuggingFace, or auto-detection
- **Cost tracking**: Built-in metrics for token savings and estimated cost reduction
- **Framework integrations**: Works with OpenAI, LangChain, LiteLLM, and more

## Next Steps

- [Installation Guide](getting-started/installation.md)
- [Quick Start Tutorial](getting-started/quick-start.md)
- [Compression Strategies](user-guide/strategies.md)
- [API Reference](api/compressor.md)
