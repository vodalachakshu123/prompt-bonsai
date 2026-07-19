# Configuration

## CompressionConfig

```python
from prompt_bonsai.config import CompressionConfig, CompressionStrategy

config = CompressionConfig(
    strategy=CompressionStrategy.HYBRID,
    target_ratio=0.5,          # Aim for 50% reduction
    min_quality=0.90,         # Reject if quality < 90%
    max_iterations=3,           # Max compression passes
    preserve_patterns=[        # Never touch these
        "{variable}",
        "{{template}}",
    ],
    tokenizer_backend="auto", # "tiktoken", "huggingface", or "auto"
    model_name="gpt-4",       # For accurate token counting
    verbose=False,            # Print compression details
)

compressor = Compressor(config=config)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `strategy` | `CompressionStrategy` | `HYBRID` | Compression approach |
| `target_ratio` | `float` | `0.5` | Target reduction (0.0-1.0) |
| `min_quality` | `float` | `0.90` | Minimum quality threshold |
| `max_iterations` | `int` | `3` | Maximum compression passes |
| `preserve_patterns` | `List[str]` | `[]` | Patterns to protect |
| `tokenizer_backend` | `TokenizerBackend` | `AUTO` | Tokenizer to use |
| `model_name` | `str` | `None` | Model for tokenizer |
| `verbose` | `bool` | `False` | Print details |
