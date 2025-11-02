from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

search = input("What do you want to search on Amazon? ")
# ✅ Setup Chrome driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # keeps Chrome open
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ Open Amazon
driver.get("https://www.amazon.in")
driver.maximize_window()

# ✅ Wait for search box and search for "doormats"
wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
search_box.send_keys(search)
search_box.send_keys(Keys.RETURN)

# ✅ Wait until results load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))

# ✅ Get all price elements
price_elements = driver.find_elements(By.CSS_SELECTOR, "span.a-price-whole")

# ✅ Process prices and track the lowest one
lowest_price = float('inf')   # start with infinity
price_list = []

for p in price_elements:
    price_text = p.text.replace(",", "").strip()
    if price_text.isdigit():  # ensure valid numeric value
        current_price = int(price_text)
        price_list.append(current_price)

        # check if it's lower than the earlier one
        if current_price < lowest_price:
            lowest_price = current_price

# ✅ Print results
print("\nAll prices found:", price_list)
print(f"\n💰 Lowest price found: ₹{lowest_price}")

# Keep browser open
input("\nPress Enter to close browser...")
driver.quit()
