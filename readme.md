To be populated

Curl in Windows Powershell (Invoke-WebRequest):
- curl http://<svc_ip/domain>/scrape -ContentType "application/json" -Body '{"event_id":"yi98m"}' -Method POST -OutFile test.

Curl in Linux
- curl http://<svc_ip/domain>/scrape -H "Content-Type: application/json" -d '{"event_id":"yi98m"}'