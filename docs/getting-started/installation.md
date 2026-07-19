# Installation

## Requirements

- Python 3.9 or higher
- pip or uv

## Basic Installation

```bash
pip install prompt-bonsai
```

## With Optional Dependencies

```bash
# OpenAI integration
pip install prompt-bonsai[openai]

# Anthropic integration
pip install prompt-bonsai[anthropic]

# LangChain integration
pip install prompt-bonsai[langchain]

# All integrations
pip install prompt-bonsai[all]

# Development dependencies
pip install prompt-bonsai[dev]
```

## Verify Installation

```python
from prompt_bonsai import compress, Compressor
print("Prompt Bonsai installed successfully!")
```

## Upgrade

```bash
pip install --upgrade prompt-bonsai
```
