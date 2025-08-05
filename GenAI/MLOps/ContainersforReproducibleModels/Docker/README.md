# Load the image from the tar file
docker load < test-model.tar.gz

# Run it on your computer
docker run -d -p 5000:5000 --name my-local-app test-model:latest

# Test it
curl http://localhost:5000/health
# Or open http://localhost:5000 in your browser