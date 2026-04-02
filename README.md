# ING Cookie Consent — Testy automatyczne

Automatyczne testy weryfikujące działanie mechanizmu zgody na pliki cookie na stronie [ing.pl](https://www.ing.pl), zaimplementowane w Pythonie z wykorzystaniem frameworka [Playwright](https://playwright.dev/python/).

## Scenariusze testowe

| Test | Opis |
|------|------|
| `test_cookie_banner_appears` | Banner z przyciskiem „Dostosuj" pojawia się na stronie głównej |
| `test_analytics_cookie_set_after_consent` | Po wyrażeniu zgody analitycznej ciastko `cookiePolicyGDPR` ma wartość `3` lub `7` |
| `test_no_consent_cookies_without_interaction` | Bez interakcji z bannerem nie pojawiają się ścisłe ciastka marketingowe (`_fbp`, `_gcl_au`) |

## Wymagania

- Python 3.12+
- pip

## Instalacja

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/<twoj-login>/<nazwa-repo>.git
cd <nazwa-repo>

# 2. Utwórz i aktywuj środowisko wirtualne
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Zainstaluj przeglądarki Playwright
playwright install --with-deps
```

## Uruchomienie testów

### Wszystkie przeglądarki równolegle (domyślnie przez pytest.ini)

```bash
pytest main.py -v
```

Konfiguracja w `pytest.ini` uruchamia testy jednocześnie na **Chromium**, **Firefox** i **WebKit** (`--numprocesses auto`).

### Jedna wybrana przeglądarka

```bash
pytest main.py --browser chromium -v
pytest main.py --browser firefox -v
pytest main.py --browser webkit -v
```

### Tryb wizualny (z otwartą przeglądarką)

```bash
pytest main.py --headed --browser chromium -v
```

### Z wydrukiem debug (ciastka w konsoli)

```bash
pytest main.py --headed -s
```

## Pipeline CI/CD (GitHub Actions)

Plik `.github/workflows/playwright.yml` definiuje pipeline, który:

- uruchamia się automatycznie przy każdym push / pull request na branch `main`
- uruchamia testy **równolegle na 3 przeglądarkach** (Chromium, Firefox, WebKit) jako osobne joby
- zapisuje artefakty z wynikami testów

### Podgląd wyników w GitHub

1. Wejdź w zakładkę **Actions** w swoim repozytorium
2. Wybierz workflow **Playwright Tests — ING Cookie Consent**
3. Każdy job (`chromium`, `firefox`, `webkit`) pokazuje wyniki osobno

## Struktura projektu

```
.
├── main.py                          # Testy Playwright
├── pytest.ini                       # Konfiguracja pytest (multi-browser)
├── requirements.txt                 # Zależności Python
├── README.md                        # Ten plik
└── .github/
    └── workflows/
        └── playwright.yml           # Pipeline GitHub Actions
```

## Uwagi techniczne

- Każdy test startuje z **wyczyszczonymi ciastkami** (fixture `clear_storage`) — gwarantuje to powtarzalność wyników niezależnie od poprzednich uruchomień
- ING koduje poziom zgody numerycznie w ciastku `cookiePolicyGDPR`: `1` = tylko techniczne, `3` = techniczne + analityczne, `7` = pełna zgoda
- Strona używa **niestandardowych przełączników** (`<div role="switch">`) zamiast standardowych `<input type="checkbox">`
