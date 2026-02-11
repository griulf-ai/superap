# SuperAP — S&P 500 Analyst Recommendations Dashboard

En web-app som henter analytikeranbefalinger fra Yahoo Finance for alle S&P 500-aksjer og viser dem i et sortérbart dashboard.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)

---

## Hva gjør appen?

- Henter listen over alle ~500 aksjer i S&P 500 fra Wikipedia
- Henter analytikerdata fra Yahoo Finance for hver aksje (anbefaling, kursmål, sektor, markedsverdi)
- Lagrer alt i en lokal SQLite-database
- Viser et dashboard med en sortérbar tabell der du kan filtrere og søke
- Oppdaterer dataene automatisk hver dag kl. 06:00 UTC

---

## Installasjon steg for steg

### 1. Sjekk at du har Python installert

Åpne en terminal og skriv:

```bash
python3 --version
```

Du trenger **Python 3.10 eller nyere**. Hvis du ikke har Python:

- **Mac**: `brew install python3` (krever [Homebrew](https://brew.sh))
- **Windows**: Last ned fra [python.org/downloads](https://www.python.org/downloads/) — husk å hake av "Add Python to PATH" under installasjonen
- **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install python3 python3-venv python3-pip`

### 2. Last ned prosjektet

```bash
git clone https://github.com/griulf-ai/superap.git
cd superap
```

Eller hvis du allerede har mappen, bare naviger til den:

```bash
cd superap
```

### 3. Opprett et virtuelt miljø

Et virtuelt miljø holder prosjektets avhengigheter adskilt fra resten av systemet:

```bash
python3 -m venv .venv
```

Dette lager en mappe `.venv/` inne i prosjektet. Du trenger bare å gjøre dette **én gang**.

### 4. Aktiver det virtuelle miljøet

**Mac / Linux:**
```bash
source .venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (cmd):**
```cmd
.venv\Scripts\activate.bat
```

Når miljøet er aktivt ser du `(.venv)` foran prompten din:
```
(.venv) bruker@maskin:~/superap$
```

> Du må aktivere miljøet **hver gang** du åpner en ny terminal for å jobbe med prosjektet.

### 5. Installer avhengigheter

```bash
pip install -r requirements.txt
```

Dette installerer Flask, yfinance, pandas og de andre pakkene appen trenger. Det tar vanligvis 1–2 minutter.

### 6. Start appen

```bash
python app.py
```

Du skal se noe som dette i terminalen:

```
2026-02-11 12:00:00 [INFO] src.scheduler: Scheduler started: daily refresh at 06:00 UTC
 * Running on http://0.0.0.0:5000
```

### 7. Åpne dashboardet

Gå til **http://localhost:5000** i nettleseren din.

Første gang vil tabellen være tom. Klikk **"Refresh Data"** for å starte innhentingen av data. Dette tar ca. 25–30 minutter fordi appen henter data for alle ~500 aksjer med forsinkelse mellom hver for å unngå å bli blokkert av Yahoo Finance.

Etter at dataene er hentet kan du:
- **Sortere** ved å klikke på kolonneoverskriftene
- **Søke/filtrere** med søkefeltet
- **Klikke på en ticker** for å se detaljert informasjon om den aksjen

---

## Daglig bruk

Når appen kjører, oppdateres dataene automatisk hver dag kl. 06:00 UTC. Du trenger bare å:

1. Aktivere det virtuelle miljøet: `source .venv/bin/activate`
2. Starte appen: `python app.py`
3. Åpne http://localhost:5000

For å **stoppe appen**, trykk `Ctrl+C` i terminalen.

---

## Konfigurasjon (valgfritt)

Du kan endre oppførselen med miljøvariabler:

```bash
# Endre tidspunkt for daglig oppdatering (standard: 06:00 UTC)
export SUPERAP_REFRESH_HOUR=8
export SUPERAP_REFRESH_MINUTE=30

# Endre plassering av databasefilen
export SUPERAP_DB=/sti/til/min/database.db

# Start appen med de nye innstillingene
python app.py
```

---

## Feilsøking

**"python3: command not found"**
→ Python er ikke installert eller ikke i PATH. Se steg 1.

**"No module named flask" eller lignende**
→ Du har glemt å aktivere det virtuelle miljøet. Kjør `source .venv/bin/activate` først.

**Tabellen er tom etter refresh**
→ Yahoo Finance kan ha blokkert forespørslene. Sjekk terminalen for feilmeldinger. Prøv igjen etter noen timer.

**"Address already in use"**
→ En annen prosess bruker port 5000. Stopp den andre prosessen, eller endre porten: `flask run --port 5001`
