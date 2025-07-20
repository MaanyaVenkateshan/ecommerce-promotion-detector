from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


CHROME_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
if not os.path.isfile(CHROME_PATH):
    raise FileNotFoundError(f"chromedriver.exe not found at {CHROME_PATH}")


options = Options()

options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(CHROME_PATH)
driver = webdriver.Chrome(service=service, options=options)


sites = [
    {"name": "flipkart", "url": "https://www.flipkart.com/"},
    {"name": "amazon", "url": "https://www.amazon.in/"},
    {"name": "walmart", "url": "https://www.walmart.com/"}
]

records = []

for site in sites:
    print(f"🔍 Scraping {site['name']}...")
    driver.get(site['url'])
    time.sleep(5)

    if site['name'] == "flipkart":
        try:
            driver.find_element("xpath", "//button[contains(text(),'✕')]").click()
        except Exception:
            pass

    
    for _ in range(100):  
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

   
    for tag in soup.find_all(["h1", "h2", "h3", "p", "span", "a", "button"]):
        text = tag.get_text(strip=True)
        if text and len(text) > 5:
            records.append({"website": site['name'], "text": text, "image_url": None})

    
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src and src.startswith("http"):
            records.append({"website": site['name'], "text": None, "image_url": src})

driver.quit()


df = pd.DataFrame(records)


csv_path = "ecommerce_scraped_data.csv"


if os.path.exists(csv_path):
    df.to_csv(csv_path, mode='a', header=False, index=False)
else:
    df.to_csv(csv_path, index=False)

print(" Done! Saved ecommerce_scraped_data.csv")
