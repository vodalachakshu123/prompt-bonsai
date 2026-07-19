# Quick Start

## One-Shot Compression

The simplest way to compress a prompt:

```python
from prompt_bonsai import compress

long_prompt = """
I would like to kindly request your assistance with a very important matter.
Please, if you could, help me understand the fundamental principles of quantum
mechanics. It would be great if you could provide a comprehensive explanation.
"""

short = compress(long_prompt, ratio=0.5)
print(short)
```

## Using the Compressor Class

For more control, use the `Compressor` class:

```python
from prompt_bonsai import Compressor

compressor = Compressor(
    strategy="hybrid",
    target_ratio=0.4,
    min_quality=0.90,
    verbose=True,
)

result = compressor.compress(long_prompt)

print(f"Original: {result.original_tokens} tokens")
print(f"Compressed: {result.compressed_tokens} tokens")
print(f"Quality: {result.quality_report.overall_score:.2f}")
```

## Preserving Template Variables

```python
from prompt_bonsai import compress

template = "Hello {name}, please analyze {data}"
compressed = compress(template, ratio=0.3, preserve=["{name}", "{data}"])

assert "{name}" in compressed
assert "{data}" in compressed
```

## Next Steps

- Learn about [Compression Strategies](../user-guide/strategies.md)
- Explore [Configuration Options](../user-guide/configuration.md)
- See [Integration Examples](../user-guide/integrations.md)
