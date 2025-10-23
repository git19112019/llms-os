#!/bin/bash
# Quick workflow runner script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if mock API is running
if ! docker ps | grep -q llms-mock-api; then
    echo -e "${BLUE}🚀 Starting Mock API...${NC}"
    docker-compose up -d mock-api
    echo -e "${GREEN}✅ Mock API started${NC}"
    sleep 3
fi

# Get workflow file
WORKFLOW=${1:-workflows/test_basic.yaml}

echo -e "${BLUE}📝 Running workflow: ${WORKFLOW}${NC}"
echo ""

# Run workflow
docker run --rm \
  --network llms-os-project_llms-network \
  -e OPENROUTER_API_URL=http://llms-mock-api:8000/api/v1 \
  -e OPENROUTER_API_KEY=sk-simulated-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest ${WORKFLOW}

echo ""
echo -e "${GREEN}✅ Workflow completed!${NC}"
