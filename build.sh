#!/usr/bin/env bash

set -e
set -o pipefail

if [ -n "$CUSTOM_DNS" ]; then
  echo "Using custom dns server: $CUSTOM_DNS"
  cat <<EOF > /etc/resolv.conf
nameserver $CUSTOM_DNS
options timeout:2 attempts:3 rotate single-request-reopen ndots:0
EOF
fi

TAG=$(echo "$DRONE_TAG" | tr -d 'v')
echo "Building on $TAG..."
docker buildx create --name multi-arch-builder --use --bootstrap --driver-opt env.http_proxy="$HTTP_PROXY" --driver-opt env.https_proxy="$HTTPS_PROXY" --driver-opt '"env.no_proxy='$NO_PROXY'"'
echo "$DOCKER_REGISTRY_PASSWORD" | docker login -u "$DOCKER_REGISTRY_USER" --password-stdin
docker buildx build -t yusiwen/app-monitor:"$TAG" --platform linux/amd64,linux/arm64 --push -f Dockerfile-pipeline .
