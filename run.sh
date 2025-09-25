#!/bin/bash

# Interactive Particle System - Self-Executable Production Runner
# This script provides a complete self-contained way to run the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}"
echo "🎨 Interactive Particle System"
echo "=============================="
echo -e "${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if virtual environment exists or create one
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/installed" ]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r <(echo "
email-validator>=2.2.0
flask>=3.1.0
flask-sqlalchemy>=3.1.1
flask-wtf>=1.2.2
gunicorn>=23.0.0
psycopg2-binary>=2.9.10
sqlalchemy>=2.0.39
")
    touch .venv/installed
fi

# Set environment variables with defaults
export FLASK_ENV=${FLASK_ENV:-production}
export SESSION_SECRET=${SESSION_SECRET:-$(python3 -c "import secrets; print(secrets.token_hex(32))")}

# Check for database URL
if [ -z "$DATABASE_URL" ]; then
    echo -e "${YELLOW}⚠️  DATABASE_URL not set, using SQLite fallback${NC}"
    export DATABASE_URL="sqlite:///particle_system.db"
fi

echo -e "${GREEN}✅ Environment ready${NC}"
echo -e "${BLUE}🚀 Starting Interactive Particle System...${NC}"
echo -e "${BLUE}📍 Access your application at: http://localhost:5000${NC}"
echo ""

# Start the application
if [ "$FLASK_ENV" = "development" ]; then
    echo -e "${YELLOW}🔧 Running in development mode${NC}"
    python main.py
else
    echo -e "${GREEN}🏭 Running in production mode${NC}"
    if [ -f "gunicorn.conf.py" ]; then
        gunicorn --config gunicorn.conf.py main:app
    else
        gunicorn --bind 0.0.0.0:5000 --workers 4 main:app
    fi
fi