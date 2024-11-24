from typing import Optional


def format_response(response: str) -> str:
    """Format the chatbot response."""
    return response.strip()


def validate_prompt(prompt: str) -> bool:
    """Validate the input prompt."""
    return bool(prompt and prompt.strip())


def sanitize_input(prompt: str) -> Optional[str]:
    """
    Sanitize user input by removing unwanted characters and limiting length.
    Returns None if input is invalid.
    """
    if not prompt:
        return None

    # Remove leading/trailing whitespace
    cleaned = prompt.strip()

    # Check length
    if len(cleaned) < 3:  # Minimum length
        return None
    if len(cleaned) > 1000:  # Maximum length
        cleaned = cleaned[:1000]

    return cleaned