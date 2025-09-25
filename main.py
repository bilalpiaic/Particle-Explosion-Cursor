from app import app  # noqa: F401

# WSGI entry point for production
if __name__ == "__main__":
    import os
    # Use environment variables to determine run mode
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)