import requests
from bs4 import BeautifulSoup
from prefect import flow, task
from datetime import datetime
import csv
import re
import time
import random

URL = "https://articulo.mercadolibre.com.mx/MLM-3382859800-tenis-kappa-multitaco-futbol-rapido-kombat-player-tf-negro-_JM"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

@task
def fetch_page(url: str) -> str:
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    html = resp.text

    # Guardar para depuración
    with open("mercadolibre_debug.html", "w", encoding="utf-8") as f:
        f.write(html)

    # Retardo para evitar detección de bot
    time.sleep(random.uniform(2, 5))
    return html

@task
def extract_price(html: str) -> float:
    soup = BeautifulSoup(html, "lxml")
    # Mercado Libre suele usar span con clase "price-tag-fraction" o dentro de "price-tag"
    tag = soup.select_one("span.price-tag-fraction")
    if not tag:
        # alternativa: precio completo
        tag = soup.select_one("div.price-tag > span.price-tag-fraction")
    if not tag:
        # alternativa con meta
        meta = soup.select_one("meta[itemprop='price']")
        if meta and meta.has_attr("content"):
            return float(meta["content"])
        raise ValueError("No se pudo encontrar el precio en la página")

    price_text = tag.get_text(strip=True)
    # price_text suele ser algo como "1,234"
    cleaned = price_text.replace(",", "").strip()
    m = re.search(r"(\d+(\.\d+)?)", cleaned)
    if not m:
        raise ValueError(f"No se pudo interpretar el precio: {price_text}")

    return float(m.group(1))

@task
def save_price(price: float, file: str = "prices_ml.csv"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, price])
    print(f"[{timestamp}] Precio guardado: {price}")

@flow
def ml_price_tracker():
    html = fetch_page(URL)
    price = extract_price(html)
    save_price(price)

if __name__ == "__main__":
    ml_price_tracker()
