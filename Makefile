.PHONY: install dev prod clean test health logs

# Default target
help:
	@echo "🎨 Interactive Particle System - Production Commands"
	@echo "================================================="
	@echo "Available commands:"
	@echo "  install    - Install all dependencies"
	@echo "  dev        - Start development server"
	@echo "  prod       - Start production server"
	@echo "  health     - Check application health"
	@echo "  test       - Run application tests"
	@echo "  clean      - Clean temporary files"
	@echo "  logs       - View application logs"

# Install dependencies
install:
	@echo "Installing dependencies..."
	@uv sync

# Development server
dev:
	@echo "Starting development server..."
	@FLASK_ENV=development python start.py

# Production server  
prod:
	@echo "Starting production server..."
	@FLASK_ENV=production python start.py

# Health check
health:
	@echo "Checking application health..."
	@curl -s http://localhost:5000/health | python -m json.tool || echo "Server not responding"
	@echo ""
	@curl -s http://localhost:5000/ready | python -m json.tool || echo "Server not ready"

# Test the application
test:
	@echo "Running application tests..."
	@python -c "from app import app, db; print('✅ App imports successfully')"
	@python -c "from config import get_config; print('✅ Config loads successfully')"
	@echo "✅ All basic tests passed"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -delete 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@rm -rf logs/*.log.* 2>/dev/null || true
	@echo "✅ Cleanup complete"

# View logs
logs:
	@echo "Recent application logs:"
	@echo "======================"
	@if [ -f logs/particle_system.log ]; then tail -20 logs/particle_system.log; else echo "No application logs found"; fi