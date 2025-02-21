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
        chrome_options.add_argument('--no-sandbox')  # Often needed in containers
        chrome_options.add_argument('--disable-dev-shm-usage') # Often needed in containers
        webdriver_service = Service(webdriver_path) # Or just "chromedriver" if it's in your PATH
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        
        # 2. Load the webpage
        driver.get(url)

        try:
            elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "matchup-card__inner"))
            WebDriverWait(driver, 20).until(elements_present)  # Wait up to 10 seconds
        except Exception as e:
            print(f"Error waiting for elements: {e}")
            return None # Or handle the error as you see fit
        div = driver.find_elements(By.CLASS_NAME, div_selector)
    
        div_content = getcards(div)
        all_round = {"Round 1": div_content}

        try:
            elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "round"))
            WebDriverWait(driver, 20).until(elements_present)  # Wait up to 10 seconds
        except Exception as e:
            print(f"Error waiting for elements: {e}")
            return None # Or handle the error as you see fit
        buttons = driver.find_elements(By.CLASS_NAME, "round")

        round_counter = 1
        for button in buttons:
            round_counter += 1
            # button_present = EC.element_to_be_clickable((By.CLASS_NAME, "round"))
            # WebDriverWait(driver, 20).until(button_present)
            button.click()

            try:
                elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, div_selector))
                WebDriverWait(driver, 20).until(elements_present)  # Wait up to 10 seconds
            except Exception as e:
                print(f"Error waiting for elements: {e}")
                return None # Or handle the error as you see fit
            div = driver.find_elements(By.CLASS_NAME, div_selector)
            div_content = getcards(div)
            all_round.update({"Round "+str(round_counter): div_content})
            # time.sleep(10)
            
        return all_round

    finally:
        if 'driver' in locals(): # Check if driver was initialized
            driver.quit()  # Close the browser

def getcards(div):
    div_content = []
    for card in div:
        cards = card.text
        parts = cards.split('\n')
        match_data = {
            "match": parts[0],
            "player1": parts[1],
            "player1_id": parts[2],
            "player1_score": int(parts[3]),
            "player2": parts[4],
            "player2_id": parts[5],
            "player2_score": int(parts[6])
        }
        div_content.append(match_data)
    return div_content