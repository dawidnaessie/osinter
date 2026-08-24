# Specyfikacje Darmowych Źródeł Danych

## 1. Pwned Passwords API (Darmowe, bez klucza)
- **Cel:** Sprawdzanie ile razy dane hasło wyciekło do sieci.
- **Endpoint:** `GET https://api.pwnedpasswords.com/range/{pierwsze_5_znakow_sha1}`
- **Zasada działania:** Model k-anonymity (wysyłamy tylko 5 pierwszych znaków skrótu SHA-1 hasła).

## 2. IP-API (Darmowe, bez klucza)
- **Cel:** Geolokalizacja adresu IP / domeny.
- **Endpoint:** `GET http://ip-api.com/json/{query}`

## 3. Integracja Holehe (Biblioteka Python)
- **Cel:** Sprawdzanie obecności e-maila w ponad 100 serwisach społecznościowych.
- **Użycie:** Poprzez pakiet Pythona `holehe`.

## 4. Hunter.io API (Darmowy plan)
- **Cel:** Wyszukiwanie adresów e-mail powiązanych z konkretną domeną (np. firma.pl).
- **Endpoint:** `GET https://api.hunter.io/v2/domain-search?domain={domain}&api_key={api_key}`
- **Zasada działania:** Wymaga klucza z pliku .env.