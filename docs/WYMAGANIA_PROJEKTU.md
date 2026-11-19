# Projekt programistyczny – wymagania

> Treść wymagań od prowadzącego, przeniesiona bez zmian merytorycznych.

Celem projektu jest samodzielne przeprowadzenie małego projektu programistycznego od pustego repozytorium do wydanej wersji. Obejmuje to kod produkcyjny, testy, dokumentację i automatyczny proces budowania. Projekt może być napisany w **dowolnym języku**, który wspiera programowanie obiektowe. Temat wybierasz samodzielnie.

| Etap | Co oddać |
| :--- | :--- |
| **Zgłoszenie tematu** | tytuł i link do repozytorium oraz ewentualnie lista współpracowników w aktywności |
| **1. wersja pośrednia** | tag np. `v0.1.0`, paczka wgrana na UPeL |
| **2. wersja pośrednia** | tag np. `v0.2.0`, paczka wgrana na UPeL |
| **Wersja końcowa** | tag `v1.0.0`, paczka wgrana na UPeL, następnie prezentacja projektu |

## 1. Koncepcje obiektowe

Projekt musi w uzasadniony sposób wykorzystywać **co najmniej 3 z 6** poniższych koncepcji. Klasa, która istnieje tylko po to, żeby „odhaczyć” wymaganie, się nie liczy.

1. **Hermetyzacja.** Stan obiektów jest prywatny, a zmienia się go wyłącznie przez metody, które pilnują poprawności danych.
2. **Abstrakcja.** Co najmniej jeden interfejs lub klasa abstrakcyjna, która jest wykorzystywana do realizacji funkcjonalności.
3. **Dziedziczenie.** Co najmniej jedna hierarchia z dwiema lub więcej klasami pochodnymi.
4. **Polimorfizm.** Obiekty różnych klas obsługiwane przez wspólny typ bazowy (wywołania metod wirtualnych lub interfejsu).
5. **Kompozycja.** Obiekty zbudowane z innych obiektów, nie tylko przez dziedziczenie.
6. **Obsługa błędów.** Własne wyjątki lub inny jawny mechanizm sygnalizowania błędów, stosowany konsekwentnie.

Każdą wykorzystaną koncepcję **opisz** w dokumentacji (odrębne `docs/` lub `README.md`): wskaż klasy i pliki, w których ją zastosowano, i wyjaśnij, dlaczego jest tam potrzebna (sekcja 4).

## 2. Repozytorium i praca z Gitem

- Repozytorium na GitHubie lub GitLabie, publiczne albo z dostępem dla prowadzącego.
- Historia zaczyna się od pustego repozytorium i pokazuje rzeczywisty przebieg pracy. Projekt wrzucony jednym commitem nie zostanie przyjęty.
- Commity są małe i spójne, a ich opisy mówią, *co* i *dlaczego* się zmieniło.
- Plik `.gitignore`, a w repozytorium brak plików wynikowych kompilacji, plików IDE i danych wrażliwych (haseł, tokenów).
- Przy pracy zespołowej historia commitów pokazuje wkład każdej osoby.

## 3. Testy

- Automatyczne testy jednostkowe w frameworku właściwym dla języka (np. GoogleTest lub Catch2 dla C++, JUnit dla Javy, pytest dla Pythona).
- Testy obejmują logikę każdej klasy z warstwy domenowej, w tym przypadki brzegowe i błędne dane.
- Testy uruchamia się jednym poleceniem opisanym w README, a pipeline uruchamia je automatycznie dla gałęzi głównej.

## 4. Dokumentacja

Plik `README.md` w katalogu głównym repozytorium lub inaczej zorganizowana dokumentacja (np. `docs/`) zawiera:

1. opis projektu i jego funkcji,
2. instrukcję budowania, uruchomienia i uruchomienia testów,
3. **diagram klas** (np. w Mermaid lub PlantUML albo jako obraz),
4. **mapę koncepcji obiektowych**: tabelę „koncepcja → klasy i pliki → uzasadnienie” dla każdej z wykorzystanych koncepcji (co najmniej 3),
5. **rejestr użycia LLM** (sekcja 6).

## 5. Pipeline CI/CD

- **Pipeline testowy** uruchamia się przy każdym pushu do **gałęzi głównej** (`main` lub `master`): buduje projekt i uruchamia testy. Czerwony pipeline na gałęzi głównej oznacza błąd do naprawienia. Na pozostałych gałęziach pipeline nie jest wymagany.
- **Pipeline wydania** uruchamia się **wyłącznie** dla commitów oznaczonych tagiem wersji w formacie `vX.Y.Z` ([wersjonowanie semantyczne](https://semver.org/lang/pl/)). Buduje paczkę z gotowym programem i publikuje ją jako wydanie (GitHub Releases lub GitLab Releases). Nazwa paczki zawiera numer wersji.
- Paczka zawiera program gotowy do uruchomienia na wskazanej w README platformie: plik wykonywalny, archiwum, pakiet albo obraz kontenera.
- Wymagane są co najmniej **trzy wydania**: dwa pośrednie (np. `v0.1.0`, `v0.2.0`) i jedno końcowe `v1.0.0`. Każde ma paczkę zbudowaną przez pipeline, a nie dodaną ręcznie.
- Paczkę z **każdego z trzech wydań** pobierz z wydania w repozytorium i wgraj na UPeL do odpowiedniego zadania w terminie z harmonogramu.
- Konfiguracja pipeline'u jest częścią repozytorium (`.github/workflows/` lub `.gitlab-ci.yml`).

## 6. Korzystanie z LLM i innych narzędzi

Możesz korzystać z dowolnych narzędzi, także z modeli językowych (ChatGPT, Claude, Copilot itp.). Każde użycie LLM przy tworzeniu kodu, testów, dokumentacji lub konfiguracji musi być **jawnie oznaczone** w dwóch miejscach.

**a) W commicie** – na końcu opisu dodaj stopkę (jedną na każde narzędzie):

```text
Dodaj walidację danych w klasie Rezerwacja

LLM: Claude; szkielet Rezerwacja::waliduj() wygenerowany, obsługa dat zmieniona, testy dopisane ręcznie
```

**b) W dokumentacji** – rejestr użycia LLM w README:

| Plik / fragment | Narzędzie | Do czego użyto i jak zweryfikowano |
| :--- | :--- | :--- |
| `src/Rezerwacja.cpp`, `waliduj()` | Claude | wygenerowany szkielet walidacji; zmieniono obsługę dat, dopisano 4 testy brzegowe |

Opis powinien jasno mówić, czy LLM wygenerował kod, który został użyty bez zmian, wygenerował kod, który później zmieniłeś, czy tylko doradzał (wyjaśnienie, przegląd, podpowiedź), a kod napisałeś samodzielnie.

> **Ważne:** Odpowiadasz za cały kod w repozytorium, niezależnie od tego, kto lub co go napisało. Podczas prezentacji musisz umieć wyjaśnić i zmodyfikować każdy fragment. Nieoznaczone użycie LLM jest traktowane jak niesamodzielna praca. Samo oznaczone użycie LLM nie obniża oceny.

## 7. Oddanie i prezentacja

- Oceniany jest stan repozytorium w commicie oznaczonym tagiem `v1.0.0` i paczka zbudowana z tego tagu, wgrana na UPeL.
- Podczas prezentacji pokazujesz działający program uruchomiony z paczki wydania, omawiasz pomysł, architekturę i odpowiadasz na pytania.
