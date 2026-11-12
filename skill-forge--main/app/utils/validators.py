
import re


def validate_email(email: str) -> bool:
    """Return True if the email has a valid basic format."""
    if not isinstance(email, str):
        return False

    email = email.strip()

    if len(email) > 254:
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.fullmatch(pattern, email))


def validate_password(password: str) -> bool:
    """
    Check basic password strength.

    Requires at least 8 characters, one uppercase letter,
    one lowercase letter, one digit, and one special character.
    """
    if not isinstance(password, str) or len(password) < 8:
        return False

    return (
        bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[a-z]", password))
        and bool(re.search(r"\d", password))
        and bool(re.search(r"[^A-Za-z0-9]", password))
    )


def validate_non_empty_string(value: str) -> bool:
    """Check that a value is a non-empty string."""
    return isinstance(value, str) and bool(value.strip())


def validate_positive_integer(value) -> bool:
    """Check that a value is a positive integer, excluding booleans."""
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and value > 0
    )


def validate_score(score) -> bool:
    """Check whether a score is numeric and between 0 and 100."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return False

    return 0 <= score <= 100
