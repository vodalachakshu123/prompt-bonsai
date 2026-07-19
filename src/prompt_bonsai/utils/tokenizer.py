"""Tokenizer utilities for prompt-bonsai."""

import re
from typing import Optional, List
from enum import Enum

from prompt_bonsai.exceptions import TokenizationError
from prompt_bonsai.config import TokenizerBackend


class Tokenizer:
    """Unified tokenizer interface supporting multiple backends."""

    def __init__(
        self,
        backend: TokenizerBackend = TokenizerBackend.AUTO,
        model_name: Optional[str] = None,
    ) -> None:
        self.backend = backend
        self.model_name = model_name or "gpt-4"
        self._tiktoken_encoder = None
        self._hf_tokenizer = None
        self._init_backend()

    def _init_backend(self) -> None:
        """Initialize the tokenizer backend."""
        if self.backend == TokenizerBackend.AUTO:
            # Try tiktoken first, fallback to huggingface
            try:
                import tiktoken
                self.backend = TokenizerBackend.TIKTOKEN
            except ImportError:
                self.backend = TokenizerBackend.HUGGINGFACE

        if self.backend == TokenizerBackend.TIKTOKEN:
            try:
                import tiktoken
                # Map common model names to tiktoken encodings
                encoding_map = {
                    "gpt-4": "cl100k_base",
                    "gpt-4o": "o200k_base",
                    "gpt-4-turbo": "cl100k_base",
                    "gpt-3.5-turbo": "cl100k_base",
                    "text-embedding-ada-002": "cl100k_base",
                }
                encoding_name = encoding_map.get(self.model_name, "cl100k_base")
                self._tiktoken_encoder = tiktoken.get_encoding(encoding_name)
            except ImportError:
                raise TokenizationError(
                    "tiktoken not installed. Install with: pip install tiktoken"
                )

        elif self.backend == TokenizerBackend.HUGGINGFACE:
            try:
                from transformers import AutoTokenizer
                # Use a default model if none specified
                model = "gpt2" if self.model_name is None else self.model_name
                self._hf_tokenizer = AutoTokenizer.from_pretrained(model)
            except ImportError:
                raise TokenizationError(
                    "transformers not installed. Install with: pip install transformers"
                )

    def count(self, text: str) -> int:
        """Count tokens in text."""
        if self.backend == TokenizerBackend.TIKTOKEN and self._tiktoken_encoder:
            return len(self._tiktoken_encoder.encode(text))
        elif self.backend == TokenizerBackend.HUGGINGFACE and self._hf_tokenizer:
            return len(self._hf_tokenizer.encode(text, add_special_tokens=False))
        else:
            # Fallback: rough approximation (1 token ~= 0.75 words)
            return int(len(text.split()) / 0.75)

    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs."""
        if self.backend == TokenizerBackend.TIKTOKEN and self._tiktoken_encoder:
            return self._tiktoken_encoder.encode(text)
        elif self.backend == TokenizerBackend.HUGGINGFACE and self._hf_tokenizer:
            return self._hf_tokenizer.encode(text, add_special_tokens=False)
        else:
            raise TokenizationError("No tokenizer backend available")

    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text."""
        if self.backend == TokenizerBackend.TIKTOKEN and self._tiktoken_encoder:
            return self._tiktoken_encoder.decode(token_ids)
        elif self.backend == TokenizerBackend.HUGGINGFACE and self._hf_tokenizer:
            return self._hf_tokenizer.decode(token_ids, skip_special_tokens=True)
        else:
            raise TokenizationError("No tokenizer backend available")

    def truncate(self, text: str, max_tokens: int) -> str:
        """Truncate text to max_tokens."""
        tokens = self.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.decode(tokens[:max_tokens])
