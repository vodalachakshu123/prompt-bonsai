# Compression Strategies

Prompt Bonsai offers three compression strategies, each optimized for different prompt types.

## Semantic Strategy

**Best for:** Conversational prompts, instructions, explanations

Removes:
- Filler words ("please", "kindly", "I would like to")
- Redundant phrases ("advance planning", "final outcome")
- Weak adverbs ("very", "really", "quite")
- Verbose constructions ("in order to" → "to")

```python
from prompt_bonsai import Compressor

compressor = Compressor(strategy="semantic", target_ratio=0.4)
result = compressor.compress("I would like to kindly request...")
```

## Structural Strategy

**Best for:** Code, JSON, XML, markdown

Optimizes:
- Extra whitespace and blank lines
- JSON/XML formatting (minifies without breaking)
- Code comments (removes while preserving structure)
- Markdown formatting (simplifies headers, lists)
- Decorative ASCII art and separators

```python
compressor = Compressor(strategy="structural", target_ratio=0.4)
result = compressor.compress(json_prompt)
```

## Hybrid Strategy (Default)

**Best for:** Mixed content — auto-detects and applies optimal approach

Analyzes prompt type:
- **Structured** (code, JSON, XML) → Structural first, then Semantic
- **Conversational** (questions, instructions) → Semantic first, then Structural
- **Mixed** → Alternates both strategies

```python
compressor = Compressor(strategy="hybrid", target_ratio=0.4)
result = compressor.compress(any_prompt)  # Automatically optimized
```

## Strategy Comparison

| Strategy | Speed | Compression | Quality | Best For |
|----------|-------|-------------|---------|----------|
| Semantic | Fast | Medium | High | Chat, instructions |
| Structural | Fast | High | Medium | Code, data |
| Hybrid | Medium | High | High | Mixed content |
