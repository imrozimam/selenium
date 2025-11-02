from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Configure headless Chrome once ---
def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

# --- Function to search a topic and save results ---
def scrape_wikipedia(topic):
    driver = get_driver()
    try:
        driver.get("https://www.wikipedia.org/")
        search_box = driver.find_element(By.ID, "searchInput")
        search_box.send_keys(topic)
        search_box.submit()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "firstHeading"))
        )

        paragraphs = driver.find_elements(By.CSS_SELECTOR, "div.mw-parser-output > p")
        data = "\n\n".join([p.text for p in paragraphs if p.text.strip()][:3])

        file_name = f"{topic.lower().replace(' ', '_')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(data)

        return f"✅ {topic}: Saved to '{file_name}'"

    except Exception as e:
        return f"❌ {topic}: Error - {e}"

    finally:
        driver.quit()

# --- Topics to search (you can modify this list) ---
topics = ["Apple", "Banana", "Python programming", "Artificial Intelligence", "Tesla"]

# --- Run parallel scraping ---
print("Starting parallel Wikipedia searches...\n")

results = []
with ThreadPoolExecutor(max_workers=3) as executor:  # run 3 at once
    futures = {executor.submit(scrape_wikipedia, topic): topic for topic in topics}
    for future in as_completed(futures):
        results.append(future.result())

print("\n--- Summary ---")
for result in results:
    print(result)
