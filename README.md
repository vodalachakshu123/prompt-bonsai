# 🌳 Prompt Bonsai

> **Cut your LLM token costs by 30–70% without losing meaning.**

[![PyPI version](https://badge.fury.io/py/prompt-bonsai.svg)](https://badge.fury.io/py/prompt-bonsai)
[![Python versions](https://img.shields.io/pypi/pyversions/prompt-bonsai.svg)](https://pypi.org/project/prompt-bonsai/)
[![CI](https://github.com/vodalachakshu/prompt-bonsai/workflows/CI/badge.svg)](https://github.com/vodalachakshu/prompt-bonsai/actions)
[![Codecov](https://codecov.io/gh/vodalachakshu/prompt-bonsai/branch/main/graph/badge.svg)](https://codecov.io/gh/vodalachakshu/prompt-bonsai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

With optional dependencies:
```bash
pip install prompt-bonsai[openai,langchain]  # For integrations
pip install prompt-bonsai[all]                  # Everything
```

## Quick Start

### One-line compression

```python
from prompt_bonsai import compress

long_prompt = "I would like to kindly request your assistance with..." * 10
short = compress(long_prompt, ratio=0.5)

print(f"Saved {len(long_prompt) - len(short)} characters")
```

### Full control with Compressor

```python
from prompt_bonsai import Compressor

compressor = Compressor(
    strategy="hybrid",      # "semantic", "structural", or "hybrid"
    target_ratio=0.4,        # Aim for 40% reduction
    min_quality=0.90,       # Reject if quality drops below 90%
    preserve=["{user_id}"], # Keep template variables
    model_name="gpt-4",     # Optimize for specific tokenizer
    verbose=True,           # Show compression details
)

result = compressor.compress(your_prompt)

print(result.text)                          # Compressed prompt
print(result.original_tokens)             # Before
print(result.compressed_tokens)           # After
print(result.quality_report.overall_score)  # Quality: 0.0–1.0
```

## Compression Strategies

| Strategy | Best For | How It Works |
|----------|----------|--------------|
| **Semantic** | Conversational prompts | Removes filler words, redundant phrases, weak adverbs |
| **Structural** | Code, JSON, XML | Normalizes whitespace, minimizes structured data, removes comments |
| **Hybrid** | Mixed content *(default)* | Auto-detects prompt type and applies optimal strategy |

## Real-World Example

```python
from prompt_bonsai import Compressor

compressor = Compressor(target_ratio=0.5, verbose=True)

system_prompt = """
You are an expert Python developer. Please review the following code
and suggest improvements for readability, performance, and
maintainability. Consider PEP 8 compliance, type hints, documentation,
error handling, and testing coverage in your analysis.
"""

result = compressor.compress(system_prompt)
```

**Output:**
```
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric              ┃ Value                           ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Strategy            │ HybridCompressor                │
│ Original Tokens     │ 67                              │
│ Compressed Tokens   │ 34                              │
│ Tokens Saved        │ 33 (49.3%)                      │
│ Quality Score       │ 0.912                           │
│ Semantic Similarity │ 0.845                           │
│ Structural Integrity│ 1.000                           │
└─────────────────────┴─────────────────────────────────┘
```

## Integration Examples

### With OpenAI

```python
from openai import OpenAI
from prompt_bonsai import compress

client = OpenAI()

prompt = "Your very long prompt here..."
compressed = compress(prompt, ratio=0.4)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": compressed}]
)
```

### With LangChain

```python
from prompt_bonsai import Compressor

compressor = Compressor(target_ratio=0.3)

# Compress before creating your prompt
compressed_context = compressor.compress(large_document).text

# Use in your LangChain pipeline
prompt = PromptTemplate.from_template(
    "Answer based on: {context}\n\nQuestion: {question}"
)
```

## Configuration

```python
from prompt_bonsai.config import CompressionConfig, CompressionStrategy

config = CompressionConfig(
    strategy=CompressionStrategy.HYBRID,
    target_ratio=0.5,
    min_quality=0.90,
    max_iterations=3,
    preserve_patterns=["{variable}", "{{template}}"],
    tokenizer_backend="auto",  # "tiktoken", "huggingface", or "auto"
    model_name="gpt-4",        # For accurate token counting
)

compressor = Compressor(config=config)
```

## CLI Usage

```bash
# Compress a file
prompt-bonsai compress input.txt --ratio 0.5 --output compressed.txt

# Compress from stdin
echo "Your long prompt..." | prompt-bonsai compress --ratio 0.4

# Check token count
prompt-bonsai tokens "Your prompt here" --model gpt-4
```

## Benchmarks

Run benchmarks against standard datasets:

```bash
python benchmarks/run_benchmarks.py
```

## API Reference

See [full documentation](https://prompt-bonsai.readthedocs.io).

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md).

```bash
git clone https://github.com/vodalachakshu/prompt-bonsai.git
cd prompt-bonsai
pip install -e ".[dev]"
pytest
```

## License

MIT License — see [LICENSE](LICENSE).
