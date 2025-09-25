#!/usr/bin/env python3
"""
Self-executable startup script for Interactive Particle System.
This script can be run directly to start the production server.
"""
import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check and set up required environment variables with fallbacks."""
    # Set DATABASE_URL fallback to SQLite if not provided
    if not os.environ.get('DATABASE_URL'):
        sqlite_path = Path.cwd() / 'particle_system.db'
        os.environ['DATABASE_URL'] = f'sqlite:///{sqlite_path}'
        logger.info(f"DATABASE_URL not set, using SQLite fallback: {sqlite_path}")
    
    # Set SESSION_SECRET fallback if not provided
    if not os.environ.get('SESSION_SECRET'):
        import secrets
        os.environ['SESSION_SECRET'] = secrets.token_hex(32)
        logger.info("SESSION_SECRET not set, generated temporary secret")
        logger.warning("For production, set a permanent SESSION_SECRET environment variable")
    
    logger.info("Environment variables configured successfully")
    return True

def check_database():
    """Check database connectivity."""
    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            db.session.execute(db.text('SELECT 1'))
        logger.info("Database connection successful")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Will attempt to create database tables on startup")
        return False

def start_production_server():
    """Start the production server with optimized settings."""
    logger.info("Starting Interactive Particle System in production mode...")
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    
    # Check if gunicorn config exists
    config_file = Path('gunicorn.conf.py')
    
    if config_file.exists():
        cmd = [
            'gunicorn',
            '--config', 'gunicorn.conf.py',
            'main:app'
        ]
    else:
        # Fallback to basic gunicorn command
        workers = max(1, (os.cpu_count() or 1) * 2 + 1)
        cmd = [
            'gunicorn',
            '--bind', '0.0.0.0:5000',
            '--workers', str(workers),
            '--worker-class', 'gthread',
            '--threads', '2',
            '--timeout', '30',
            '--keepalive', '2',
            '--max-requests', '1000',
            '--max-requests-jitter', '100',
            '--preload',
            'main:app'
        ]
    
    logger.info(f"Starting server with command: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)

def start_development_server():
    """Start the development server."""
    logger.info("Starting Interactive Particle System in development mode...")
    os.environ['FLASK_ENV'] = 'development'
    
    try:
        from main import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start development server: {e}")
        sys.exit(1)

def main():
    """Main entry point."""
    print("🎨 Interactive Particle System")
    print("=" * 50)
    
    # Check environment variables
    if not check_environment():
        sys.exit(1)
    
    # Check database connectivity
    if not check_database():
        logger.warning("Database check failed, but continuing anyway...")
    
    # Determine run mode
    mode = os.environ.get('FLASK_ENV', 'production').lower()
    
    if mode == 'development':
        start_development_server()
    else:
        start_production_server()

if __name__ == '__main__':
    main()