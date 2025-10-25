#!/bin/bash

# Start infrastructure services
echo "Starting infrastructure services..."
docker-compose -f infra/docker-compose.yml up -d

echo "Waiting for services to be ready..."
sleep 5

echo "Services started:"
echo "- PostgreSQL: localhost:5432"
echo "- Redis: localhost:6379"
echo "- MinIO: http://localhost:9000"
echo "- MinIO Console: http://localhost:9001"
echo "- Adminer: http://localhost:8080"

echo ""
echo "To stop services, run: docker-compose -f infra/docker-compose.yml down"
