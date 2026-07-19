"""Structural compression strategy.

Compresses by removing formatting noise, whitespace, comments,
and simplifying structured data (JSON, XML, code) while preserving
structural integrity.
"""

import re
import json
from typing import Optional, List

from prompt_bonsai.compressors.base import BaseCompressor
from prompt_bonsai.config import CompressionConfig


class StructuralCompressor(BaseCompressor):
    """Compress prompts by optimizing structure and formatting."""

    def __init__(self, config: Optional[CompressionConfig] = None) -> None:
        super().__init__(config)
        self._last_iterations = 1

    def _compress_impl(
        self,
        text: str,
        target_tokens: int,
        preserve_patterns: Optional[List[str]] = None,
    ) -> str:
        """Compress by optimizing structure."""
        compressed = text
        iteration = 0
        max_iter = self.config.max_iterations

        while (
            self.tokenizer.count(compressed) > target_tokens
            and iteration < max_iter
        ):
            iteration += 1

            # Phase 1: Remove extra whitespace
            compressed = self._normalize_whitespace(compressed)

            # Phase 2: Minimize JSON/XML if present
            compressed = self._minimize_structured_data(compressed)

            # Phase 3: Remove comments
            compressed = self._remove_comments(compressed)

            # Phase 4: Simplify markdown
            compressed = self._simplify_markdown(compressed)

            # Phase 5: Remove decorative characters
            if iteration >= 2:
                compressed = self._remove_decorations(compressed)

            if self.tokenizer.count(compressed) <= target_tokens:
                break

        self._last_iterations = iteration
        return compressed.strip()

    def _normalize_whitespace(self, text: str) -> str:
        """Normalize whitespace while preserving paragraph breaks."""
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        # Replace multiple newlines with double newline
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove leading/trailing whitespace per line
        lines = [line.strip() for line in text.split('\n')]
        return '\n'.join(lines)

    def _minimize_structured_data(self, text: str) -> str:
        """Minimize JSON and XML content."""
        # Try to find and minimize JSON blocks
        def minimize_json(match: re.Match) -> str:
            try:
                data = json.loads(match.group(1))
                return json.dumps(data, separators=(',', ':'))
            except json.JSONDecodeError:
                return match.group(0)

        # Match JSON in code blocks or inline
        text = re.sub(
            r'```json\n(.*?)\n```',
            lambda m: '```json\n' + minimize_json(m) + '\n```',
            text,
            flags=re.DOTALL,
        )

        # Match inline JSON
        text = re.sub(
            r'\{[^{}]*\}',
            lambda m: minimize_json(m),
            text,
        )

        # Minimize XML by removing extra whitespace between tags
        text = re.sub(r'>\s+<', '><', text)

        return text

    def _remove_comments(self, text: str) -> str:
        """Remove code comments while preserving code."""
        # Python-style comments (but not in URLs)
        text = re.sub(r'(?<!:)//.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'#\s+.*$', '', text, flags=re.MULTILINE)

        # Block comments (simple heuristic)
        text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)

        # HTML comments
        text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

        return text

    def _simplify_markdown(self, text: str) -> str:
        """Simplify markdown formatting."""
        # Convert headers to simpler forms if too many levels
        text = re.sub(r'^#{4,}\s+', '**', text, flags=re.MULTILINE)

        # Simplify horizontal rules
        text = re.sub(r'\n---\n', '\n\n', text)
        text = re.sub(r'\n\*\*\*\n', '\n\n', text)

        # Remove extra blank lines between list items
        text = re.sub(r'(- .+)\n\n(- )', r'\1\n\2', text)

        return text

    def _remove_decorations(self, text: str) -> str:
        """Remove decorative characters and ASCII art."""
        # Remove lines that are mostly decorative characters
        lines = text.split('\n')
        cleaned = []
        for line in lines:
            stripped = line.strip()
            # Skip lines that are just repeated characters
            if re.match(r'^[\-\=\*\#\~\+]{3,}$', stripped):
                continue
            # Skip ASCII art lines (high ratio of non-alphanumeric)
            if len(stripped) > 10:
                non_alpha = sum(1 for c in stripped if not c.isalnum() and not c.isspace())
                if non_alpha / len(stripped) > 0.7:
                    continue
            cleaned.append(line)

        return '\n'.join(cleaned)
