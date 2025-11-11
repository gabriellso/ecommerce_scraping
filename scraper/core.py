from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import logging
import time

from scraper.utils import retry, random_user_agent
from scraper.sites import parse_amazon, parse_mercadolivre

OUTPUT_FILE = 'results_produtos.csv'

def init_driver():
    options = Options()
    options.add_argument(f"user-agent={random_user_agent()}")
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    return driver

@retry(max_retries=3)
def scrape_product(url, driver, max_title_length=80):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    if "mercadolivre.com.br" in url:
        parsed = parse_mercadolivre(soup, max_title_length)
    elif "amazon.com.br" in url:
        parsed = parse_amazon(soup, max_title_length)
    else:
        logging.warning(f"Site não reconhecido: {url}")
        return None

    return {
        "name": parsed["name"],
        "price": parsed["price"],
        "url": url
    }

def main():
    try:
        urls_df = pd.read_csv("urls.csv")
        urls = urls_df["url"].dropna().tolist()
    except FileNotFoundError:
        logging.error("Arquivo 'urls.csv' não encontrado!")
        return
    except KeyError:
        logging.error("O CSV precisa ter uma coluna chamada 'url'.")
        return

    driver = init_driver()
    data = []

    for url in urls:
        logging.info(f"Scraping {url}...")
        result = scrape_product(url, driver)
        if result:
            data.append(result)

    driver.quit()

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"\n✅ Dados salvos em '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
