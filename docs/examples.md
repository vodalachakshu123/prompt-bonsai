# Examples

## Basic Usage

```python
from prompt_bonsai import compress, Compressor

# One-shot compression
short = compress(long_prompt, ratio=0.5)

# With quality control
compressor = Compressor(min_quality=0.95)
result = compressor.compress(prompt)
```

## Batch Processing

```python
from prompt_bonsai import Compressor

compressor = Compressor(target_ratio=0.4)

prompts = [prompt1, prompt2, prompt3]
for p in prompts:
    compressor.compress(p)

stats = compressor.stats()
print(f"Saved {stats['total_tokens_saved']} tokens")
```

## Template Variables

```python
from prompt_bonsai import compress

template = "Analyze {data} for {user}"
compressed = compress(template, preserve=["{data}", "{user}"])
```

See the `examples/` directory in the repository for full working scripts.
