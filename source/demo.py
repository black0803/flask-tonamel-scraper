import modules.scraper
data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/YaSgI/tournament", "matchup-card__inner", "chromedriver.exe")
print(data)