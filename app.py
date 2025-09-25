import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from config import get_config, config

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    # Proxy fix for Replit deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize CSRF protection
    csrf = CSRFProtect(app)
    
    # Security headers
    @app.after_request
    def security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.replit.com; style-src 'self' 'unsafe-inline' https://cdn.replit.com;"
        return response
    
    # Health check endpoints
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'interactive-particle-system'}
    
    @app.route('/ready')
    def readiness_check():
        try:
            # Check database connectivity
            db.session.execute(db.text('SELECT 1'))
            return {'status': 'ready'}
        except Exception as e:
            app.logger.error(f'Database connection failed: {e}')
            return {'status': 'not ready', 'error': 'database connection failed'}, 503
    
    # Set up logging for production
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/particle_system.log', maxBytes=10240000, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Interactive Particle System startup')
    
    with app.app_context():
        # Import models to register them
        import models
        db.create_all()
        
        # Register routes directly
        from flask import render_template, request, jsonify
        from models import ParticleSettings, UserPreference
        
        @app.route('/')
        def index():
            """Main particle system page."""
            app.logger.info(f'Index page accessed from {request.remote_addr}')
            return render_template('index.html')
        
        @app.route('/api/settings')
        def get_settings():
            """Get particle system settings."""
            settings = ParticleSettings.query.first()
            if not settings:
                settings = ParticleSettings()
                db.session.add(settings)
                db.session.commit()
            
            return jsonify({
                'max_particles': settings.max_particles,
                'fade_speed': settings.fade_speed,
                'min_size': settings.min_size,
                'max_size': settings.max_size
            })
        
        @app.route('/api/preferences')
        def get_preferences():
            """Get user preferences."""
            prefs = UserPreference.query.first()
            if not prefs:
                prefs = UserPreference()
                db.session.add(prefs)
                db.session.commit()
            
            return jsonify({
                'theme': prefs.theme,
                'particle_color': prefs.particle_color,
                'background_color': prefs.background_color
            })
    
    return app

# Create the application instance
app = create_app()