# 🕵️‍♂️ OSINT Deep Scanner

Nowoczesne, asynchroniczne narzędzie CLI do białego wywiadu (OSINT) i szybkiego profilowania celów sieciowych. Zaprojektowane z myślą o maksymalnej czytelności w terminalu oraz architekturze "AI-First".

Narzędzie automatycznie analizuje podany cel (adres IP lub domenę), odpowiednio dobiera moduły skanujące i prezentuje wyniki w formie czytelnych, "hakerskich" tabel w terminalu.

## ✨ Główne funkcje

* **Inteligentny Routing:** Automatyczne rozpoznawanie typu celu (IP vs Domena) za pomocą wyrażeń regularnych i kierowanie do odpowiednich modułów API.
* **Geolokalizacja IP:** Precyzyjne namierzanie fizycznej lokalizacji serwerów, miast oraz dostawców ISP (via IP-API).
* **Firmowy Ślad Cyfrowy:** Wyszukiwanie publicznie dostępnych adresów e-mail powiązanych z daną domeną (via Hunter.io).
* **Hollywood UI:** Zaawansowany, asynchroniczny interfejs terminalowy budowany w oparciu o bibliotekę `rich` (animowane spinnery, kolorowe tabele, ostrzeżenia o zagrożeniach).
* **AI-Ready Architecture:** Projekt zawiera specjalny folder `.ai` z pełnym kontekstem dla agentów programistycznych.

## 🚀 Wymagania

* Python 3.11 lub nowszy
* Darmowy klucz API z serwisu [Hunter.io](https://hunter.io/)

## ⚙️ Instalacja i Konfiguracja

Krok 1: Sklonuj repozytorium
```bash
git clone [https://github.com/dawidnaessie/osinter.git](https://github.com/dawidnaessie/osinter.git)
cd osinter
```
Krok 2: Utwórz i aktywuj wirtualne środowisko
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```
Krok 3: Zainstaluj wymagane biblioteki
```bash
pip install httpx rich typer python-dotenv holehe
```
Krok 4: Skonfiguruj klucze API
Utwórz plik .env w głównym katalogu projektu i dodaj swój klucz Hunter API:
```bash
HUNTER_API_KEY=twój_klucz_api_tutaj
```
