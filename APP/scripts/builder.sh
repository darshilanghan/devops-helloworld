#!/bin/bash
set -e

IMAGE=${IMAGE:-helloworld}
REPO=${REPO:-darshil}
TAG=${TAG:-v1.0}
APP_PATH=${APP_PATH:-.}
PUSH=${PUSH:-true}

FULL_IMAGE=$REPO/$IMAGE:$TAG

echo "Checking if image exists on DockerHub..."
if docker manifest inspect $FULL_IMAGE > /dev/null 2>&1; then
  echo "Image already exists. Exiting."
  exit 0
else
  echo "Image not found. Building new image."
fi

echo "Building Docker image..."
docker build -t $FULL_IMAGE $APP_PATH


echo "Checking Redis container..."
if [ "$(docker ps -q -f name=redis)" ]; then
  echo "Redis already running"
else
  echo "Starting Redis..."
  docker run -d -p 6379:6379 --name redis redis || docker start redis
fi

echo "Checking MongoDB container..."
if [ "$(docker ps -q -f name=mongodb)" ]; then
  echo "MongoDB already running"
else
  echo "Starting MongoDB..."
  docker run -d -p 27017:27017 --name mongodb mongo || docker start mongodb
fi


echo "Running container for validation..."
docker rm -f test_container >/dev/null 2>&1 || true
docker run -d -p 5005:5005 --name test_container $FULL_IMAGE

sleep 5

curl -f http://localhost:5005/health || (echo "Health check failed" && docker logs test_container && exit 1)

docker rm -f test_container

if [ "$PUSH" = "true" ]; then
  echo "Logging into Docker Hub..."
  echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

  echo "Pushing image..."
  docker push $FULL_IMAGE

  echo "Docker image pushed successfully"
else
  echo "Push skipped (Pull Request build)"
fi

echo "Build process complete"