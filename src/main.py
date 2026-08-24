"""
Główny punkt wejścia aplikacji OSINT Deep Scanner.
Odpowiada za interfejs CLI, formatowanie i prezentację wyników.
"""

import asyncio
from pathlib import Path
import sys
from typing import Any, Dict

# Wymuszenie kodowania UTF-8 dla konsoli Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Zapewnienie poprawnej ścieżki do importów modułów projektu
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import typer

from src.core.analyzer import analyze_target

app = typer.Typer(
    name="osint-scanner",
    help="OSINT Deep Scanner - Szybkie rozpoznanie celów (IP / Domeny)",
    add_completion=False,
)
console = Console()


def display_welcome_banner(target: str) -> None:
    """Wyświetla panel powitalny w hakerskim stylu."""
    banner_content = Text()
    banner_content.append("=== OSINT DEEP SCANNER v1.0.0 ===\n", style="bold green")
    banner_content.append("Pasywny zwiad i analiza celow sieciowych\n", style="dim green")
    banner_content.append("---------------------------------------------\n", style="green")
    banner_content.append("[+] Cel skanowania: ", style="bold cyan")
    banner_content.append(f"{target}\n", style="bold yellow")
    banner_content.append("[+] Status: ", style="bold cyan")
    banner_content.append("INICJALIZACJA SILNIKA ANALIZY", style="bold green")

    panel = Panel(
        banner_content,
        title="[bold green] OSINT DEEP SCANNER [/bold green]",
        subtitle="[bold dim green]SYSTEM RECONNAISSANCE[/bold dim green]",
        border_style="green",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def display_geolocation_table(geo_result: Dict[str, Any]) -> None:
    """Rysuje tabelę z danymi geolokalizacyjnymi."""
    if geo_result.get("status") == "error":
        console.print(
            Panel(
                f"[bold yellow][!] {geo_result.get('message', 'Nie udalo sie pobrac danych geolokalizacji')}[/bold yellow]",
                title="[bold yellow]GEOLOKALIZACJA IP[/bold yellow]",
                border_style="yellow",
            )
        )
        return

    data = geo_result.get("data", {})
    table = Table(
        title="[bold green]>> WYNIKI GEOLOKALIZACJI IP <<[/bold green]",
        border_style="green",
        header_style="bold green",
        show_lines=True,
    )

    table.add_column("Parametr", style="cyan", no_wrap=True)
    table.add_column("Wartosc", style="bold white")

    table.add_row("Adres IP / Host", str(data.get("query", "N/A")))
    table.add_row("Kraj", f"{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})")
    table.add_row("Region i Miasto", f"{data.get('regionName', '')}, {data.get('city', 'N/A')}".strip(", "))
    table.add_row("Kod pocztowy", str(data.get("zip", "N/A")))
    table.add_row("Koordynaty (Lat, Lon)", f"{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
    table.add_row("Dostawca internetu (ISP)", str(data.get("isp", "N/A")))
    table.add_row("Organizacja / AS", f"{data.get('org', '')} ({data.get('as', 'N/A')})".strip())
    table.add_row("Strefa czasowa", str(data.get("timezone", "N/A")))

    console.print(table)
    console.print()


def display_hunter_section(hunter_result: Dict[str, Any]) -> None:
    """Rysuje sekcje Hunter.io i liste znalezionych adresow e-mail."""
    if hunter_result.get("status") == "error":
        console.print(
            Panel(
                f"[bold yellow][!] {hunter_result.get('message', 'Nie udalo sie pobrac danych z Hunter.io')}[/bold yellow]",
                title="[bold yellow]HUNTER.IO INFO[/bold yellow]",
                border_style="yellow",
            )
        )
        return

    data = hunter_result.get("data", {})
    emails_list = data.get("emails", [])

    if emails_list:
        console.print(
            Panel(
                f"[bold red][!] WYKRYTO ZNANE ADRESY E-MAIL W DOMENIE ({len(emails_list)})[/bold red]",
                border_style="red",
                style="bold red",
            )
        )

        table = Table(
            title=f"[bold cyan]>> ZNALEZIONE ADRESY E-MAIL ({len(emails_list)}) <<[/bold cyan]",
            border_style="cyan",
            header_style="bold cyan",
            show_lines=True,
        )

        table.add_column("Adres E-mail", style="bold yellow")
        table.add_column("Imie i Nazwisko", style="white")
        table.add_column("Stanowisko / Dzial", style="green")
        table.add_column("Pewnosc (Confidence)", justify="center", style="magenta")

        for email in emails_list:
            first_name = email.get("first_name") or ""
            last_name = email.get("last_name") or ""
            full_name = f"{first_name} {last_name}".strip() or "Brak danych"

            position = email.get("position") or email.get("department") or "Brak danych"
            confidence = f"{email.get('confidence', 0)}%"

            table.add_row(
                str(email.get("value", "N/A")),
                full_name,
                position,
                confidence,
            )

        console.print(table)
        console.print()
    else:
        console.print(
            Panel(
                "[bold green][+] Nie wykryto publicznie dostepnych adresow e-mail dla tej domeny w bazie Hunter.io.[/bold green]",
                title="[bold green]HUNTER.IO WYNIK[/bold green]",
                border_style="green",
            )
        )
        console.print()


@app.command()
def scan(
    target: str = typer.Argument(
        ...,
        help="Cel skanowania: poprawny adres IPv4 (np. 8.8.8.8) lub domena (np. example.com)",
    ),
) -> None:
    """
    Skanuje podany cel i prezentuje zebrane dane wywiadowcze w terminalu.
    """
    display_welcome_banner(target)

    # Uruchomienie analizy z animowanym spinnerem
    with console.status(
        "[bold cyan]Inicjalizacja skanowania i zbieranie danych...[/bold cyan]",
        spinner="dots",
    ):
        result = asyncio.run(analyze_target(target))

    # Obsluga bledu formatu celu
    if result.get("status") == "error":
        console.print(
            Panel(
                f"[bold red][X] BLAD: {result.get('message', result.get('error', 'Niepoprawny cel skanowania'))}[/bold red]",
                title="[bold red]BLAD SKANOWANIA[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
        )
        raise typer.Exit(code=1)

    # Prezentacja danych geolokalizacji
    if "geolocation" in result:
        display_geolocation_table(result["geolocation"])

    # Prezentacja danych Hunter.io (dla domen)
    if "emails" in result:
        display_hunter_section(result["emails"])

    console.print(
        Panel(
            "[bold green][+] Skanowanie zakonczone pomyslnie.[/bold green]",
            border_style="green",
            style="green",
        )
    )


if __name__ == "__main__":
    app()
