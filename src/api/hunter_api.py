"""
Moduł integracji z Hunter.io API (wyszukiwanie adresów e-mail w domenie).
"""

import os
from dotenv import load_dotenv
import httpx

load_dotenv()


async def get_hunter_data(domain: str) -> dict:
    """
    Wysyła asynchroniczne zapytanie do Hunter.io API w celu znalezienia adresów e-mail powiązanych z domeną.

    Args:
        domain: Nazwa domeny do przeskanowania.

    Returns:
        Słownik ze statusem oraz danymi z Hunter.io lub informacją o błędzie.
    """
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "message": "Brak klucza HUNTER_API_KEY w zmiennych środowiskowych (.env)",
        }

    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

            if response.status_code == 401:
                return {
                    "status": "error",
                    "message": "Brak autoryzacji: Niepoprawny klucz Hunter.io API (HTTP 401)",
                }
            elif response.status_code == 429:
                return {
                    "status": "error",
                    "message": "Przekroczono limit zapytań Hunter.io API (Rate limit - HTTP 429)",
                }
            elif response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Błąd Hunter.io API (HTTP {response.status_code})",
                }

            data = response.json()
            return {
                "status": "success",
                "data": data.get("data", data),
            }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Przekroczono czas oczekiwania na odpowiedź z Hunter.io API (Timeout)",
        }
    except httpx.RequestError as exc:
        return {
            "status": "error",
            "message": f"Błąd połączenia sieciowego z Hunter.io: {str(exc)}",
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Wystąpił nieoczekiwany błąd: {str(exc)}",
        }
