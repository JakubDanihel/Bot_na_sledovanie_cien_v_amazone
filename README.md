# Bot_na_sledovanie_cien_v_amazone
Jednoduchy bot na sledovanie ceny produktu v Pythone3.10.

## 1. Účel skriptu

Tento Python skript slúži ako automatizovaný nástroj (bot) na sledovanie ceny vybraného produktu na webovej stránke Amazon. Jeho hlavnou úlohou je:

1.  Načítať webovú stránku produktu.
2.  Získať (scrapovať) aktuálnu cenu produktu.
3.  Porovnať ju s vopred nastavenou cieľovou cenou.
4.  Ak je aktuálna cena nižšia ako cieľová, odoslať používateľovi e-mailové upozornenie.

Skript je navrhnutý tak, aby bol ľahko konfigurovateľný a bezpečný, keďže citlivé údaje (ako heslá) oddeľuje od hlavného kódu.

## 2. Príprava a inštalácia

Pred spustením skriptu je potrebné vykonať nasledujúce kroky:

### a) Inštalácia potrebných knižníc

Skript vyžaduje nasledujúce Python knižnice. Nainštalujte ich pomocou príkazu `pip`:

```sh
pip install requests beautifulsoup4 python-dotenv
```

-   `requests`: Na odosielanie HTTP požiadaviek a sťahovanie obsahu webových stránok.
-   `beautifulsoup4`: Na spracovanie (parsovanie) HTML kódu a extrakciu dát.
-   `python-dotenv`: Na načítanie citlivých údajov z `.env` súboru.

### b) Konfigurácia v súbore `.env`

Vytvorte v hlavnom priečinku projektu súbor s názvom `.env`. Tento súbor bude obsahovať citlivé údaje, ktoré skript potrebuje na odoslanie e-mailu. Súbor by mal mať nasledujúci formát:

```
MY_EMAIL="vas_email@gmail.com"
MY_PASSWORD="vase_heslo_pre_aplikaciu"
RECIPIENT_EMAIL="email_prijemcu@example.com"
```

-   `MY_EMAIL`: Vaša e-mailová adresa, z ktorej sa bude posielať upozornenie (napr. Gmail).
-   `MY_PASSWORD`: **Heslo pre aplikáciu**, nie vaše bežné heslo k e-mailu. Z bezpečnostných dôvodov poskytovatelia ako Gmail vyžadujú vygenerovanie jedinečného hesla pre externé aplikácie.
-   `RECIPIENT_EMAIL`: E-mailová adresa, na ktorú má byť upozornenie doručené.

### c) Konfigurácia v súbore `main.py`

Priamo v kóde je potrebné nastaviť dve premenné:

-   `URL`: Vložte sem presnú webovú adresu (URL) produktu na Amazone, ktorý chcete sledovať.
-   `TARGET_PRICE`: Nastavte číselnú hodnotu cieľovej ceny. Ak cena produktu klesne pod túto hodnotu, skript odošle e-mail.

## 3. Štruktúra kódu

Kód je rozdelený do niekoľkých logických častí pre lepšiu prehľadnosť a údržbu.

### a) Importy a načítanie `.env`

```python
import requests
import bs4
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
```

Na začiatku sa importujú všetky potrebné knižnice a okamžite sa zavolá funkcia `load_dotenv()`, ktorá načíta premenné zo súboru `.env` a sprístupní ich v programe.

### b) Konfigurácia

```python
URL = "..."
TARGET_PRICE = 100.0
MY_EMAIL = os.getenv("MY_EMAIL")
# ... atď.
```

V tejto časti sa definujú hlavné premenné – URL produktu, cieľová cena a načítavajú sa e-mailové údaje z premenných prostredia.

### c) Funkcia `get_product_price()`

```python
def get_product_price():
    # ...
```

Táto funkcia je zodpovedná za web scraping.
-   **Výstupy:** Vracia dvojicu hodnôt (`tuple`): `(cena, názov_produktu)`. Ak sa cenu nepodarí získať, vráti `(None, názov_produktu)`.

### d) Funkcia `send_email_alert()`

```python
def send_email_alert(price, product_title):
    # ...
```

Funkcia zodpovedná za odoslanie e-mailového upozornenia.
-   **Vstupy:** `price` (aktuálna cena), `product_title` (názov produktu).

### e) Hlavná logika

```python
if __name__ == "__main__":
    # ...
```

Táto časť sa vykoná iba vtedy, keď je skript spustený priamo. Spojí všetky predchádzajúce kroky do jedného celku.

## 4. Ako spustiť skript

1.  Otvorte terminál alebo príkazový riadok.
2.  Prejdite do priečinka, kde máte uložený projekt.
3.  Spustite skript príkazom:
    ```sh
    python main.py
    ```

Skript vykoná jednu kontrolu a následne sa ukončí. Pre pravidelné monitorovanie by bolo potrebné tento skript spúšťať automaticky v určitých intervaloch (napr. pomocou Cron job na Linuxe/macOS alebo Plánovača úloh vo Windows).
