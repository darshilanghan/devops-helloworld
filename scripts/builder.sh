# #!/bin/bash

set -e

IMAGE=${IMAGE:-helloworld}
REPO=${REPO:-darshil}
TAG=${TAG:-v1.0}
APP_PATH=${APP_PATH:-../app}
PUSH=${PUSH:-true}

FULL_IMAGE=$REPO/$IMAGE:$TAG
NETWORK=test_network

echo "Checking if image exists on DockerHub..."

if docker manifest inspect $FULL_IMAGE > /dev/null 2>&1; then
  echo "Image already exists. Exiting."
  exit 0
else
  echo "Image not found. Building new image."
fi

echo "Building Docker image..."

docker build -t $FULL_IMAGE $APP_PATH

echo "Cleaning old containers..."

docker rm -f test_container redis mongo 2>/dev/null || true
docker network rm $NETWORK 2>/dev/null || true

echo "Creating docker network..."

docker network create $NETWORK

echo "Starting Redis container..."

docker run -d \
  --name redis \
  --network $NETWORK \
  redis:7

echo "Starting MongoDB container..."

docker run -d \
  --name mongo \
  --network $NETWORK \
  mongo:7

echo "Starting Flask application..."

docker run -d \
  -p 5000:5000 \
  --name test_container \
  --network $NETWORK \
  -e REDIS_HOST=redis \
  -e REDIS_PORT=6379 \
  -e MONGO_URI=mongodb://mongo:27017 \
  $FULL_IMAGE


echo "Waiting for container to start..."

sleep 8

echo "Validating application..."

curl -f http://localhost:5000/health

echo "Application is healthy"

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

