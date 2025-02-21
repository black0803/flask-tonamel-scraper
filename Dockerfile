# # Container image that runs your code
# FROM alpine:3.10

# # Copies your code file from your action repository to the filesystem path `/` of the container
# COPY entrypoint.sh /entrypoint.sh

# # Code file to execute when the docker container starts up (`entrypoint.sh`)
# ENTRYPOINT ["/entrypoint.sh"]
FROM python:3.12.5-alpine3.19
RUN apk add --no-cache chromium chromium-chromedriver
COPY source/requirements.txt .
RUN pip install -r requirements.txt
COPY source .
CMD ["python", "app.py"]
