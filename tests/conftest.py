"""Pytest configuration and fixtures for prompt-bonsai tests."""

import pytest

from prompt_bonsai import Compressor
from prompt_bonsai.config import CompressionConfig, CompressionStrategy


@pytest.fixture
def long_prompt():
    """Return a long prompt for testing."""
    return """
    I would like to request your assistance with a very important task. 
    Please, if you could, help me understand the following complex topic 
    in a way that is clear and concise. I am wondering if you might be 
    able to explain the fundamental principles of quantum mechanics, 
    including but not limited to wave-particle duality, the uncertainty 
    principle, and quantum entanglement. It would be great if you could 
    provide specific examples and analogies to make the concepts more 
    accessible. Thank you very much in advance for your help with this matter.
    """ * 5  # Make it longer for meaningful compression


@pytest.fixture
def structured_prompt():
    """Return a structured prompt with JSON and code."""
    return """
    Please analyze the following data and provide insights:

    ```json
    {
        "users": [
            {
                "id": 1,
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "role": "administrator",
                "created_at": "2023-01-15T10:30:00Z"
            },
            {
                "id": 2,
                "name": "Bob Smith",
                "email": "bob@example.com",
                "role": "user",
                "created_at": "2023-02-20T14:45:00Z"
            }
        ]
    }
    ```

    Here is the Python code to process this:

    ```python
    # This function processes user data
    def process_users(users):
        # Iterate through each user
        for user in users:
            # Print user information
            print(f"User: {user['name']}")
            # Check if user is admin
            if user['role'] == 'administrator':
                # Grant special permissions
                grant_permissions(user)
    ```

    Could you please review this and suggest improvements? Thank you!
    """


@pytest.fixture
def compressor():
    """Return a default compressor instance."""
    return Compressor(strategy="hybrid", target_ratio=0.3)


@pytest.fixture
def semantic_compressor():
    """Return a semantic compressor instance."""
    return Compressor(strategy="semantic", target_ratio=0.3)


@pytest.fixture
def structural_compressor():
    """Return a structural compressor instance."""
    return Compressor(strategy="structural", target_ratio=0.3)
