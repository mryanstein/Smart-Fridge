# FridgeManager: przewodnik dewelopera

Notatka dla nas, autorów projektu. Prowadzi krok po kroku od pustego folderu do wydania `v1.0.0`. Przy każdym ważniejszym kroku jest wyjaśnienie, **po co** to robimy, bo celem jest nie tylko oddać projekt, ale też go zrozumieć i umieć obronić na prezentacji.

Stos: **Python + Flet** (interfejs), **pytest** (testy), **uv** (środowisko), **GitHub Actions** (CI/CD), **VS Code** (edytor).

## Spis treści

- [Jak otwierać te notatki](#jak-otwierać-te-notatki)
- [Co budujemy](#co-budujemy)
- [Architektura](#architektura)
- [Etap 0: Przygotowanie](#etap-0-przygotowanie)
- [Etap 1: wersja v0.1.0](#etap-1-wersja-v010)
- [Etap 2: wersja v0.2.0](#etap-2-wersja-v020)
- [Etap 3: wersja v1.0.0](#etap-3-wersja-v100)
- [Jak pisać testy](#jak-pisać-testy)
- [Git i praca w zespole](#git-i-praca-w-zespole)
- [Prezentacja](#prezentacja)
- [Rozwiązywanie problemów](#rozwiązywanie-problemów)
- [Checklista wymagań prowadzącego](#checklista-wymagań-prowadzącego)

## Jak otwierać te notatki

Wszystkie notatki to zwykły Markdown (`.md`) bez elementów specyficznych dla Obsidiana (bez `> [!tip]`, `[[linków]]` i `%%komentarzy%%`), więc wyglądają tak samo w VS Code i na GitHubie.

- **VS Code:** otwórz plik i naciśnij `Ctrl+Shift+V` (podgląd w nowej karcie) albo `Ctrl+K`, potem `V` (podgląd obok edytora). Podgląd odświeża się na bieżąco.
- **Diagramy Mermaid** (są w `README.md`): GitHub rysuje je sam. VS Code potrzebuje rozszerzenia **Markdown Preview Mermaid Support**.
- **Spis treści:** panel **Outline** w Eksploratorze albo `Ctrl+Shift+O` pokazuje nagłówki pliku.
- **Checkboxy** `- [ ]`: w podglądzie są tylko wyświetlane. Odhaczamy je w edytorze, zamieniając `[ ]` na `[x]`, i commitujemy. Jeśli wolicie klikać, użyjcie zakładki **Projects** lub **Issues** na GitHubie.
- **Bloki kodu** mają przycisk kopiowania na GitHubie. W VS Code zaznacz i skopiuj.

W tej notatce:

> 💡 **Po co to?** oznacza krótkie wyjaśnienie, dlaczego robimy dany krok.

**Commit:** podpowiada przykładowy opis commita. **Gotowe, gdy** to lista warunków zakończenia kroku.

## Co budujemy

FridgeManager to aplikacja desktopowa (Flet), która:

1. **Kontroluje zawartość lodówki.** Stan rośnie, gdy zatwierdzamy zakupy z listy, i maleje, gdy gotujemy przepis.
2. **Generuje listę zakupów dla przepisu.** Porównuje to, czego przepis potrzebuje, z tym, co jest w lodówce, i podaje tylko braki.
3. **Ma dodatki** poprawiające wygodę: kalorie i dziennik, jednostki kuchenne, opakowania itd.

### Podział na mniejsze części

| # | Część | Co robi | Wersja |
| :--- | :--- | :--- | :--- |
| A | Jednostki i ilości | `Unit`, `Quantity`: poprawne ilości, przeliczanie g↔kg, ml↔l | v0.1.0 |
| B | Produkty | `FoodItem` i trzy klasy pochodne: jak przeliczyć ilość na bazową i na gramy | v0.1.0 |
| C | Lodówka | `Fridge`: dodawanie, zużywanie, sprawdzanie stanu | v0.1.0 |
| D | Interfejs: lodówka | widok listy produktów i formularz dodawania | v0.1.0 |
| E | Infrastruktura | testy, CI, paczka `.exe`, wydanie | v0.1.0 |
| F | Przepisy | `Recipe`: składniki na 1 porcję, przeliczanie na N porcji | v0.2.0 |
| G | Lista zakupów | `ShoppingList`: czego brakuje do przepisu | v0.2.0 |
| H | Zapis danych | repozytorium (pamięć, JSON), dane przetrwają restart | v0.2.0 |
| I | Serwis | `CookingService`: zakupy (dodaje), gotowanie (odejmuje), lista zakupów | v0.2.0 |
| J | Interfejs: przepisy i zakupy | widoki przepisów, listy zakupów, przycisk „Ugotuj” | v0.2.0 |
| K | Kalorie i dziennik | kcal przepisu, dziennik dnia | v1.0.0 |
| L | Jednostki kuchenne | szklanka, łyżka, łyżeczka | v1.0.0 |
| M | Dodatki do wyboru | opakowania, wiele przepisów naraz, edycja i usuwanie, eksport listy | v1.0.0 (wg czasu) |
| N | Dokumentacja i prezentacja | README, diagram, mapa OOP, rejestr LLM | v1.0.0 |

> 💡 **Po co ten podział?** Część A–C to rdzeń: bez niego nic nie działa, a da się go w całości przetestować bez okna aplikacji. Wersje pośrednie mają być działające, nie kompletne. Jeśli zabraknie czasu, tniemy część M, potem L i K, a rdzeń (A–J) zostaje.

### Scenariusz referencyjny (nasz „test akceptacyjny”)

Ten scenariusz opisuje, jak ma działać gotowa aplikacja. W etapie 2 zamienimy go w automatyczny test.

1. Dodajemy produkty: **mleko** (na objętość, ml), **mąka** (na wagę, g), **jajko** (na sztuki, 1 sztuka ≈ 55 g).
2. Kupujemy 1 l mleka. Lodówka: **mleko 1000 ml**.
3. Dodajemy przepis **Naleśniki** (na 1 porcję): 100 ml mleka, 60 g mąki, 1 jajko.
4. Prosimy o listę zakupów dla **2 porcji**. Potrzeba: 200 ml mleka, 120 g mąki, 2 jajek. W lodówce jest tylko mleko, więc lista to: **mąka 120 g, jajka 2 szt.** (mleka nie ma na liście, bo jest go dość).
5. Zatwierdzamy zakupy. Lodówka: mleko 1000 ml, mąka 120 g, jajka 2 szt.
6. Gotujemy 2 porcje. Lodówka: **mleko 800 ml**, a mąka i jajka znikają (zero).
7. Próbujemy ugotować 2 porcje jeszcze raz. Aplikacja zgłasza `InsufficientStockError`, a stan lodówki się **nie zmienia** (mleko nadal 800 ml).

## Architektura

### Warstwy i zasada zależności

```text
ui/        →  storage/  →  domain/
(Flet)        (JSON,        (logika, klasy, wyjątki)
               pamięć)
```

Strzałka znaczy „może importować”. `domain/` **nie importuje niczego** z `ui/` ani `storage/` i **nie używa** `flet`, `print()`, `input()` ani plików.

> 💡 **Po co?** Logikę (np. „czy starczy mleka”) testujemy w pytest w milisekundach, bez okna i bez dysku. Interfejs można przepisać (np. z Flet na terminal) bez ruszania logiki. A na prezentacji łatwo pokazać, że projekt ma czystą architekturę.

### Struktura folderów

```text
fridge-manager/
├── .github/workflows/
│   ├── test.yml
│   └── release.yml
├── docs/
│   ├── PRZEWODNIK_DEWELOPERA.md
│   └── WYMAGANIA_PROJEKTU.md
├── src/
│   ├── main.py                    # punkt wejścia Flet
│   └── fridge_manager/
│       ├── __init__.py
│       ├── domain/
│       │   ├── __init__.py
│       │   ├── errors.py          # wyjątki
│       │   ├── quantity.py        # Kind, Unit, Quantity
│       │   ├── food.py            # FoodItem, WeightItem, VolumeItem, PieceItem
│       │   ├── fridge.py          # StockItem, Fridge
│       │   ├── recipe.py          # RecipeIngredient, Recipe
│       │   ├── shopping.py        # ShoppingItem, ShoppingList
│       │   ├── journal.py         # JournalEntry, CalorieJournal (v1.0.0)
│       │   ├── app_data.py        # AppData
│       │   ├── repository.py      # StorageRepository (ABC)
│       │   └── service.py         # CookingService
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── memory_repository.py
│       │   ├── json_repository.py
│       │   ├── serialization.py
│       │   └── paths.py           # gdzie leży data.json
│       └── ui/
│           ├── __init__.py
│           ├── app.py             # main(page): składa widoki
│           ├── formatting.py      # np. 1000 ml → "1 l"
│           ├── fridge_view.py
│           ├── recipes_view.py
│           └── journal_view.py    # v1.0.0
├── tests/
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

### Skąd wiemy, że projekt spełnia wymagania OOP

Pełna tabela „koncepcja → klasy i pliki → uzasadnienie” jest w `README.md`. W skrócie, wszystkie 6 koncepcji ma uzasadnione miejsce:

| Koncepcja | Gdzie | Dlaczego tu |
| :--- | :--- | :--- |
| Hermetyzacja | `Fridge`, `StockItem` | ilość nie może spaść poniżej zera, a jednostki muszą pasować |
| Abstrakcja | `FoodItem`, `StorageRepository` | kod nie zależy od konkretnego rodzaju produktu ani od sposobu zapisu |
| Dziedziczenie | `WeightItem`, `VolumeItem`, `PieceItem`; hierarchia wyjątków | produkty różnią się danymi i przeliczaniem |
| Polimorfizm | `to_grams()`, `base_unit`, `load()/save()` | jeden kod obsługuje mleko, mąkę i jajka |
| Kompozycja | `Recipe` → `RecipeIngredient` → `Quantity`, `Fridge` → `StockItem` | obiekty z obiektów |
| Obsługa błędów | `DomainError` i potomkowie | interfejs łapie jeden typ i pokazuje komunikat |

> 💡 **Uwaga:** prowadzący pisze, że klasa istniejąca tylko „dla odhaczenia” się nie liczy. Hierarchia `FoodItem` jest uzasadniona tylko wtedy, gdy klasy pochodne **naprawdę** zachowują się inaczej (`to_grams()` i `base_unit`). Pilnujcie tego przy pisaniu kodu.

## Etap 0: Przygotowanie

Robicie to **razem** na jednym spotkaniu. Po nim oboje mają działające środowisko i identyczny punkt wyjścia.

### 0.1 Zainstalujcie narzędzia

Szczegóły (z poleceniami) są w `README.md`, sekcja „Środowisko deweloperskie”. Krótko: **Git**, **uv**, **VS Code**. Sprawdźcie:

```bash
git --version
uv --version
```

> 💡 **Po co uv?** Jedno narzędzie zastępuje kilka: instaluje Pythona (w wersji z `.python-version`), tworzy `.venv` i pilnuje zależności w pliku blokady `uv.lock`. Dzięki temu „u mnie działa” znaczy „u Ciebie też”, bo oboje macie dokładnie te same wersje bibliotek.

### 0.2 Rozszerzenia VS Code

Zainstalujcie: **Python**, **Pylance**, **Even Better TOML**, **Markdown Preview Mermaid Support**. Opcjonalnie: **GitHub Pull Requests**, **GitLens**, **Ruff**.

### 0.3 Repozytorium na GitHubie

1. Jedna osoba tworzy **puste** repozytorium `fridge-manager` (publiczne). Bez README, `.gitignore` i licencji, bo historia ma zaczynać się od pustego repozytorium.
2. Dodaje drugą osobę: `Settings → Collaborators → Add people`.
3. **Zgłoście temat na UPeL:** tytuł (np. „FridgeManager: asystent lodówki, przepisów i zakupów”), link do repozytorium i lista współpracowników.
4. Każda osoba ustawia swoją tożsamość w Gicie (inaczej historia nie pokaże wkładu każdego):
   ```bash
   git config --global user.name "Imię Nazwisko"
   git config --global user.email "adres-przypisany-do-konta-github@example.com"
   ```
5. Każdy klonuje repozytorium i otwiera folder w VS Code:
   ```bash
   git clone <LINK_DO_REPOZYTORIUM>
   cd fridge-manager
   code .
   ```

### 0.4 Plik `.gitignore` (pierwszy commit)

Utwórzcie `.gitignore`:

```text
# Python
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.ruff_cache/

# Środowisko wirtualne
.venv/

# Build (PyInstaller, Flet)
build/
dist/
*.spec

# IDE
.vscode/
.idea/

# Dane użytkownika i sekrety
data.json
.env

# System
.DS_Store
Thumbs.db
```

**Commit:** `Dodaj .gitignore`

> 💡 **Po co jako pierwszy?** Prowadzący wymaga braku plików IDE, wyników kompilacji i danych wrażliwych w repozytorium. Łatwiej niczego nie dodać niż potem czyścić historię. `.vscode/` jest tu ignorowany, więc konfigurację edytora robicie lokalnie (krok 0.7).

### 0.5 Projekt `uv`

1. Przypnijcie wersję Pythona (powstanie plik `.python-version`):
   ```bash
   uv python pin 3.12
   ```
2. Utwórzcie `pyproject.toml` (na razie bez zależności):
   ```toml
   [project]
   name = "fridge-manager"
   version = "0.1.0"
   description = "Asystent lodówki, przepisów i zakupów (Python + Flet)"
   requires-python = ">=3.10"
   dependencies = []

   [tool.pytest.ini_options]
   pythonpath = ["src"]
   testpaths = ["tests"]
   ```
3. Dodajcie zależności (polecenia same wpiszą je do `pyproject.toml` i utworzą `uv.lock`):
   ```bash
   uv add flet
   uv add --dev pytest flet-cli flet-desktop pyinstaller
   ```
4. Sprawdźcie, że środowisko działa: `uv run python --version` (ma pokazać 3.12.x).

**Commit:** `Dodaj konfigurację projektu uv i zależności`  (razem z `pyproject.toml`, `uv.lock`, `.python-version`).

> 💡 **Po co `pythonpath = ["src"]`?** Nasz kod leży w `src/fridge_manager/`. Ta linijka mówi pytest, żeby szukał pakietów w `src/`, więc w testach działa `from fridge_manager.domain.quantity import Quantity`.
>
> 💡 **Po co `flet-cli`, `flet-desktop`, `pyinstaller` jako `--dev`?** To narzędzia do uruchamiania okna deweloperskiego (`flet run`) i budowania `.exe`. Sam program potrzebuje tylko biblioteki `flet`.
>
> 💡 **Po co `uv.lock` w repozytorium?** To „zdjęcie” dokładnych wersji wszystkich bibliotek. CI instaluje z niego (`uv sync --locked`) i nie zmieni nic za naszymi plecami.

### 0.6 Struktura folderów i „Hello Flet”

1. Utwórzcie foldery i puste pliki `__init__.py` zgodnie ze strukturą z sekcji [Architektura](#architektura) (na razie wystarczą `src/fridge_manager/{domain,storage,ui}/__init__.py` oraz `tests/`).
2. Utwórzcie `src/main.py`:
   ```python
   import flet as ft


   def main(page: ft.Page) -> None:
       page.title = "FridgeManager"
       page.add(ft.Text("Hello, FridgeManager!"))


   if __name__ == "__main__":
       ft.run(main)
   ```
3. Uruchomcie:
   ```bash
   uv run flet run src/main.py
   ```
   Powinno otworzyć się okno z napisem. Zmieńcie tekst i zapiszcie plik. Okno odświeży się samo (hot reload).

> ⚠️ **Flet szybko się zmienia.** W poradnikach z internetu spotkacie starsze API (np. `ft.app(target=main)`, `ft.ElevatedButton`, `page.snack_bar`). My używamy Flet 1.x (`ft.run(main)`, `ft.Button`). Gdy kontrolka „nie istnieje”, zajrzyjcie do [dokumentacji Flet](https://flet.dev/docs) w wersji zgodnej z `uv.lock` i do `uv run flet --version`. W tym przewodniku podaję szkielety i odpowiedzialności widoków, a nie każdy argument kontrolek.

### 0.7 Konfiguracja VS Code (lokalnie, nie w repo)

Utwórzcie folder `.vscode/` i dwa pliki. Są ignorowane przez Git, więc każdy robi to u siebie.

`.vscode/settings.json` (Windows):

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.analysis.extraPaths": ["src"]
}
```

Na macOS / Linux ścieżka interpretera to `${workspaceFolder}/.venv/bin/python`.

`.vscode/launch.json` (uruchamianie i debugowanie aplikacji klawiszem `F5`):

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FridgeManager (Flet)",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/src/main.py",
      "console": "integratedTerminal"
    }
  ]
}
```

Co z tego macie:

- **F5** uruchamia aplikację z debuggerem. Postawcie czerwony punkt przerwania obok numeru linii, żeby zobaczyć wartości zmiennych.
- Panel **Testing** (ikona kolby) pokazuje wszystkie testy, pozwala je uruchamiać pojedynczo i debugować.
- `python.analysis.extraPaths` sprawia, że Pylance rozumie importy z `src/` (bez żółtych podkreśleń).

### 0.8 Pierwszy test i pierwszy commit kodu

Pytest kończy się błędem, gdy nie znajdzie żadnego testu, a to zaświeciłoby CI na czerwono. Dodajcie na razie prosty test w `tests/test_smoke.py`:

```python
def test_pytest_dziala() -> None:
    assert 1 + 1 == 2
```

Uruchomcie `uv run pytest`. Ma być zielono. Ten plik usuniecie w kroku 1.2, gdy pojawią się prawdziwe testy.

**Commity** (osobno): `Dodaj punkt wejścia aplikacji Flet`, `Dodaj pierwszy test pytest`.

### 0.9 Zasady pracy (przeczytajcie razem)

Najważniejsze reguły (szczegóły w sekcji [Git i praca w zespole](#git-i-praca-w-zespole)):

- Każda funkcja w osobnej gałęzi (`feat/...`), scalana przez Pull Request.
- Małe commity, opisy mówią *co* i *dlaczego*.
- **Każde użycie LLM** ma stopkę w commicie i wpis w rejestrze w `README.md`.
- Każdy z Was ma umieć wyjaśnić **cały** kod, także część napisaną przez drugą osobę.

**Gotowe, gdy:** oboje uruchamiacie `uv run flet run src/main.py` i `uv run pytest`, repozytorium ma pierwsze commity od obu osób, a temat jest zgłoszony na UPeL.

## Etap 1: wersja v0.1.0

**Cel:** działa rdzeń (jednostki, produkty, lodówka), proste okno z listą lodówki, testy w CI i **paczka `.exe` zbudowana przez pipeline**.

> 💡 **Dlaczego paczka już w v0.1.0?** Pipeline wydania i `flet pack` to najczęstsze źródło niespodzianek. Lepiej odkryć problemy teraz, na prostym programie, niż tydzień przed końcem.

Proponowany podział pracy dla dwóch osób: **Osoba A** robi kroki 1.1–1.4 (domena), **Osoba B** robi 1.5–1.7 (okno, CI, paczka). Spotykacie się na 1.8–1.9. Przed prezentacją zamieńcie się: każdy opowiada kod, którego nie pisał.

### 1.1 Wyjątki: `domain/errors.py`

Utwórzcie hierarchię błędów domenowych:

```python
class DomainError(Exception):
    """Bazowy wyjątek aplikacji. Interfejs łapie tylko ten typ."""


class InvalidDataError(DomainError):
    """Niepoprawne dane (pusta nazwa, ujemna kaloryczność...)."""


class InvalidQuantityError(DomainError):
    """Ilość lub liczba porcji spoza dopuszczalnego zakresu."""


class IncompatibleUnitError(DomainError):
    """Jednostek nie da się przeliczyć (np. gramy na mililitry)."""


class InsufficientStockError(DomainError):
    """W lodówce jest mniej produktu, niż potrzeba."""


class NotFoundError(DomainError):
    """Nie ma takiego produktu lub przepisu."""


class StorageError(DomainError):
    """Problem z zapisem lub odczytem danych."""
```

Jeśli na razie wystarczą Wam cztery pierwsze, dodajcie `NotFoundError` i `StorageError` w etapie 2, gdy będą potrzebne.

> 💡 **Po co własne wyjątki?** `ValueError` mówi „coś jest nie tak”, a `InsufficientStockError` mówi **co** jest nie tak. Wspólny przodek `DomainError` pozwala interfejsowi napisać jeden `except DomainError` zamiast łapać wszystko (`except Exception` ukryłoby też prawdziwe błędy programistyczne). To jednocześnie spełnia „obsługę błędów” i „dziedziczenie”.

**Test** (`tests/test_errors.py`): każdy wyjątek jest podklasą `DomainError`, a `raise InsufficientStockError("...")` da się złapać przez `except DomainError`.

**Commit:** `Dodaj hierarchię wyjątków domenowych`

### 1.2 Jednostki i ilości: `domain/quantity.py`

Usuńcie `tests/test_smoke.py`. Potrzebujemy trzech elementów:

- `Kind`: rodzaj wielkości (`MASS`, `VOLUME`, `COUNT`),
- `Unit`: jednostki `G`, `KG`, `ML`, `L`, `PCS` (sztuki). Każda ma swój `kind` i `factor` (ile jednostek bazowych: g, ml lub szt. mieści się w jednej): `KG` → 1000, `L` → 1000,
- `Quantity`: niemutowalna liczba + jednostka, **z walidacją**.

Szkielet:

```python
import math
from dataclasses import dataclass
from enum import Enum

from fridge_manager.domain.errors import InvalidQuantityError


class Kind(Enum):
    MASS = "masa"
    VOLUME = "objętość"
    COUNT = "sztuki"


class Unit(Enum):
    G = "g"
    KG = "kg"
    ML = "ml"
    L = "l"
    PCS = "szt"

    @property
    def kind(self) -> Kind:
        return _KINDS[self]

    @property
    def factor(self) -> float:
        """Ile jednostek bazowych (g, ml, szt) mieści się w tej jednostce."""
        return _FACTORS[self]


_KINDS = {
    Unit.G: Kind.MASS,
    Unit.KG: Kind.MASS,
    Unit.ML: Kind.VOLUME,
    Unit.L: Kind.VOLUME,
    Unit.PCS: Kind.COUNT,
}
_FACTORS = {Unit.G: 1, Unit.KG: 1000, Unit.ML: 1, Unit.L: 1000, Unit.PCS: 1}


@dataclass(frozen=True)
class Quantity:
    amount: float
    unit: Unit

    def __post_init__(self) -> None:
        # TODO: rzuć InvalidQuantityError, gdy amount nie jest skończoną liczbą > 0
        ...
```

Uzupełnijcie `__post_init__` (podpowiedź: `math.isfinite`).

> 💡 **Po co `frozen=True`?** Obiekt `Quantity` nie może zmienić się po utworzeniu (próba `q.amount = 5` rzuca błąd). Wtedy nikt przypadkiem nie zepsuje ilości, którą trzyma przepis albo lodówka. Walidacja w `__post_init__` gwarantuje, że **nigdy** nie istnieje `Quantity` z ilością ujemną lub NaN, więc dalszy kod nie musi tego sprawdzać.
>
> 💡 **Po co `Kind` i `factor`?** Dzięki nim przeliczanie 1 l → 1000 ml i wykrywanie, że „gramy ≠ mililitry”, jest w jednym miejscu, a nie w `if`-ach rozsianych po programie.

**Testy** (`tests/test_quantity.py`), użyjcie `pytest.mark.parametrize`:

- poprawna ilość tworzy obiekt,
- `0`, liczby ujemne, `nan`, `inf` → `InvalidQuantityError`,
- niemutowalność (przypisanie do `amount` rzuca `dataclasses.FrozenInstanceError`),
- równość: `Quantity(1, Unit.KG) == Quantity(1, Unit.KG)`,
- `Unit.KG.factor == 1000`, `Unit.L.kind is Kind.VOLUME` itd. (parametryzowane).

**Commity:** `Dodaj Unit i Quantity z walidacją ilości`, `Dodaj testy Quantity i Unit`

### 1.3 Produkty: `domain/food.py`

Tu jest serce OOP. Plan:

- **`FoodItem`**: klasa abstrakcyjna (`abc.ABC`). Przechowuje nazwę i kaloryczność na 100 g.
- Trzy klasy pochodne:
  - `WeightItem`: produkt na wagę (mąka). Bazą jest gram.
  - `VolumeItem`: produkt na objętość (mleko). Bazą jest mililitr, dodatkowo `grams_per_ml` (gęstość, domyślnie 1.0).
  - `PieceItem`: produkt na sztuki (jajko). Bazą jest sztuka, dodatkowo `grams_per_piece`.
- Każda klasa pochodna **sama** definiuje dwie rzeczy: `base_unit` (w czym liczymy zapas) i `to_grams(base_amount)` (ile to gramów, potrzebne do kalorii).
- Reszta jest w klasie bazowej: `to_base(q)` (przelicza dowolną zgodną ilość na bazową) i `calories(q)`.

Szkielet:

```python
from abc import ABC, abstractmethod

from fridge_manager.domain.errors import IncompatibleUnitError, InvalidDataError
from fridge_manager.domain.quantity import Quantity, Unit


class FoodItem(ABC):
    def __init__(self, name: str, calories_per_100g: float) -> None:
        # TODO: przytnij nazwę (strip); pusta nazwa lub ujemna kaloryczność → InvalidDataError
        self._name = name
        self._calories_per_100g = calories_per_100g

    @property
    def name(self) -> str:
        return self._name

    @property
    def key(self) -> str:
        """Identyfikator produktu: nazwa bez rozróżniania wielkości liter."""
        return self._name.casefold()

    @property
    def calories_per_100g(self) -> float:
        return self._calories_per_100g

    @property
    @abstractmethod
    def base_unit(self) -> Unit:
        """Jednostka, w której trzymamy zapas tego produktu (G, ML lub PCS)."""

    @abstractmethod
    def to_grams(self, base_amount: float) -> float:
        """Ile gramów to base_amount jednostek bazowych."""

    def to_base(self, q: Quantity) -> float:
        """Przelicza ilość na jednostkę bazową produktu."""
        if q.unit.kind is not self.base_unit.kind:
            raise IncompatibleUnitError(
                f"Nie można przeliczyć {q.unit.value} na {self.base_unit.value} "
                f"dla produktu „{self.name}”"
            )
        return q.amount * q.unit.factor / self.base_unit.factor

    def calories(self, q: Quantity) -> float:
        return self.to_grams(self.to_base(q)) * self._calories_per_100g / 100


class WeightItem(FoodItem):
    @property
    def base_unit(self) -> Unit:
        return Unit.G

    def to_grams(self, base_amount: float) -> float:
        return base_amount


# TODO: VolumeItem (grams_per_ml) i PieceItem (grams_per_piece) zrobicie sami
```

Zadanie: dopiszcie `VolumeItem` i `PieceItem`. W konstruktorze wywołajcie `super().__init__(...)` i zwalidujcie dodatkowy parametr (musi być > 0, inaczej `InvalidDataError`).

> 💡 **Po co klasa abstrakcyjna?** `FoodItem()` nie ma sensu (nie wiadomo, w czym liczyć), więc `ABC` zabrania go tworzyć. Mówi też każdej klasie pochodnej: „musisz zdefiniować `base_unit` i `to_grams`”. To **abstrakcja**.
>
> 💡 **Po co dziedziczenie i polimorfizm?** Gdy `Fridge` dostaje `FoodItem`, nie sprawdza, czy to mleko czy jajko. Woła `food.to_base(q)` i każda klasa robi swoje. Dodanie czwartego rodzaju produktu (np. na zwitki, pęczki) to nowa klasa, bez zmian w lodówce i przepisach. To **polimorfizm**.
>
> 💡 **Po co metoda szablonowa (`calories`)?** Algorytm („przelicz na bazę → na gramy → pomnóż przez kcal”) jest jeden i leży w klasie bazowej. Klasy pochodne podmieniają tylko kroki, które się różnią. To wzorzec *Template Method* i dobry temat na pytanie na prezentacji.
>
> 💡 **Po co `key`?** „Mleko” i „mleko” to ten sam produkt. Lodówka identyfikuje produkty po `key`, więc nie zrobi dwóch osobnych pozycji.

Uproszczenie: kaloryczność podajemy zawsze na 100 g. Dla płynów przyjmujemy etykietę „na 100 ml” za równoważną (gęstość ≈ 1), a `grams_per_ml` pozwala to doprecyzować (mleko ≈ 1,03).

**Testy** (`tests/test_food.py`):

- nie można utworzyć `FoodItem` bezpośrednio (`pytest.raises(TypeError)`),
- pusta nazwa, spacje, ujemna kaloryczność → `InvalidDataError`,
- `to_base`: `1 kg` na `WeightItem` → 1000; `1 l` na `VolumeItem` → 1000; `2 szt` na `PieceItem` → 2,
- niezgodne jednostki: `ml` na `WeightItem`, `g` na `PieceItem` → `IncompatibleUnitError`,
- `calories`: 100 g mąki po 350 kcal/100 g → 350; 2 jajka po 55 g i 140 kcal/100 g → 154 (użyjcie `pytest.approx`),
- `key`: „Mleko” i „mleko ” mają ten sam klucz,
- `isinstance(WeightItem(...), FoodItem)` jest prawdziwe (polimorfizm).

**Commity:** `Dodaj klasę abstrakcyjną FoodItem i WeightItem`, `Dodaj VolumeItem i PieceItem`, `Dodaj testy hierarchii FoodItem`

### 1.4 Lodówka: `domain/fridge.py`

Dwie klasy:

- **`StockItem`**: pozycja w lodówce = produkt + ilość **w jednostce bazowej** produktu. Prywatne pole `_amount`, metody `add(amount)` i `remove(amount)`.
- **`Fridge`**: prywatny słownik `_items: dict[str, StockItem]` (klucz = `food.key`).

Interfejs `Fridge`:

| Metoda | Zadanie |
| :--- | :--- |
| `add(food, q)` | dodaje ilość (przeliczoną przez `food.to_base(q)`); tworzy pozycję lub zwiększa istniejącą |
| `consume(food, q)` | odejmuje ilość; za mało lub brak produktu → `InsufficientStockError`; po zejściu do zera pozycja **znika** |
| `available(food) -> float` | ile jest w jednostce bazowej (0, gdy brak) |
| `items() -> list[StockItem]` | **kopia** listy pozycji do wyświetlenia |

Kluczowy fragment `consume`:

```python
EPS = 1e-9  # tolerancja na błędy zmiennoprzecinkowe


def consume(self, food: FoodItem, q: Quantity) -> None:
    needed = food.to_base(q)          # tu może polecieć IncompatibleUnitError
    have = self.available(food)
    if needed > have + EPS:
        raise InsufficientStockError(
            f"Za mało produktu „{food.name}”: potrzeba {needed:g}, jest {have:g}"
        )
    # TODO: zmniejsz ilość w StockItem; jeśli zostało <= EPS, usuń pozycję z _items
```

> 💡 **Po co hermetyzacja tutaj?** Gdyby `_items` było publiczne, ktoś mógłby napisać `fridge.items["mleko"].amount = -5` i lodówka miałaby ujemny zapas. Skoro zmiana jest możliwa **tylko** przez `add()` i `consume()`, te dwie metody są jedynym miejscem do pilnowania poprawności. W Pythonie prywatność to konwencja (`_nazwa`), dlatego na zewnątrz wystawiamy właściwości tylko do odczytu i **kopie** kolekcji.
>
> 💡 **Po co `EPS`?** W komputerze `0.1 + 0.2 != 0.3`. Po kilku zakupach i gotowaniach w zapasie mogłoby zostać `1e-17` zamiast zera, a porównanie „czy starczy” by się myliło. Tolerancja porządkuje takie przypadki. (Alternatywa: liczyć w liczbach całkowitych, np. mililitrach.)
>
> 💡 **Po co usuwać pozycję przy zerze?** Lodówka nie powinna wyświetlać „mąka: 0 g”. Wtedy też `available()` ma jedną regułę: nie ma wpisu, to jest 0.

**Testy** (`tests/test_fridge.py`) i przypadki brzegowe:

- `add` nowego produktu i dodanie kolejnej porcji (ilości się sumują),
- `add` w innej jednostce: 1 kg po 500 g mąki daje 1500 g,
- `consume` części ilości (1000 ml mleka − 200 ml = 800 ml; **to nasz przykład z mlekiem**),
- `consume` **dokładnie** całej ilości: pozycja znika, `available == 0`,
- `consume` więcej niż jest → `InsufficientStockError`, **a stan się nie zmienił**,
- `consume` produktu, którego nie ma → `InsufficientStockError`,
- niezgodne jednostki (ml dla mąki) → `IncompatibleUnitError`,
- błąd zmiennoprzecinkowy: dodaj 0,1 i 0,2, zużyj 0,3 → pozycja znika (`pytest.approx` lub `EPS`),
- `items()` zwraca kopię: dopisanie do zwróconej listy nie zmienia lodówki (test hermetyzacji),
- ten sam produkt pod nazwą „Mleko” i „mleko” to jedna pozycja.

**Commity:** `Dodaj StockItem i Fridge z dodawaniem i zużyciem`, `Dodaj testy przypadków brzegowych lodówki`

### 1.5 Pierwszy widok w Flet: lodówka

W v0.1.0 okno ma **tylko** lodówkę: listę produktów i formularz „dodaj”. Dane żyją w pamięci (bez zapisu), a w etapie 2 podmienimy je na serwis i JSON.

Plan widoku (`ui/fridge_view.py`):

```python
import flet as ft

from fridge_manager.domain.errors import DomainError
from fridge_manager.domain.fridge import Fridge


class FridgeView:
    """Lista produktów w lodówce + formularz dodawania."""

    def __init__(self, page: ft.Page, fridge: Fridge, foods: dict) -> None:
        self._page = page
        self._fridge = fridge
        self._foods = foods                       # produkty znane aplikacji: key -> FoodItem
        self._list = ft.ListView(expand=True)
        self._error = ft.Text("", color=ft.Colors.RED)
        # TODO: pola formularza (TextField na ilość, Dropdown na produkt i jednostkę, Button)
        self.root = ft.Column(controls=[self._list, self._error])  # + formularz

    def refresh(self) -> None:
        self._list.controls = [
            ft.Text(f"{item.food.name}: {item.amount:g} {item.food.base_unit.value}")
            for item in self._fridge.items()
        ]
        self._page.update()

    def _on_add_click(self, e: ft.ControlEvent) -> None:
        try:
            ...  # odczytaj formularz, zbuduj Quantity, wywołaj self._fridge.add(...)
            self._error.value = ""
        except DomainError as err:
            self._error.value = str(err)
        self.refresh()
```

I `ui/app.py`, który składa całość:

```python
import flet as ft

from fridge_manager.domain.fridge import Fridge
from fridge_manager.ui.fridge_view import FridgeView


def main(page: ft.Page) -> None:
    page.title = "FridgeManager"
    fridge = Fridge()
    foods = {}  # TODO: kilka produktów startowych (mleko, mąka, jajko), żeby było co dodawać
    view = FridgeView(page, fridge, foods)
    page.add(view.root)
    view.refresh()
```

W `src/main.py` zastąpcie napis wywołaniem `from fridge_manager.ui.app import main`. Zostawcie `ft.run(main)`.

Dopiszcie też `ui/formatting.py` z funkcją przekształcającą `1000 ml` w `1 l`, a `1500 g` w `1,5 kg`. To czysta funkcja i możecie ją przetestować w `tests/test_formatting.py`.

> 💡 **Po co klasa widoku z `refresh()`?** Flet nie odświeża listy sam po zmianie danych. Wzorzec jest zawsze ten sam: zmień dane → przebuduj kontrolki → `page.update()`. Trzymanie tego w klasie (zamiast funkcji zagnieżdżonych w `main`) pozwala dodać kolejne widoki bez bałaganu.
>
> 💡 **Po co `except DomainError` w interfejsie?** To jedyne miejsce, gdzie „zamieniamy” wyjątki na komunikaty dla człowieka. Domena rzuca błąd, interfejs go pokazuje. Inne wyjątki (prawdziwe błędy w kodzie) **celowo** nie są łapane, żeby nie ukryć bugów.
>
> ⚠️ Pierwszy komunikat błędu pokazujemy zwykłym `ft.Text`. Ładniejszy `SnackBar` dodacie później: w Flet 1.x pokazuje się go przez `page.show_dialog(...)`, ale sprawdźcie w dokumentacji, czy to nadal aktualne.

Ręczny test przed commitem: dodaj mleko, dodaj jeszcze raz, spróbuj dodać „-5” i „abc”. Aplikacja ma pokazać błąd, a nie wywalić się.

**Commity:** `Dodaj widok lodówki we Flet`, `Dodaj formatowanie ilości w interfejsie`

### 1.6 Pipeline testowy: `.github/workflows/test.yml`

```yaml
name: Testy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v7
      - name: Zainstaluj zależności
        run: uv sync --locked
      - name: Uruchom testy
        run: uv run pytest
```

Po wypchnięciu zajrzyjcie w zakładkę **Actions** w repozytorium. Powinien pojawić się zielony przebieg.

> 💡 **Po co `--locked`?** Pipeline ma użyć dokładnie tych wersji, które są w `uv.lock`. Jeśli ktoś zmienił `pyproject.toml` i zapomniał o `uv.lock`, CI zgłosi błąd. To dobrze, bo wychodzi od razu.
>
> 💡 **Po co `pull_request`?** Wymaganie dotyczy tylko `main`, ale uruchamianie testów na pull requestach pozwala wykryć błąd **przed** scaleniem, więc `main` nie robi się czerwony. Wersje akcji (`checkout@v5`, `setup-uv@v7`) mogą być starsze niż najnowsze. Działają, a aktualne numery sprawdzicie na stronach tych akcji.

**Commit:** `Dodaj pipeline testowy GitHub Actions`

### 1.7 Paczka `.exe` i pipeline wydania

#### Najpierw lokalnie (Windows)

```bash
uv run flet pack src/main.py --name FridgeManager --yes
```

Sprawdźcie folder `dist/`. Powinien powstać `FridgeManager.exe` (albo folder z nim). Uruchomcie go i upewnijcie się, że okno działa.

> 💡 **Po co lokalnie?** Zanim oddamy to CI, chcemy wiedzieć, jak wygląda wynik i czy program w ogóle startuje spakowany. `flet pack` używa PyInstallera, który zamyka Pythona i biblioteki w jednym pliku. Użytkownik nie musi nic instalować. PyInstaller **nie buduje między systemami**: `.exe` powstaje tylko na Windows, dlatego w CI użyjemy runnera `windows-latest`.

Jeśli ścieżka wyniku jest inna niż `dist/FridgeManager.exe`, dopasujcie ją w pliku poniżej.

#### Pipeline: `.github/workflows/release.yml`

```yaml
name: Wydanie

on:
  push:
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"

permissions:
  contents: write

jobs:
  release:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v5
      - uses: astral-sh/setup-uv@v7

      - name: Zainstaluj zależności
        run: uv sync --locked

      - name: Sprawdź zgodność tagu z wersją w pyproject.toml
        shell: bash
        run: |
          VERSION=$(uv run python -c "import tomllib; print(tomllib.load(open('pyproject.toml','rb'))['project']['version'])")
          if [ "v$VERSION" != "$GITHUB_REF_NAME" ]; then
            echo "Tag $GITHUB_REF_NAME nie zgadza się z wersją $VERSION w pyproject.toml"
            exit 1
          fi

      - name: Uruchom testy
        run: uv run pytest

      - name: Zbuduj program
        run: uv run flet pack src/main.py --name FridgeManager --yes

      - name: Spakuj paczkę
        run: |
          New-Item -ItemType Directory release | Out-Null
          Copy-Item dist\FridgeManager.exe release\
          Copy-Item README.md release\
          Compress-Archive -Path release\* -DestinationPath "FridgeManager-$env:GITHUB_REF_NAME-windows.zip"

      - name: Opublikuj wydanie
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh release create "$GITHUB_REF_NAME" "FridgeManager-$GITHUB_REF_NAME-windows.zip" \
            --title "$GITHUB_REF_NAME" --generate-notes
```

> 💡 **Po co filtr `v[0-9]+.[0-9]+.[0-9]+`?** Prowadzący wymaga, żeby pipeline wydania odpalał się **wyłącznie** dla tagów w formacie `vX.Y.Z`.
>
> 💡 **Po co sprawdzanie wersji?** Łatwo zapomnieć podnieść numer w `pyproject.toml`. Wtedy paczka `v0.2.0` zawierałaby program podpisany jako 0.1.0. Pipeline po prostu zatrzyma się z czytelnym błędem.
>
> 💡 **Po co `permissions: contents: write`?** Domyślnie token CI może tylko czytać repozytorium, a tworzenie wydania to zapis.
>
> 💡 **Po co `windows-latest`?** Patrz wyżej: `.exe` buduje się na Windows.

**Commit:** `Dodaj pipeline wydania z paczką dla Windows`

> Plan B, gdyby `flet pack` sprawiał problemy w CI: paczka `.zip` ze źródłami (`src/`, `pyproject.toml`, `uv.lock`, `.python-version`, `README.md`) i instrukcją „`uv sync` i `uv run python src/main.py`”. Prowadzący dopuszcza archiwum, ale `.exe` robi lepsze wrażenie na prezentacji, więc najpierw próbujcie z `.exe`. Kolejna opcja to `flet build windows` (wymaga Visual Studio z komponentem „Desktop development with C++”, który jest na runnerze `windows-latest`, ale build jest wolniejszy i bardziej wymagający).

### 1.8 README i rejestr LLM (szkielet)

`README.md` jest już gotowy jako szablon w repozytorium. Na tym etapie:

- wklejcie link do repozytorium i dopiszcie autorów,
- usuńcie z niego fragmenty, których jeszcze nie ma w kodzie, albo zostawcie je z 🚧,
- wpiszcie **prawdziwe** wpisy do rejestru LLM za wszystko, co do tej pory powstało przy pomocy modelu (zastępując przykładowe).

> 💡 **Po co prowadzić rejestr od razu?** Odtwarzanie po miesiącu, co wygenerował model, a co napisaliście sami, jest nudne i grozi „nieoznaczonym użyciem LLM”, które prowadzący traktuje jak niesamodzielną pracę. Dopisywanie jednej linijki przy każdym commicie to minimum wysiłku.

**Commit:** `Uzupełnij README o instrukcję uruchomienia i rejestr LLM`

### 1.9 Wydanie v0.1.0

Lista kontrolna:

- [ ] `uv run pytest` jest zielone lokalnie, a ostatni przebieg **Testy** na `main` w Actions też.
- [ ] `version = "0.1.0"` w `pyproject.toml` (zacommitowane i wypchnięte).
- [ ] Wszystkie gałęzie scalone, `git status` czysty.
- [ ] `git ls-files` nie zawiera `.venv`, `dist`, `build`, `data.json`, `.vscode`.
- [ ] Tag:
  ```bash
  git tag v0.1.0
  git push origin v0.1.0
  ```
- [ ] W Actions przebieg **Wydanie** jest zielony, w **Releases** pojawiło się `FridgeManager-v0.1.0-windows.zip`.
- [ ] **Pobierzcie** paczkę z GitHub Releases (nie z lokalnego `dist/`), rozpakujcie w innym folderze i uruchomcie.
- [ ] Wgrajcie paczkę na UPeL do zadania „1. wersja pośrednia”.

> 💡 **Dlaczego pobieramy paczkę z Releases?** Prowadzący oceni dokładnie to, co jest w wydaniu. Dlatego sprawdzamy, że to działa, a nie tylko wersja z naszego komputera.

Jeśli pipeline wydania się wywali, **nie edytujcie** tagu ręcznie. Usuńcie tag lokalnie i zdalnie, popraw problem na `main` i oznaczcie ponownie:

```bash
git tag -d v0.1.0
git push origin :refs/tags/v0.1.0
```

(Jeśli powstało częściowe wydanie w GitHub, usuńcie je w zakładce Releases.)

**Gotowe, gdy:** paczka v0.1.0 jest na UPeL, a Wy umiecie wytłumaczyć każdą klasę z etapu 1.

## Etap 2: wersja v0.2.0

**Cel:** przepisy, lista zakupów, zakup (dodaje do lodówki), gotowanie (odejmuje), zapis do JSON, widoki we Flet. Po tym etapie działa **scenariusz referencyjny** z sekcji [Co budujemy](#co-budujemy).

Podział dla dwóch osób: **A** robi 2.1–2.2 i 2.6 (przepisy, lista, serwis), **B** robi 2.3–2.5 (dane, repozytoria, JSON). UI (2.7) robicie razem.

### 2.1 Przepisy: `domain/recipe.py`

Dwie klasy:

- **`RecipeIngredient`** (`@dataclass(frozen=True)`): `food: FoodItem` i `per_portion: Quantity`.
- **`Recipe`**: nazwa i lista składników **na 1 porcję**.

Interfejs `Recipe`:

| Metoda | Zadanie |
| :--- | :--- |
| `Recipe(name, ingredients)` | pusta nazwa, brak składników lub ten sam produkt dwa razy → `InvalidDataError` |
| `scale(portions)` | lista `RecipeIngredient` przeliczona na N porcji (do wyświetlenia); `portions <= 0` → `InvalidQuantityError` |
| `required_amounts(portions)` | lista par `(FoodItem, ilość w jednostce bazowej)` na N porcji; używają jej lista zakupów i gotowanie |

Przykład z mlekiem: przepis „Naleśniki”, składnik mleko 100 ml na porcję. `required_amounts(2)` zwraca mleko w ilości 200 (ml).

> 💡 **Po co kompozycja?** Przepis *ma* składniki, a nie *jest* produktem. Gdybyśmy zrobili `Recipe(FoodItem)`, dziedziczenie przestałoby mieć sens (przepis nie ma gęstości ani kcal na 100 g). To klasyczne rozróżnienie „jest” (dziedziczenie) i „ma” (kompozycja).
>
> 💡 **Po co zakaz duplikatów?** Dwa wpisy „mleko” w jednym przepisie wymagałyby łączenia ilości i komplikowały listę zakupów. Walidacja w konstruktorze mówi użytkownikowi to od razu.
>
> 💡 **Po co `required_amounts` w jednostce bazowej?** Lodówka trzyma zapas w jednostce bazowej produktu, więc porównanie „potrzeba vs jest” to odejmowanie dwóch liczb. Przeliczanie jednostek robi się raz, w `FoodItem.to_base`.

**Testy** (`tests/test_recipe.py`): poprawny przepis; pusty; duplikaty; `scale(2)` mnoży ilości; `scale(0)`, `scale(-1)` → błąd; **ułamek porcji** (`scale(0.5)`); `required_amounts` zamienia litry na mililitry; składniki z różnych klas produktów (`WeightItem`, `VolumeItem`, `PieceItem`) w jednym przepisie.

**Commity:** `Dodaj Recipe i RecipeIngredient`, `Dodaj testy przepisu`

### 2.2 Lista zakupów: `domain/shopping.py`

- **`ShoppingItem`** (`frozen dataclass`): `food` i `missing: Quantity` (w jednostce bazowej produktu).
- **`ShoppingList`**: trzyma listę `ShoppingItem`. Metody: `items` (kopia), `is_empty()`, oraz `__iter__` i `__len__` (żeby można było pisać `for item in lista`).

> 💡 **Po co osobna klasa listy zakupów?** `ShoppingList` mówi, czego brakuje, a serwis (2.6) używa jej na dwa sposoby: do pokazania użytkownikowi i do sprawdzenia, czy można gotować (`is_empty()`). To czytelniejsze niż przekazywanie luźnych słowników.

**Testy** (`tests/test_shopping.py`): pusta lista, lista z jedną pozycją, `items` zwraca kopię, iteracja.

**Commit:** `Dodaj ShoppingItem i ShoppingList`

### 2.3 Zbiór danych: `domain/app_data.py`

`AppData` to prosty kontener wszystkiego, co aplikacja zapamiętuje:

```python
from dataclasses import dataclass, field

from fridge_manager.domain.food import FoodItem
from fridge_manager.domain.fridge import Fridge
from fridge_manager.domain.recipe import Recipe


@dataclass
class AppData:
    foods: dict[str, FoodItem] = field(default_factory=dict)    # key -> FoodItem
    recipes: dict[str, Recipe] = field(default_factory=dict)    # nazwa (casefold) -> Recipe
    fridge: Fridge = field(default_factory=Fridge)
    # v1.0.0: journal: CalorieJournal
```

> 💡 **Po co `default_factory`?** Domyślnych wartości zmiennych (słownik, lodówka) nie wolno dawać wprost (`foods = {}`), bo wszystkie obiekty `AppData` dzieliłyby ten sam słownik. `default_factory` tworzy nowy przy każdym obiekcie. To częsta pułapka w Pythonie.

### 2.4 Repozytorium: `domain/repository.py` i `storage/memory_repository.py`

```python
from abc import ABC, abstractmethod

from fridge_manager.domain.app_data import AppData


class StorageRepository(ABC):
    @abstractmethod
    def load(self) -> AppData:
        """Wczytuje dane. Gdy nic jeszcze nie zapisano, zwraca pusty AppData."""

    @abstractmethod
    def save(self, data: AppData) -> None:
        """Zapisuje dane."""
```

`InMemoryRepository` trzyma dane w polu i oddaje je z `load()`. Służy do testów i do uruchamiania programu bez dysku.

> 💡 **Po co abstrakcja zapisu?** `CookingService` woła `repo.save(data)` i nie wie, czy to plik, baza czy pamięć. W testach wstrzykujemy `InMemoryRepository`, więc testy nie dotykają dysku. Za tydzień można dopisać `SqliteRepository` bez zmiany serwisu. To praktyczny przykład **abstrakcji + polimorfizmu** i *wstrzykiwania zależności*.

**Testy:** `tests/test_repositories.py`. Najlepiej napisać **jeden zestaw testów** dla obu repozytoriów (w 2.5 dołożycie `JsonRepository`) z `@pytest.fixture(params=[...])`: wczytanie pustego, zapis i odczyt dają ten sam stan.

**Commity:** `Dodaj AppData`, `Dodaj abstrakcję StorageRepository i InMemoryRepository`

### 2.5 Zapis JSON: `storage/json_repository.py`

Pliki:

- `storage/paths.py`: funkcja `default_data_path()` zwraca ścieżkę pliku danych:
  - jeśli ustawiona jest zmienna `FRIDGE_MANAGER_DATA`, użyj jej,
  - Windows: `%APPDATA%\FridgeManager\data.json`,
  - macOS / Linux: `~/.fridge_manager/data.json`.
- `storage/serialization.py`: funkcje zamieniające `AppData` na słownik (i z powrotem).
- `storage/json_repository.py`: `JsonRepository(path)` implementuje `load()` i `save()`.

Przykład pliku (`schema_version` pozwoli kiedyś zmienić format):

```json
{
  "schema_version": 1,
  "foods": [
    {"type": "volume", "name": "Mleko", "calories_per_100g": 64, "grams_per_ml": 1.03},
    {"type": "weight", "name": "Mąka", "calories_per_100g": 350},
    {"type": "piece", "name": "Jajko", "calories_per_100g": 140, "grams_per_piece": 55}
  ],
  "recipes": [
    {"name": "Naleśniki", "ingredients": [
      {"food": "mleko", "amount": 100, "unit": "ml"},
      {"food": "mąka", "amount": 60, "unit": "g"},
      {"food": "jajko", "amount": 1, "unit": "szt"}
    ]}
  ],
  "fridge": [
    {"food": "mleko", "amount": 800}
  ]
}
```

Wskazówki do implementacji:

- Rodzaj produktu zapisujemy jako tekst (`"weight"`, `"volume"`, `"piece"`) i trzymamy w kodzie słownik `FOOD_TYPES = {"weight": WeightItem, ...}`. Przy wczytywaniu to on wybiera klasę.
- Przepisy i lodówka odwołują się do produktów po `key`. Wczytując, zbierzcie najpierw produkty, a dopiero potem budujcie przepisy i lodówkę z **tych samych obiektów**.
- Lodówkę odtwarzajcie przez publiczne `fridge.add(food, Quantity(amount, food.base_unit))`.
- Zapis: najpierw do pliku tymczasowego obok (`data.json.tmp`), potem `os.replace(tmp, path)`. Utwórzcie brakujący folder (`path.parent.mkdir(parents=True, exist_ok=True)`).
- Plik nie istnieje → `load()` zwraca pusty `AppData`. Plik uszkodzony, nieznany typ produktu, brakujące pole → `StorageError` z czytelnym komunikatem.
- Kodowanie: `encoding="utf-8"`, `ensure_ascii=False` (polskie znaki).

> 💡 **Po co zapis przez plik tymczasowy?** Gdy program padnie w trakcie zapisu, zostałby ucięty, uszkodzony `data.json`. `os.replace` jest atomowe: plik jest albo stary, albo nowy, nigdy pół na pół.
>
> 💡 **Po co `StorageError` zamiast surowego `json.JSONDecodeError`?** Interfejs łapie tylko `DomainError`. Zamiana błędów technicznych (zły JSON, brak pola) na nasz wyjątek to spójna obsługa błędów w całym projekcie.
>
> 💡 **Po co dane poza folderem programu?** `.exe` może leżeć w folderze tylko do odczytu albo być uruchamiany z różnych miejsc. Katalog użytkownika jest stały i nie trafia do repozytorium.

**Testy** (z wbudowaną fixture `tmp_path`, która daje tymczasowy folder):

- zapis i odczyt zwracają ten sam stan (produkty, przepisy, lodówka),
- brak pliku → pusty `AppData`,
- uszkodzony JSON, nieznany typ produktu, przepis z nieistniejącym produktem → `StorageError`,
- zapis tworzy brakujący folder,
- polskie znaki (Mąka, Naleśniki) przeżywają zapis i odczyt,
- `default_data_path()` uwzględnia `FRIDGE_MANAGER_DATA` (użyjcie fixture `monkeypatch`).

**Commity:** `Dodaj serializację AppData do słowników`, `Dodaj JsonRepository z atomowym zapisem`, `Dodaj testy JsonRepository`

### 2.6 Serwis: `domain/service.py`

`CookingService(data: AppData, repository: StorageRepository)` łączy wszystko. Metody:

| Metoda | Co robi |
| :--- | :--- |
| `add_food(food)` | dodaje produkt do znanych produktów (duplikat po `key` → `InvalidDataError`), zapisuje |
| `add_recipe(recipe)` | dodaje przepis; produkty przepisu muszą być znane aplikacji (inaczej `NotFoundError`), zapisuje |
| `buy(food, q)` | **dodaje** do lodówki, zapisuje |
| `build_shopping_list(recipe_name, portions)` | zwraca `ShoppingList` z brakami (nic nie zmienia) |
| `buy_missing(shopping)` | zatwierdza zakupy z listy: dodaje wszystkie pozycje do lodówki, zapisuje |
| `cook(recipe_name, portions)` | **odejmuje** składniki od razu **albo wcale**, zapisuje |
| `list_foods()`, `list_recipes()`, `fridge_items()`, `get_recipe(name)` | odczyt dla interfejsu (kopie, nieznany przepis → `NotFoundError`) |

Algorytm listy zakupów:

```python
def build_shopping_list(self, recipe_name: str, portions: float) -> ShoppingList:
    recipe = self.get_recipe(recipe_name)
    missing = []
    for food, needed in recipe.required_amounts(portions):
        lack = needed - self._data.fridge.available(food)
        if lack > EPS:
            missing.append(ShoppingItem(food, Quantity(lack, food.base_unit)))
    return ShoppingList(missing)
```

Algorytm gotowania (**wszystko albo nic**):

```python
def cook(self, recipe_name: str, portions: float) -> None:
    shopping = self.build_shopping_list(recipe_name, portions)
    if not shopping.is_empty():
        raise InsufficientStockError(...)  # wymień czego brakuje
    recipe = self.get_recipe(recipe_name)
    for food, needed in recipe.required_amounts(portions):
        self._data.fridge.consume(food, Quantity(needed, food.base_unit))
    self._repository.save(self._data)
```

> 💡 **Po co najpierw sprawdzić, potem odejmować?** Przy przepisie z trzech składników mogłoby się zdarzyć, że mleko odejmiemy, mąkę odejmiemy, a przy jajkach wyjdzie błąd. Lodówka zostałaby w połowie zmieniona. Sprawdzenie wszystkiego przed pierwszą zmianą daje **atomowość**: albo cały przepis, albo nic. Na obronie to ciekawa rzecz do pokazania.
>
> 💡 **Po co serwis, skoro `Fridge` już umie `add` i `consume`?** `Fridge` nie zna przepisów ani zapisu. Reguły „ugotuj przepis i zapisz” nie należą ani do lodówki, ani do przepisu, więc mają własną klasę. Interfejs wywołuje tylko serwis, więc nie rozstrzyga żadnych reguł biznesowych.
>
> 💡 **Po co `repository.save` po każdej zmianie?** Dane nie zginą, jeśli program zostanie zamknięty nagle. Przy tak małych danych koszt jest znikomy.

Uwaga do `Quantity(lack, ...)`: `Quantity` wymaga ilości > 0. Dlatego pozycji bez braków nie tworzymy (stąd warunek `lack > EPS`).

**Testy** (`tests/test_service.py`, z `InMemoryRepository`):

- **scenariusz referencyjny** (kroki 1–7 z sekcji [Co budujemy](#co-budujemy)) jako jeden test, pokazujący, że całość działa razem,
- lista zakupów, gdy wszystko jest: pusta,
- lista zakupów, gdy jest część: tylko braki (nie całość),
- lista zakupów dla ułamka porcji i dla dużej liczby porcji,
- `buy_missing` → po nim ponowne `build_shopping_list` jest puste,
- `cook`, gdy czegoś brakuje: `InsufficientStockError`, lodówka **bez zmian** (test atomowości),
- `cook` zużywa wszystko do zera: pozycje znikają,
- nieznany przepis → `NotFoundError`; przepis z nieznanym produktem → `NotFoundError`,
- każda zmiana woła `save` (użyjcie własnego, „szpiegującego” repozytorium, które liczy wywołania `save`; to dobry sposób, żeby zobaczyć w praktyce polimorfizm).

**Commity:** `Dodaj CookingService z zakupami i gotowaniem`, `Dodaj test scenariusza z mlekiem`, `Dodaj testy atomowości gotowania`

### 2.7 Widoki Flet: przepisy i zakupy

Zmiany w interfejsie:

1. W `ui/app.py`: wczytaj dane przez `JsonRepository(default_data_path())`, utwórz `CookingService`, przekaż go widokom. Dopilnuj, że błąd odczytu (`StorageError`) pokaże się użytkownikowi, a nie zamknie aplikacji.
2. `FridgeView` używa serwisu (`fridge_items()`, `buy(...)`) zamiast gołej lodówki.
3. Nowy `ui/recipes_view.py`:
   - lista przepisów i formularz „dodaj przepis” (nazwa + składniki: produkt, ilość, jednostka; składniki można dodawać po jednym),
   - wybór przepisu + pole liczby porcji + przycisk **Pokaż listę zakupów**,
   - lista braków i przycisk **Kupiłem** (wywołuje `buy_missing`),
   - przycisk **Ugotuj** (wywołuje `cook`).
4. Nawigacja między widokami: **najprostsza i niezawodna** wersja to rząd przycisków („Lodówka”, „Przepisy”) nad kontenerem, którego `content` podmieniacie na `view.root` wybranego widoku, a potem `page.update()`. Gdy będziecie chcieli ładniejszą (np. `NavigationBar`), sprawdzicie ją w dokumentacji.
5. Po każdej akcji: odśwież widoki, a `DomainError` pokaż jako komunikat.

> 💡 **Po co „cienki” interfejs?** Zauważcie, że w widokach nie ma ani jednej reguły typu „czy starczy mleka”. Widok zbiera dane z pól, wywołuje metodę serwisu, a wynik lub błąd wyświetla. Dzięki temu cała logika jest przetestowana testami jednostkowymi, a interfejs sprawdzamy ręcznie.

**Ręczny test (lista kontrolna):**

- [ ] Uruchomienie z pustym plikiem danych działa i pokazuje pustą lodówkę.
- [ ] Przejście przez cały scenariusz z mlekiem w oknie aplikacji.
- [ ] Zamknięcie i ponowne uruchomienie: stan lodówki i przepisy zostały.
- [ ] Błędne dane (litery w ilości, 0 porcji, ujemna ilość) → komunikat, bez awarii.
- [ ] Ręcznie zepsuty `data.json` → czytelny komunikat, aplikacja się nie wywala.

**Commity:** (osobno) `Podłącz CookingService do interfejsu`, `Dodaj widok przepisów`, `Dodaj listę zakupów i zatwierdzanie zakupów w interfejsie`, `Dodaj przycisk Ugotuj`

### 2.8 Przegląd testów przed wydaniem

Przejdźcie po klasach domeny i sprawdźcie, czy **każda** ma testy, także na błędne dane. Uruchomcie raport pokrycia (opcjonalnie, to dobry sposób, by zobaczyć, czego nie przetestowano):

```bash
uv add --dev pytest-cov
uv run pytest --cov=src/fridge_manager/domain --cov-report=term-missing
```

Linie wymienione w kolumnie `Missing` to kod bez testów. Nie chodzi o 100%, tylko o to, żeby żadna klasa domeny nie została bez testu.

**Commit:** `Uzupełnij testy przypadków brzegowych`

### 2.9 Wydanie v0.2.0

Powtórzcie listę z [kroku 1.9](#19-wydanie-v010), zmieniając numery:

- [ ] `version = "0.2.0"` w `pyproject.toml`,
- [ ] Testy zielone, `git status` czysty, nic zbędnego w `git ls-files`,
- [ ] `git tag v0.2.0` i `git push origin v0.2.0`,
- [ ] paczka pobrana z Releases działa (w tym **zapis danych w katalogu użytkownika**),
- [ ] wgrana na UPeL do zadania „2. wersja pośrednia”,
- [ ] w README sekcje „Dane aplikacji” i „CI/CD” odzwierciedlają stan faktyczny, a rejestr LLM jest aktualny.

**Gotowe, gdy:** scenariusz z mlekiem działa z paczki `.exe`.

## Etap 3: wersja v1.0.0

**Cel:** kalorie i dziennik, jednostki kuchenne, wybrane dodatki, dopracowanie, **kompletna dokumentacja** i przygotowanie do prezentacji.

Nie zaczynajcie dodatków, zanim rdzeń z etapu 2 nie będzie pewny.

### 3.1 Kalorie i dziennik: `domain/journal.py`

- **`JournalEntry`** (`frozen dataclass`): `day: date`, `recipe_name`, `portions`, `kcal`.
- **`CalorieJournal`**: prywatna lista wpisów; `add(entry)`, `entries()` (kopia, od najnowszych), `total_for(day) -> float`.
- W `Recipe` dodajcie `total_calories(portions)`: suma `food.calories(ingredient.per_portion)` pomnożona przez liczbę porcji.
- `AppData` dostaje pole `journal` (z `default_factory`).
- `CookingService.cook(...)` po udanym odjęciu składników dopisuje wpis do dziennika. Dodatkowy parametr `eaten=None` pozwala zapisać mniej porcji, niż ugotowano (domyślnie tyle samo), ale nie więcej niż ugotowane (`InvalidQuantityError`).
- **Serializacja:** dopiszcie dziennik do JSON. Przy wczytywaniu **starego pliku bez `journal`** użyjcie pustego dziennika (plik z v0.2.0 ma nadal się wczytywać).

> 💡 **Po co obsługa starego formatu?** Prawdziwy użytkownik ma już dane z poprzedniej wersji. Aplikacja, która po aktualizacji nie otwiera swojego pliku, to zły program. Test „wczytaj plik v0.2.0” to dobra praktyka i dobry temat na pytanie na prezentacji.

**Testy:** kalorie przepisu (ręcznie policzone: 2 porcje naleśników), wpis do dziennika po `cook`, suma dnia (kilka wpisów, różne dni), `eaten > portions` → błąd, stary JSON bez `journal`.

**Commity:** `Dodaj CalorieJournal i JournalEntry`, `Dodaj total_calories do Recipe`, `Zapisuj kalorie w dzienniku po ugotowaniu`, `Dodaj dziennik do serializacji JSON`

### 3.2 Widok dziennika: `ui/journal_view.py`

Lista wpisów (data, przepis, porcje, kcal) i suma kcal na dziś. Dodajcie przycisk „Dziennik” do nawigacji. Opcjonalnie: cel dzienny (np. pole z liczbą kcal) i informacja, ile jeszcze zostało.

**Commit:** `Dodaj widok dziennika kalorii`

### 3.3 Jednostki kuchenne

Dopiszcie do `Unit`: szklanka (`CUP`, 250 ml), łyżka (`TBSP`, 15 ml), łyżeczka (`TSP`, 5 ml). Wszystkie mają `kind` = `VOLUME`, a `factor` odpowiednio 250, 15 i 5. Zaktualizujcie `_KINDS`, `_FACTORS` i listy w interfejsie.

> 💡 **Po co to ćwiczenie?** Zobaczcie, ile plików musieliście ruszyć: praktycznie tylko `quantity.py` (i testy). `Fridge`, `Recipe` i serwis działają od razu, bo polegają na `kind` i `factor`. Tak wygląda dobry projekt: nowa funkcja to małe zmiany w jednym miejscu.

**Testy:** `1 CUP` mleka to 250 ml; łyżeczki na litry; łyżka mąki → `IncompatibleUnitError`. Nowe jednostki w parametryzowanym teście `Unit`.

**Commit:** `Dodaj jednostki kuchenne (szklanka, łyżka, łyżeczka)`

### 3.4 Dodatki do wyboru

Wybierzcie **2–3** według czasu (każdy ma konkretne miejsce w kodzie):

| Dodatek | Pomysł | Gdzie |
| :--- | :--- | :--- |
| **Opakowania** | produkt ma `package_size`; lista zakupów zaokrągla w górę do pełnych opakowań (potrzeba 200 ml, mleko w 1 l, kup 1 opakowanie) | `FoodItem`, `ShoppingItem` |
| **Wiele przepisów naraz** | jedna lista zakupów z sumą składników z kilku przepisów | `CookingService` |
| **Edycja i usuwanie** | usuwanie przepisu i produktu z lodówki, korekta ilości | `CookingService`, widoki |
| **Eksport listy zakupów** | zapis listy do pliku `.txt` | nowa funkcja w `storage/` |
| **Przeliczanie masa ↔ sztuki** | „100 g jajka” w przepisie przy zapasie w sztukach (przez `grams_per_piece`) | `FoodItem.to_base` w klasach pochodnych (tu polimorfizm naprawdę pracuje) |
| **Terminy ważności** | data ważności i lista „psuje się niedługo” | `StockItem`, widok lodówki |

Każdy dodatek robicie tak samo: testy → logika w `domain/` → serializacja (jeśli trzeba) → widok. Oddzielny commit na każdy krok.

### 3.5 Dopracowanie

- Puste stany w widokach („Lodówka jest pusta”).
- Czytelne formatowanie ilości (`1 l` zamiast `1000 ml`) i liczb (bez długich ułamków).
- Wszędzie czytelne komunikaty błędów po polsku.
- Okno ma sensowny tytuł i rozmiar, a przyciski są opisane.
- Usuńcie martwy kod, nieużywane importy, wydruki diagnostyczne (`print`) i zakomentowane fragmenty.
- Opcjonalnie narzędzie Ruff: `uv add --dev ruff`, potem `uv run ruff check .` wskaże nieużywane importy i proste błędy.

### 3.6 Dokumentacja końcowa

`README.md` ma zawierać (wymaganie prowadzącego):

- [ ] opis projektu i funkcji (zaktualizowany, ze zrzutem ekranu),
- [ ] instrukcję budowania, uruchomienia i testów (sprawdźcie ją, **wykonując krok po kroku na czystym folderze**),
- [ ] **diagram klas** zgodny z kodem (nazwy klas i metod). Przejrzyjcie go klasa po klasie,
- [ ] **mapę koncepcji obiektowych** z prawdziwymi nazwami plików i klas,
- [ ] **rejestr użycia LLM** kompletny: każdy plik lub fragment, narzędzie, co zrobiono i jak zweryfikowano. Wpiszcie wyraźnie: *wygenerowano i użyto bez zmian*, *wygenerowano i zmieniono* albo *tylko porada*,
- [ ] brak oznaczeń 🚧 (wyszukajcie w VS Code: `Ctrl+Shift+F`, tekst `🚧`).

Sprawdźcie też, czy **commity** mają stopki `LLM:` tam, gdzie była pomoc modelu (przejrzyjcie `git log`).

**Commit:** `Uzupełnij dokumentację końcową`

### 3.7 Kontrola jakości przed tagiem

- [ ] `uv run pytest` zielone, pokrycie domeny sensowne (2.8).
- [ ] CI na `main` zielone.
- [ ] `git ls-files`: nic z `.venv`, `dist`, `build`, `data.json`, `.vscode`, haseł ani tokenów.
- [ ] Historia commitów: małe, opisowe commity od **obu** osób od pierwszego dnia (`git log --format="%an: %s"`).
- [ ] Wszystko, co jest w `README.md`, jest prawdą.

### 3.8 Wydanie v1.0.0

- [ ] `version = "1.0.0"` w `pyproject.toml`,
- [ ] `git tag v1.0.0`, `git push origin v1.0.0`,
- [ ] przebieg **Wydanie** zielony, paczka w Releases,
- [ ] **pobierzcie paczkę z Releases** na „czysty” komputer lub folder (najlepiej bez zainstalowanego Pythona i uv) i uruchomcie,
- [ ] wgrajcie na UPeL do zadania „Wersja końcowa”.

Oceniany jest **stan repozytorium w commicie z tagiem `v1.0.0`** i paczka zbudowana z tego tagu, więc po tagu nie zmieniajcie niczego na tym tagu.

## Jak pisać testy

### Podstawy

- Każdy plik `tests/test_*.py`, każda funkcja `test_*`.
- Uruchamianie: `uv run pytest` (wszystko), `uv run pytest tests/test_fridge.py` (jeden plik), `uv run pytest -k consume` (testy z „consume” w nazwie), `uv run pytest -x` (stop po pierwszym błędzie).
- Struktura testu **Arrange–Act–Assert**: przygotuj, wykonaj, sprawdź. Jeden test sprawdza jedną rzecz.
- Nazwy mówią, co się dzieje: `test_consume_wiecej_niz_jest_rzuca_insufficient_stock`.

### Przykład (pierwszy prawdziwy test)

```python
import pytest

from fridge_manager.domain.errors import InvalidQuantityError
from fridge_manager.domain.quantity import Quantity, Unit


@pytest.mark.parametrize("amount", [0, -1, float("nan"), float("inf")])
def test_quantity_odrzuca_niepoprawna_ilosc(amount: float) -> None:
    with pytest.raises(InvalidQuantityError):
        Quantity(amount, Unit.G)
```

### Narzędzia, których będziecie używać

| Narzędzie | Do czego |
| :--- | :--- |
| `pytest.raises(Wyjątek)` | sprawdzenie, że kod rzuca błąd |
| `pytest.approx(x)` | porównanie liczb zmiennoprzecinkowych z tolerancją |
| `@pytest.mark.parametrize` | ten sam test dla wielu danych |
| `@pytest.fixture` | wspólne przygotowanie (np. lodówka z mlekiem); fixture'y wspólne dla plików trafiają do `tests/conftest.py` |
| `tmp_path` | wbudowany tymczasowy folder (testy JSON) |
| `monkeypatch` | tymczasowa zmiana zmiennej środowiskowej |

### Co testować w każdej klasie domeny

Dla każdej klasy z `domain/` (wymaganie prowadzącego: „logika każdej klasy, w tym przypadki brzegowe i błędne dane”):

1. **Szczęśliwa ścieżka:** typowe użycie.
2. **Błędne dane:** zero, wartości ujemne, puste teksty, `nan`, zła jednostka, nieistniejący produkt.
3. **Granice:** dokładnie tyle, ile jest; ułamki; bardzo duże liczby.
4. **Brak efektów ubocznych po błędzie:** po wyjątku stan obiektu jest taki jak przed wywołaniem.
5. **Hermetyzacja:** zwracane kolekcje to kopie, niemutowalne obiekty rzeczywiście są niemutowalne.

> 💡 **Zasada:** gdy znajdziecie błąd ręcznie w aplikacji, najpierw napiszcie test, który go odtwarza (czerwony), potem naprawcie kod (zielony). Wtedy błąd nigdy nie wróci.

## Git i praca w zespole

### Gałęzie i Pull Requesty

- `main` jest zawsze zielone i zawsze działa.
- Nowa praca: `git switch -c feat/fridge` (przedrostki: `feat/`, `test/`, `ci/`, `docs/`, `fix/`).
- Wypchnięcie gałęzi: `git push -u origin feat/fridge`, potem **Pull Request** do `main`. CI uruchomi testy.
- Drugą osobę prosicie o przejrzenie PR (to też sposób, żeby **poznać kod, którego się nie pisało**).
- Scalamy zwykłym merge'em (bez „squash”), żeby zachować małe commity i autorstwo każdego z Was.
- Po scaleniu: `git switch main`, `git pull`, usuwamy gałąź.

### Commity

- Małe i spójne: jedna zmiana logiczna na commit (nie „dodałem wszystko”).
- Pierwsza linia: tryb rozkazujący po polsku, do ok. 70 znaków (*Dodaj*, *Napraw*, *Zmień*).
- Opcjonalnie w treści: **dlaczego** zmieniamy.
- Gdy część napisał model językowy, **stopka `LLM:`** na końcu.
- Gdy programowaliście razem na jednym komputerze: `Co-authored-by: Imię Nazwisko <mail>`.

Przykład:

```text
Dodaj walidację ilości w Quantity

Ilość musi być skończona i dodatnia, inaczej reszta programu musiałaby
sprawdzać to w wielu miejscach.

LLM: Claude; szkielet __post_init__ wygenerowany, warunek dla NaN i inf poprawiony ręcznie, testy napisane samodzielnie
```

### Rejestr LLM: nawyk

Po każdym commicie ze stopką `LLM:` dopiszcie wiersz do tabeli w `README.md`. Trzy typy wpisów, które prowadzący chce rozróżniać:

1. **wygenerowano i użyto bez zmian**,
2. **wygenerowano, potem zmieniono** (napiszcie co),
3. **tylko porada** (wyjaśnienie, przegląd, podpowiedź, a kod napisany samodzielnie).

Dopisujcie też to, **jak zweryfikowaliście** kod (testy, ręczne uruchomienie, przegląd).

> ⚠️ Nieoznaczone użycie LLM jest traktowane jak niesamodzielna praca. Oznaczone nie obniża oceny. Odpowiadacie za cały kod w repozytorium i na prezentacji musicie umieć go wyjaśnić i zmienić.

## Prezentacja

Pokazujecie działający program **uruchomiony z paczki wydania**, omawiacie pomysł i architekturę, odpowiadacie na pytania.

### Plan pokazu (ok. 5–10 minut)

1. Cel w jednym zdaniu i scenariusz z mlekiem na żywo: kupno 1 l → przepis → lista zakupów → „Kupiłem” → „Ugotuj” → zostało 800 ml.
2. Pokazanie błędu: próba ugotowania bez składników → komunikat, lodówka bez zmian.
3. Architektura: warstwy `domain` / `storage` / `ui` i dlaczego `domain` nie zna interfejsu.
4. Mapa 6 koncepcji OOP na prawdziwych klasach (z README).
5. Testy i CI: zielony pipeline, tagi, wydania.

### Pytania, które mogą paść (przećwiczcie odpowiedzi)

- Dlaczego `FoodItem` jest abstrakcyjna? Co się stanie, jeśli dodamy nowy rodzaj produktu?
- Gdzie w kodzie działa polimorfizm? Pokaż wywołanie `to_base` / `to_grams` w `Fridge`.
- Czym kompozycja różni się od dziedziczenia? Pokaż przykład z `Recipe`.
- Dlaczego `Quantity` jest niemutowalna?
- Dlaczego `cook` najpierw sprawdza listę zakupów, a dopiero potem odejmuje?
- Dlaczego `domain` nie importuje `flet`? Jak zmieniłbyś interfejs na terminalowy?
- Jak zmienić format zapisu z JSON na bazę SQLite? (odpowiedź: nowa klasa po `StorageRepository`, bez zmian w serwisie)
- Pokaż w repozytorium, który fragment napisał model językowy i jak go sprawdziłeś.
- *Zmień na żywo:* dodaj jednostkę (np. „szczypta”), zmień regułę zaokrąglania, dopisz test.

## Rozwiązywanie problemów

| Problem | Przyczyna i rozwiązanie |
| :--- | :--- |
| `uv` lub `git` „nie jest rozpoznawane” | Zamknij i otwórz terminal (albo VS Code) po instalacji, żeby odświeżyć `PATH`. |
| `ModuleNotFoundError: fridge_manager` w testach | Brak `pythonpath = ["src"]` w `[tool.pytest.ini_options]` lub brakujące `__init__.py` w pakietach. |
| Pylance podkreśla importy z `src` | Wybierz interpreter `.venv` (`Ctrl+Shift+P → Python: Select Interpreter`) i sprawdź `python.analysis.extraPaths`. |
| Okno Flet się nie otwiera | Uruchom `uv run flet doctor`. Sprawdź, czy `flet-desktop` jest zainstalowane (`uv sync`). Na Linuksie brakuje bibliotek systemowych (zob. dokumentacja Flet). |
| Kontrolka Flet „nie istnieje” lub zmieniła nazwę | Flet 1.x zmienił API względem starszych poradników. Sprawdź dokumentację zgodną z zainstalowaną wersją (`uv run flet --version`). |
| `pytest: no tests ran` (kod wyjścia 5) | W `tests/` nie ma żadnego testu. Dodaj test lub zostaw `test_smoke.py`, aż pojawią się prawdziwe. |
| CI: `uv sync --locked` zgłasza, że lock jest nieaktualny | Zmieniono `pyproject.toml` bez `uv lock`. Uruchom `uv lock` lub `uv sync` i zacommituj `uv.lock`. |
| Pipeline wydania: „Tag nie zgadza się z wersją” | Zapomniano podnieść `version` w `pyproject.toml` przed tagiem. Usuń tag, popraw wersję, otaguj ponownie. |
| `flet pack` w CI nie znajduje `dist/FridgeManager.exe` | Sprawdź lokalnie, co powstaje w `dist/` i dopasuj ścieżkę w `release.yml`. Zobacz też „Plan B” w kroku 1.7. |
| Windows SmartScreen / antywirus blokuje `.exe` | Program nie jest podpisany certyfikatem. **Więcej informacji → Uruchom mimo to**. Opiszcie to w README. Antywirusy czasem fałszywie alarmują przy PyInstallerze. |
| Konflikt przy scalaniu | `git pull` na `main`, `git merge main` do swojej gałęzi, rozwiąż konflikty w VS Code (przyciski „Accept…”), zacommituj. |
| Nie wiem, co jest w repozytorium | `git ls-files` pokazuje pliki śledzone przez Git, `git status` zmiany lokalne. |

## Checklista wymagań prowadzącego

Pełna treść wymagań: [WYMAGANIA_PROJEKTU.md](WYMAGANIA_PROJEKTU.md). Gdzie je realizujemy:

| Wymaganie | Gdzie / kiedy |
| :--- | :--- |
| Min. 3 z 6 koncepcji OOP, uzasadnione | wszystkie 6 w domenie, opis w `README.md` (3.6) |
| Mapa koncepcji w dokumentacji | `README.md`, sekcja „Mapa koncepcji obiektowych” |
| Repozytorium od pustego, historia pracy | Etap 0.3, potem małe commity |
| `.gitignore`, brak plików IDE i wyników budowania | krok 0.4, kontrola w 1.9 i 3.7 |
| Wkład każdej osoby widoczny w historii | tożsamość Git w 0.3, PR-y i commity obu osób |
| Testy jednostkowe (pytest), brzegowe i błędne dane | kroki 1.1–1.4, 2.1–2.8, sekcja „Jak pisać testy” |
| Testy jednym poleceniem opisanym w README | `uv run pytest` |
| Pipeline testowy na `main` | krok 1.6 |
| Pipeline wydania tylko dla tagu `vX.Y.Z`, paczka z numerem wersji | krok 1.7 |
| Paczka gotowa do uruchomienia na wskazanej platformie | `.exe` na Windows, wskazane w README |
| Trzy wydania zbudowane przez pipeline | 1.9, 2.9, 3.8 |
| Paczki z Releases wgrane na UPeL | 1.9, 2.9, 3.8 |
| README: opis, instrukcja, diagram klas, mapa OOP, rejestr LLM | 3.6 |
| Oznaczanie LLM w commicie i w README | sekcja „Git i praca w zespole” |
| Prezentacja z paczki wydania | sekcja „Prezentacja” |
| Zgłoszenie tematu na UPeL | krok 0.3 |

Terminy z harmonogramu UPeL wpiszcie tutaj, żeby były pod ręką:

| Etap | Termin |
| :--- | :--- |
| Zgłoszenie tematu | |
| `v0.1.0` | |
| `v0.2.0` | |
| `v1.0.0` i prezentacja | |
