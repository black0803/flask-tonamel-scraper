
## License

This project uses dual licensing:

* The core application (in the `flask-server/` and `tonamel-scraper/` directories) is licensed under the MIT License. See `flask-server/LICENSE-MIT` or `tonamel-scraper/LICENSE-MIT` for details. This application is primarily designed to work with AWS DynamoDB.
* For users aiming for a cloud-agnostic approach, or for local development, the Sample Deployment folder (in the `sample-deployment/` directory) and the `docker-compose.yml` file provide an optional ScyllaDB setup. This setup is licensed under the GNU Affero General Public License v3.0 (AGPLv3). See `sample-deployment/LICENSE-AGPL` and the folder containing the `docker-compose.yml` file for details. This ScyllaDB setup is not enforced and is dependent on the user's choice.
* If this application is deployed as a network service using ScyllaDB, the AGPLv3 license will apply to the entire application (Please define the `USE_SCYLLA` variable as `True` in the environment variable if you use ScyllaDB).
* The `docker-compose.yml` file is provided for local development and cloud-agnostic testing, allowing users to experiment with ScyllaDB without a production setup. It is best not be used in a production environment.

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