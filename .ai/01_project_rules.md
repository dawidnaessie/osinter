# Zasady Projektu OSINT Scanner

## Stack Technologiczny
- Język: Python 3.11+
- Interfejs CLI: Biblioteka `rich` (dla pięknych kolorów i tabel w terminalu) oraz `typer` (do obsługi argumentów).
- Zapytania HTTP: Biblioteka `httpx` (zamiast starego `requests`), najlepiej asynchronicznie (`asyncio`).
- Zarządzanie środowiskiem: `python-dotenv` do ładowania kluczy z pliku .env.

## Zasady Kodowania
1. Zawsze używaj Type Hints (np. `def check_email(email: str) -> dict:`).
2. Obsługuj błędy API (Rate limits - kod 429, brak autoryzacji - kod 401).
3. Nigdy nie hardkoduj kluczy API. Zawsze pobieraj je przez `os.getenv()`.
4. Kod musi być modularny – każdy plik w folderze `src/api/` odpowiada tylko za jedno API.