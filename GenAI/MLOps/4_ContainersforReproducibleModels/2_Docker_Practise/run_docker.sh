# Build the image with a tag name
docker build -t ml-api:1.0.0 .

docker run -p 5000:5000 ml-api:1.0.0