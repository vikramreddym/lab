#!/bin/bash

# Define variables
ACCOUNT_ID=99999
REGION=us-east-2
REGISTRY_NAME=mlzoomcamp-images
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com

aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${PREFIX}

# Gateway image
GATEWAY_REMOTE=${PREFIX}/${REGISTRY_NAME}:zoomcamp-10-gateway-001

# Tag Gateway image
docker push ${GATEWAY_REMOTE}

# Model image
MODEL_REMOTE=${PREFIX}/${REGISTRY_NAME}:zoomcamp-10-model-xception-v4-001

# Tag Model image
docker push ${MODEL_REMOTE}

# Optional: Print results
echo "Pushed images"
