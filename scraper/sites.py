from bs4 import BeautifulSoup

def parse_mercadolivre(soup, max_title_length=80):
    name_el = soup.select_one("h1.ui-pdp-title")
    name = name_el.get_text(strip=True) if name_el else ""
    name = name.split(",")[0].strip()
    if len(name) > max_title_length:
        name = name[:max_title_length] + "…"

    price_container = soup.select_one("div.ui-pdp-price__second-line")
    price_float = 0.0

    if price_container:
        price_fraction_el = price_container.select_one("span.andes-money-amount__fraction")
        price_cents_el = price_container.select_one("span.andes-money-amount__cents")

        price_fraction = price_fraction_el.get_text(strip=True) if price_fraction_el else "0"
        price_cents = price_cents_el.get_text(strip=True) if price_cents_el else "00"

        price_fraction = price_fraction.replace(".", "")
        price_cents = price_cents.zfill(2)

        try:
            price_float = float(f"{price_fraction}.{price_cents}")
        except:
            price_float = 0.0

    return {"name": name, "price": price_float}

def parse_amazon(soup, max_title_length=80):
    name_el = soup.select_one("#productTitle")
    name = name_el.get_text(strip=True) if name_el else ""
    name = name.split("-")[0].strip()
    if len(name) > max_title_length:
        name = name[:max_title_length] + "…"

    price_whole_el = soup.select_one(".a-price-whole")
    price_fraction_el = soup.select_one(".a-price-fraction")

    price_float = 0.0
    if price_whole_el and price_fraction_el:
        price_whole = ''.join(filter(str.isdigit, price_whole_el.get_text(strip=True)))
        price_cents = ''.join(filter(str.isdigit, price_fraction_el.get_text(strip=True))).zfill(2)
        try:
            price_float = float(f"{price_whole}.{price_cents}")
        except:
            price_float = 0.0

    return {"name": name, "price": price_float}