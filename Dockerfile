# # Container image that runs your code
# FROM alpine:3.10

# # Copies your code file from your action repository to the filesystem path `/` of the container
# COPY entrypoint.sh /entrypoint.sh

# # Code file to execute when the docker container starts up (`entrypoint.sh`)
# ENTRYPOINT ["/entrypoint.sh"]
ARG CHROMEDRIVER_PATH="chromedriver"
FROM python:3.12.5-alpine3.19
COPY source/requirements.txt .
RUN pip install -r requirements.txt
COPY source .
COPY ${CHROMEDRIVER_PATH} .
CMD ["python", "app.py"]
