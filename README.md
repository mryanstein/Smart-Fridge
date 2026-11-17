# Smart-Fridge

Czy miałeś kiedyś problem z tworzeniem listy zakupów? To ostatni raz, bo dzięki naszej wspaniałej aplikacji możesz wygenerować całą spersonalizowaną listę zakupów jednym kliknięciem. Nie czekaj, promocja -70% trwa tylko dziś.

## 🛠️ Instalacja i konfiguracja środowiska

Projekt wykorzystuje menedżer pakietów **[uv](https://docs.astral.sh/uv/)** oraz izolowane środowisko wirtualne `.venv`.

### Wymagania wstępne

* Zainstalowany **Python 3.10+**
* Zainstalowane narzędzie **uv** (jeśli nie masz, instalacja jednym poleceniem):
  * **Windows (PowerShell):**
    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
  * **macOS / Linux:**
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### 1. Sklonowanie repozytorium i utworzenie środowiska wirtualnego

```bash
git clone <LINK_DO_REPOZYTORIUM>
cd <NAZWA_FOLDERU_PROJEKTU>

# Utworzenie środowiska wirtualnego w folderze .venv
uv venv
```

### 2. Aktywacja środowiska wirtualnego

* **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
* **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

*(Po poprawnej aktywacji przed ścieżką w terminalu pojawi się prefiks `(.venv)`).*

### 3. Pobranie wymaganych bibliotek (`requirements.txt`)

Przy aktywnym środowisku `.venv` zainstaluj wszystkie zależności projektu:

```bash
uv pip install -r requirements.txt
```

### 4. Uruchomienie aplikacji i testów

* **Uruchomienie aplikacji (Flet):**
  ```bash
  python main.py
  ```
* **Uruchomienie testów jednostkowych:**
  ```bash
  pytest
  ```

### Dodawanie nowych bibliotek (dla zespołu)

Jeśli doinstalujesz nową paczkę przez `uv pip install <nazwa_pakietu>`, zaktualizuj plik zależności przed wysłaniem commita:

```bash
uv pip freeze > requirements.txt
```

Druga osoba po pobraniu zmian (`git pull`) aktualizuje swoje środowisko poleceniem:

```bash
uv pip install -r requirements.txt
```
