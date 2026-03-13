#!/bin/bash

set -e

IMAGE=${IMAGE:-helloworld}
REPO=${REPO:-darshil}
TAG=${TAG:-v1.0}
APP_PATH=${APP_PATH:-../app}
PUSH=${PUSH:-true}

FULL_IMAGE=$REPO/$IMAGE:$TAG

echo "Checking if image exists on DockerHub..."

docker manifest inspect $FULL_IMAGE > /dev/null 2>&1

if [ $? -eq 0 ]; then
  echo "Image already exists. Exiting."
  exit 0
fi

echo "Building Docker image..."

docker build -t $FULL_IMAGE $APP_PATH

echo "Running container for validation..."

docker run -d -p 5000:5000 --name test_container $FULL_IMAGE

sleep 5

curl -f http://localhost:5000/health

if [ $? -ne 0 ]; then
   echo "Validation failed"
   docker rm -f test_container
   exit 1
fi

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
