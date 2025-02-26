To be populated

Curl in Windows Powershell (Invoke-WebRequest):
- curl http://<svc_ip/domain>/scrape -ContentType "application/json" -Body '{"event_id":"yi98m"}' -Method POST -OutFile test.

Curl in Linux
- curl http://<svc_ip/domain>/scrape -H "Content-Type: application/json" -d '{"event_id":"yi98m"}'

Docker Image
- black0803/flask-tonamel-scraper-server
- black0803/tonamel-scraper

API:
- GET / : homepage scrape
- POST / : scrape from homepage form
- POST /scrape : scrape using POST data json
- GET /query-event?event_id= : query from get
- POST /query-event : query from POST data json