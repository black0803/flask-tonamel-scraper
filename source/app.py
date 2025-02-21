import modules.scraper
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import os

load_dotenv()
app = Flask(__name__)

@app.get("/")
def root_path():
    return render_template("index.html")

@app.post("/")
def root_submit():
    data = request.form['event_id']
    div_selector = "matchup-card__inner"  # Replace with the CSS selector of the div
    data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/"+data+"/tournament", div_selector, os.getenv("CHROMEDRIVER","chromedriver"))
    if data:
        return data
    else:
        return jsonify({
            "output": "unexpected payload"
        })

@app.post("/scrape")
def scrape():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        div_selector = "matchup-card__inner"  # Replace with the CSS selector of the div
        try:
            data = modules.scraper.scrape_with_selenium("https://tonamel.com/competition/"+data.get('event_id')+"/tournament", div_selector, "chromedriver.exe")
        except:
            data = False
        
        if data:
            return data
        else:
            return jsonify({
                "output": "unexpected payload"
            })

    else:
        return jsonify({
            "output": "unexpected payload"
        })


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

    # if scraped_data:
    #     print(scraped_data)
    # else:
    #     print("Scraping failed.")