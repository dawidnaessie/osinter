"""
Moduł walidacji celów wejściowych (e-mail, IPv4, domena) dla OSINT Scanner.
Wykorzystuje wstępnie skompilowane wyrażenia regularne (regex) dla maksymalnej wydajności.
"""

import re

# Wstępnie skompilowane wzorce regex dla optymalizacji wydajności
_EMAIL_PATTERN: re.Pattern[str] = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

_IPV4_PATTERN: re.Pattern[str] = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
)

_DOMAIN_PATTERN: re.Pattern[str] = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
)


def is_valid_email(target: str) -> bool:
    """
    Sprawdza, czy podany ciąg znaków jest poprawnym adresem e-mail.

    Args:
        target: Ciąg znaków do walidacji.

    Returns:
        True, jeśli format adresu e-mail jest poprawny, w przeciwnym razie False.
    """
    if not isinstance(target, str) or not target:
        return False
    return bool(_EMAIL_PATTERN.fullmatch(target.strip()))


def is_valid_ip(target: str) -> bool:
    """
    Sprawdza, czy podany ciąg znaków jest poprawnym adresem IPv4 (zakres 0.0.0.0 - 255.255.255.255).

    Args:
        target: Ciąg znaków do walidacji.

    Returns:
        True, jeśli format adresu IPv4 jest poprawny, w przeciwnym razie False.
    """
    if not isinstance(target, str) or not target:
        return False
    return bool(_IPV4_PATTERN.fullmatch(target.strip()))


def is_valid_domain(target: str) -> bool:
    """
    Sprawdza, czy podany ciąg znaków jest poprawną nazwą domeny.

    Args:
        target: Ciąg znaków do walidacji.

    Returns:
        True, jeśli format nazwy domeny jest poprawny, w przeciwnym razie False.
    """
    if not isinstance(target, str) or not target:
        return False
    return bool(_DOMAIN_PATTERN.fullmatch(target.strip()))
