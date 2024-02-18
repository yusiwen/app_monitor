#!/usr/bin/env bash

set -e
set -o pipefail

TAG=$(echo $DRONE_TAG | tr -d 'v')
echo "Building on $TAG..."
docker buildx create --name multi-arch-builder --use --bootstrap
echo "$DOCKER_REGISTRY_PASSWORD" | docker login -u $DOCKER_REGISTRY_USER --password-stdin
docker buildx build -t yusiwen/app-monitor:$TAG --platform linux/amd64,linux/arm64 --push -f Dockerfile-pipeline .
