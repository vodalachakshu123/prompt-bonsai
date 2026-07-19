# Contributing to Prompt Bonsai

Thank you for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/vodalachakshu123/prompt-bonsai.git
cd prompt-bonsai
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

```bash
make format  # black + ruff
make lint    # ruff + mypy
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Add tests for your changes
4. Run `make all` to ensure everything passes
5. Submit a pull request
