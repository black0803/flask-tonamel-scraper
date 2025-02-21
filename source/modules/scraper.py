from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # For Chrome
#from selenium.webdriver.firefox.service import Service # For Firefox
import time

def scrape_with_selenium(url, div_selector, webdriver_path):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no browser window) - optional
        webdriver_service = Service(webdriver_path) # Or just "chromedriver" if it's in your PATH
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        
        # 2. Load the webpage
        driver.get(url)

        # 3. Wait for the specific div to load (important!)
        # Adjust the timeout as needed
        try:
            button_present = EC.element_to_be_clickable((By.CLASS_NAME, "round"))
            WebDriverWait(driver, 20).until(button_present)
        except Exception as e:
            print(f"Error waiting for element: {e}")
            return None # Or handle the error as you see fit

        
        time.sleep(10)
        buttons = driver.find_elements(By.CLASS_NAME, "round")
        
        # 4. Extract the content of the div
        div = driver.find_elements(By.CLASS_NAME, div_selector)
        div_content = getcards(div)
        all_round = {"Round 1": div_content}
        
        round_counter = 1
        for button in buttons:
            round_counter += 1
            button.click()
            time.sleep(10)
            div = driver.find_elements(By.CLASS_NAME, div_selector)
            div_content = getcards(div)
            all_round.update({"Round "+str(round_counter): div_content})
            
        return all_round

    finally:
        if 'driver' in locals(): # Check if driver was initialized
            driver.quit()  # Close the browser

def getcards(div):
    div_content = []
    for card in div:
        text_content = card.text
        div_content.append(text_content)
    return div_content