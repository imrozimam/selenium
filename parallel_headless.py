from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_driver():
    """Create a new headless Chrome driver."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)

def scrape_wikipedia(topic):
    """Scrape about 500 words of content for a given topic."""
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

        # Join a larger number of non-empty paragraphs (10–15)
        text_blocks = [p.text.strip() for p in paragraphs if p.text.strip()]
        long_text = " ".join(text_blocks[:12])  # combine ~500 words

        # Optional: truncate or pad near 500 words
        words = long_text.split()
        if len(words) > 500:
            long_text = " ".join(words[:500])

        file_name = f"{topic.lower().replace(' ', '_')}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(long_text)

        return f"✅ {topic}: Saved to '{file_name}' ({len(words)} words)"

    except Exception as e:
        return f"❌ {topic}: Error - {e}"

    finally:
        driver.quit()

# --- Topics to scrape ---
topics = ["Apple", "Banana", "Python programming", "Artificial Intelligence", "Tesla"]

print("Starting parallel Wikipedia data collection...\n")

results = []
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(scrape_wikipedia, topic): topic for topic in topics}
    for future in as_completed(futures):
        results.append(future.result())

print("\n--- Summary ---")
for result in results:
    print(result)
