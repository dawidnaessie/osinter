# Architektura Systemu OSINT Scanner

## Przepływ Danych (Data Flow)
Aplikacja działa w architekturze warstwowej. Przepływ danych wygląda następująco:
1. **UI (src/main.py):** Przyjmuje dane od użytkownika (np. adres e-mail) i przekazuje je do warstwy Core. Zajmuje się wyłącznie rysowaniem tabel i kolorowaniem tekstu.
2. **Core (src/core/analyzer.py):** Mózg operacji (Agregator). Używa `utils/validators.py` do upewnienia się, czy cel to np. e-mail, czy domena. Następnie wywołuje odpowiednie moduły z warstwy API. Łączy surowe wyniki w jeden ustandaryzowany format.
3. **API (src/api/*.py):** "Robotnicy". Moduły odpowiedzialne WYŁĄCZNIE za komunikację HTTP z zewnętrznymi serwisami.

## Obsługa Błędów
- Warstwa **API** przechwytuje błędy sieciowe (np. brak internetu, limit zapytań) i zwraca ustandaryzowany słownik z błędem, np.: `{"status": "error", "message": "Rate limit exceeded"}`.
- Warstwa **Core** nie przerywa działania całego skanowania, gdy tylko jedno z API zawiedzie. Zapisuje błąd i pozwala reszcie skanerów działać dalej.

## Zasada Niezależności (Loose Coupling)
Moduły wewnątrz `src/api/` absolutnie nie mogą komunikować się ze sobą. Jeśli program sprawdza e-mail w dwóch różnych serwisach, to `analyzer.py` nimi zarządza i uruchamia je równolegle.