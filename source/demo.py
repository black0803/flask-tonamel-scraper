import modules.scraper
import os
from dotenv import load_dotenv

load_dotenv()
data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/YaSgI/tournament", "matchup-card__inner", os.getenv("CHROMEDRIVER","/usr/bin/chromedriver"))
print(data)