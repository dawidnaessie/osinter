"""
Moduł główny analizy i agregacji danych OSINT (Core Analyzer).
Odpowiada za walidację celu, koordynację wywołań asynchronicznych do API oraz agregację wyników.
"""

import asyncio
from typing import Any, Dict

from src.api.hunter_api import get_hunter_data
from src.api.ip_geolocation import get_ip_data
from src.utils.validators import is_valid_domain, is_valid_email, is_valid_ip


async def analyze_target(target: str) -> Dict[str, Any]:
    """
    Główna funkcja analizująca cel (adres IP lub domenę).
    Rozpoznaje typ celu, wykonuje odpowiednie zapytania do API (w tym równolegle)
    i łączy wyniki w ustandaryzowany słownik.

    Args:
        target: Ciąg znaków reprezentujący cel do analizy (np. '8.8.8.8' lub 'example.com').

    Returns:
        Słownik ze strukturą zagregowanych wyników lub informacją o błędzie.
    """
    if not isinstance(target, str) or not target.strip():
        return {
            "status": "error",
            "message": "Nierozpoznany format celu (pusty parametr)",
            "error": "Nierozpoznany format celu",
        }

    clean_target = target.strip()

    # 1. Scenariusz: Cel to adres IPv4
    if is_valid_ip(clean_target):
        geo_result = await get_ip_data(clean_target)
        return {
            "status": "success",
            "target": clean_target,
            "target_type": "ip",
            "geolocation": geo_result,
        }

    # 2. Scenariusz: Cel to Domena (agregacja równoległa Hunter.io + geolokalizacja)
    if is_valid_domain(clean_target):
        hunter_result, geo_result = await asyncio.gather(
            get_hunter_data(clean_target),
            get_ip_data(clean_target),
        )

        return {
            "status": "success",
            "target": clean_target,
            "target_type": "domain",
            "emails": hunter_result,
            "geolocation": geo_result,
        }

    # 3. Scenariusz: Nierozpoznany format celu
    return {
        "status": "error",
        "message": "Nierozpoznany format celu (oczekiwano poprawnego adresu IPv4 lub domeny)",
        "error": "Nierozpoznany format celu",
    }
