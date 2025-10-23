#!/bin/bash
set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         �� COMPREHENSIVE BUILD TEST - START                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Clean
echo "🧹 Step 1: Clean previous build..."
rm -rf llms-os-project
echo "   ✅ Cleaned"
echo ""

# Step 2: Build project from YAML
echo "🏗️  Step 2: Build project from YAML..."
python3 build_project.py > /dev/null 2>&1
if [ -d "llms-os-project" ]; then
    echo "   ✅ Project created"
else
    echo "   ❌ Project creation failed"
    exit 1
fi
echo ""

# Step 3: Build Docker images
echo "🐳 Step 3: Build Docker images..."
cd llms-os-project
docker-compose build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Docker images built successfully"
else
    echo "   ❌ Docker build failed"
    exit 1
fi
echo ""

# Step 4: Start services
echo "🚀 Step 4: Start services..."
docker-compose up -d mock-api > /dev/null 2>&1
sleep 5
if docker ps | grep -q llms-mock-api; then
    echo "   ✅ Mock API running"
else
    echo "   ❌ Mock API failed to start"
    exit 1
fi
echo ""

# Step 5: Test workflow
echo "🎯 Step 5: Run test workflow..."
OUTPUT=$(docker run --rm --network llms-os-project_llms-network \
  -e OPENROUTER_API_URL=http://llms-mock-api:8000/api/v1 \
  -e OPENROUTER_API_KEY=sk-simulated-key \
  -v $(pwd)/workflows:/app/workflows \
  llms-os:latest workflows/test_basic.yaml 2>&1)

if echo "$OUTPUT" | grep -q "✅ Basic test completed successfully"; then
    echo "   ✅ Workflow executed successfully"
else
    echo "   ❌ Workflow execution failed"
    echo "$OUTPUT"
    exit 1
fi
echo ""

# Step 6: Test CLI
echo "🔧 Step 6: Test CLI..."
VERSION=$(docker run --rm llms-os:latest --version 2>&1)
if echo "$VERSION" | grep -q "LLMs_OS v1.0.0"; then
    echo "   ✅ CLI working: $VERSION"
else
    echo "   ❌ CLI test failed"
    exit 1
fi
echo ""

# Step 7: Check images
echo "📦 Step 7: Verify images..."
if docker images | grep -q "llms-os.*latest"; then
    MAIN_SIZE=$(docker images llms-os:latest --format "{{.Size}}")
    API_SIZE=$(docker images llms-os-mock-api:latest --format "{{.Size}}")
    echo "   ✅ llms-os:latest - $MAIN_SIZE"
    echo "   ✅ llms-os-mock-api:latest - $API_SIZE"
else
    echo "   ❌ Images not found"
    exit 1
fi
echo ""

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║         ✅ ALL TESTS PASSED - BUILD IS STABLE                    ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
