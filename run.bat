docker run -d --name textsum_endpoint -p 8000:8000 textsum_endpoint
cd frontend\textsum
docker-compose -f docker-compose.dev.yml up -d
cd ..
cd ..