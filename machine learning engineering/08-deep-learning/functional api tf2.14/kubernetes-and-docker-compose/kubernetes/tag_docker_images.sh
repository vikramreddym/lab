#!/bin/bash

# Define variables
ACCOUNT_ID=99999
REGION=us-east-2
REGISTRY_NAME=mlzoomcamp-images
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}

# Gateway image
GATEWAY_LOCAL=zoomcamp-10-gateway:001
GATEWAY_REMOTE=${PREFIX}:zoomcamp-10-gateway-001

# Tag Gateway image
docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}

# Model image
MODEL_LOCAL=zoomcamp-10-model:xception-v4-001
MODEL_REMOTE=${PREFIX}:zoomcamp-10-model-xception-v4-001

# Tag Model image
docker tag ${MODEL_LOCAL} ${MODEL_REMOTE}

# Optional: Print results
echo "Tagged images:"
echo "  ${GATEWAY_LOCAL} -> ${GATEWAY_REMOTE}"
echo "  ${MODEL_LOCAL} -> ${MODEL_REMOTE}"
