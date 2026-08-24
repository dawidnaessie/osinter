"""
Moduł integracji z IP-API (geolokalizacja adresów IP).
"""

import httpx


async def get_ip_data(target: str) -> dict:
    """
    Wysyła asynchroniczne zapytanie do serwisu IP-API w celu pobrania danych geolokalizacyjnych.

    Args:
        target: Adres IP lub nazwa hosta do geolokalizacji.

    Returns:
        Słownik ze statusem oraz danymi geolokalizacyjnymi lub informacją o błędzie.
    """
    url = f"http://ip-api.com/json/{target}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

            if response.status_code == 429:
                return {
                    "status": "error",
                    "message": "Przekroczono limit zapytań (Rate limit - HTTP 429)",
                }
            elif response.status_code == 401:
                return {
                    "status": "error",
                    "message": "Brak autoryzacji (HTTP 401)",
                }
            elif response.status_code != 200:
                return {
                    "status": "error",
                    "message": f"Błąd serwera HTTP {response.status_code}",
                }

            data = response.json()
            if data.get("status") == "fail":
                return {
                    "status": "error",
                    "message": data.get("message", "Nie udało się zlokalizować celu"),
                }

            return {
                "status": "success",
                "data": data,
            }

    except httpx.TimeoutException:
        return {
            "status": "error",
            "message": "Przekroczono czas oczekiwania na odpowiedź z IP-API (Timeout)",
        }
    except httpx.RequestError as exc:
        return {
            "status": "error",
            "message": f"Błąd połączenia sieciowego: {str(exc)}",
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Wystąpił nieoczekiwany błąd: {str(exc)}",
        }
