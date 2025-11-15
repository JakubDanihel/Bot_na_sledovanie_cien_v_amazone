import requests
import bs4
import smtplib
import os
from dotenv import load_dotenv

# ziskanie premennych z zuboru .env kde su ulozene prihlasovacie udaje (pre tento pripad bol pouzity gmail)
load_dotenv()

# Konfiguracia
# URL adresa produktu na Amazone, ktoreho cenu chceme sledovat
# JE POTREBNE NAHRAT SKUTOCNU ADRESU PRODUKTU
URL = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# Cielova cena produktu pre ktoru sa spusti oznam ak cena poklesne nizsie
TARGET_PRICE = 100.0

# Nacitanie udajov z .env ako premenne prostredia (v ramci bezpecnosti sa to neuklada do suboru
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

# ziskanie ceny produktu

def get_product_price():
    # Funkcia na ziskanie ceny. Cenu vrati ako float alebo none ak nie je

    #nastavenie headers aby amazon nevypol aplikaciu
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,sk;q=0.8"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()  # Skontroluje, či požiadavka prebehla úspešne

        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # Hladanie ceny (moze toto miesto byt ine ak sa jedna o iny produkt alebo krajinu amazonu)
        price_whole = soup.find(class_="a-price-whole")
        price_fraction = soup.find(class_="a-price-fraction")
        
        # Pokus o najdenie projektu
        product_title_element = soup.find(id="productTitle")
        product_title = product_title_element.getText().strip() if product_title_element else "Neznamy produkt"


        if price_whole and price_fraction:
            price_text = f"{price_whole.getText().strip()}{price_fraction.getText().strip()}"
            return float(price_text), product_title
        else:
            print("Nepodarilo sa najst cenu. Skontroluj strukturo HTML.")
            return None, product_title

    except requests.exceptions.RequestException as e:
        print(f"Chyba pri stahovani stranky: {e}")
        return None, "Neznamy produkt"
    except (AttributeError, ValueError) as e:
        print(f"Chyba pri spracovaní ceny: {e}")
        return None, "Neznamy produkt"

# Odoslanie mailu s varovanim

def send_email_alert(price, product_title):

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
        print("Poslane uspesne")
    except Exception as e:
        print(f"Chyba pri odosielaní e-mailu: {e}")


# MAIN

if __name__ == "__main__":
    # Overenie ci su vsetky hodnoty nacitane (premenne prostredia)
    if not all([MY_EMAIL, MY_PASSWORD, RECIPIENT_EMAIL]):
        print("Chyba: Nie su nastavene vsetky hodnoty v prostredi v .env súbore (MY_EMAIL, MY_PASSWORD, RECIPIENT_EMAIL).")
    else:
        current_price, product_name = get_product_price()

        if current_price is not None:
            print(f"Aktualna cena produktu '{product_name}' je: {current_price} EUR")
            
            if current_price < TARGET_PRICE:
                print("Cena je nizsia ako hranica. Posielam e-mail...")
                send_email_alert(current_price, product_name)
            else:
                print("Cena je vysia ako hranica. E-mail sa neposiela.")
