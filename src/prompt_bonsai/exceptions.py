"""Custom exceptions for prompt-bonsai."""


class PromptBonsaiError(Exception):
    """Base exception for all prompt-bonsai errors."""
    pass


class CompressionError(PromptBonsaiError):
    """Raised when compression fails."""
    pass


class QualityError(PromptBonsaiError):
    """Raised when compressed prompt fails quality checks."""
    pass


class TokenizationError(PromptBonsaiError):
    """Raised when tokenization fails."""
    pass


class StrategyError(PromptBonsaiError):
    """Raised when an invalid strategy is specified."""
    pass


class ConfigurationError(PromptBonsaiError):
    """Raised when configuration is invalid."""
    pass
