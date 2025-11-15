import requests
import bs4
import smtplib
import os
from dotenv import load_dotenv

# Načítanie premenných prostredia zo súboru .env
load_dotenv()

# --- Konfigurácia ---
# URL adresa produktu na Amazone, ktorého cenu chcete sledovať
# DÔLEŽITÉ: Nahraďte túto URL adresou skutočného produktu!
URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# Cieľová cena v EUR. Ak cena klesne pod túto hodnotu, pošle sa e-mail.
TARGET_PRICE = 100.0

# Načítanie údajov pre odoslanie e-mailu zo súboru .env
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# --- Získanie ceny produktu ---

def get_product_price():
    """
    Funkcia na získanie ceny produktu z Amazonu.
    Vráti cenu ako float, alebo None, ak sa cenu nepodarí získať.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,sk;q=0.8"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Skontroluje, či požiadavka prebehla úspešne

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # Nájdenie ceny - toto sa môže líšiť v závislosti od produktu a krajiny Amazonu
        price_whole = soup.find(class_="a-price-whole")
        price_fraction = soup.find(class_="a-price-fraction")
        
        # Pokus o nájdenie názvu produktu
        product_title_element = soup.find(id="productTitle")
        product_title = product_title_element.getText().strip() if product_title_element else "Neznámy produkt"


        if price_whole and price_fraction:
            price_text = f"{price_whole.getText().strip()}{price_fraction.getText().strip()}"
            return float(price_text), product_title
        else:
            print("Nepodarilo sa nájsť cenu na stránke. Skontrolujte HTML štruktúru.")
            return None, product_title

    except requests.exceptions.RequestException as e:
        print(f"Chyba pri sťahovaní stránky: {e}")
        return None, "Neznámy produkt"
    except (AttributeError, ValueError) as e:
        print(f"Chyba pri spracovaní ceny: {e}")
        return None, "Neznámy produkt"

# --- Posielanie e-mailu ---

def send_email_alert(price, product_title):
    """
    Odošle e-mailové upozornenie o nízkej cene.
    """
    message = f"Subject:Amazon Price Alert!\n\nCena pre produkt '{product_title}' klesla na {price} EUR!\n\nLink na produkt:\n{URL}".encode('utf-8')

    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=RECIPIENT_EMAIL,
                msg=message
            )
        print("E-mailové upozornenie úspešne odoslané!")
    except Exception as e:
        print(f"Chyba pri odosielaní e-mailu: {e}")


# --- Hlavná logika ---

if __name__ == "__main__":
    # Overenie, či sú načítané všetky potrebné premenné prostredia
    if not all([MY_EMAIL, MY_PASSWORD, RECIPIENT_EMAIL]):
        print("Chyba: Nie sú nastavené všetky potrebné premenné prostredia v .env súbore (MY_EMAIL, MY_PASSWORD, RECIPIENT_EMAIL).")
    else:
        current_price, product_name = get_product_price()

        if current_price is not None:
            print(f"Aktuálna cena produktu '{product_name}' je: {current_price} EUR")
            
            if current_price < TARGET_PRICE:
                print("Cena je nižšia ako cieľová. Posielam e-mail...")
                send_email_alert(current_price, product_name)
            else:
                print("Cena je stále vyššia ako cieľová. E-mail sa neposiela.")
