#!/bin/bash

# docker compose build
gcloud auth configure-docker asia-southeast1-docker.pkg.dev
docker tag repetit-be:latest asia-southeast1-docker.pkg.dev/repetit-app/repetit-be/repetit-be:latest
docker push asia-southeast1-docker.pkg.dev/repetit-app/repetit-be/repetit-be:latest