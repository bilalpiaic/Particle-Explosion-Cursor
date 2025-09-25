# Interactive Particle System

## Overview

This is a web-based interactive particle system built with Flask and p5.js. The application creates a dynamic visual experience where particles are generated in response to user mouse interactions. The system features a real-time particle animation with customizable settings and user preferences stored in a database. The particles exhibit realistic physics behavior including movement, fading, and lifecycle management, creating an engaging interactive canvas experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask with SQLAlchemy ORM for database operations
- **Database**: PostgreSQL (configured via DATABASE_URL environment variable)
- **Models**: Two primary data models - ParticleSettings for animation configuration and UserPreference for visual theming
- **Application Structure**: Modular design with separate files for app initialization, models, and routes
- **Database Management**: Automatic table creation on startup with connection pooling for reliability

### Frontend Architecture
- **Rendering Engine**: p5.js JavaScript library for canvas-based graphics and animations
- **UI Framework**: Bootstrap with Replit dark theme for consistent styling
- **Animation System**: Object-oriented particle system with individual Particle class instances
- **Performance Optimization**: Maximum particle limit (1000) and efficient particle lifecycle management
- **Responsive Design**: Automatic canvas resizing and mobile touch optimization

### Data Models
- **ParticleSettings**: Configures animation parameters including max_particles, fade_speed, particle size ranges
- **UserPreference**: Stores visual customization options like theme, particle_color, and background_color
- **Timestamps**: Both models include created_at and updated_at fields for tracking changes

### Particle System Design
- **Physics Simulation**: Each particle has position, velocity, size, and lifetime properties
- **Lifecycle Management**: Particles automatically shrink and fade over time before removal
- **Interactive Generation**: New particles spawn based on mouse movement and clicks
- **Performance Considerations**: Dead particle cleanup and maximum particle count enforcement

## External Dependencies

### Frontend Libraries
- **p5.js (v1.9.0)**: Core graphics library for canvas rendering and animation
- **Bootstrap**: UI framework with Replit dark theme integration via CDN

### Backend Dependencies
- **Flask**: Web framework for application structure and routing
- **Flask-SQLAlchemy**: Database ORM for model management and queries
- **PostgreSQL**: Primary database for persistent storage of settings and preferences

### Environment Configuration
- **DATABASE_URL**: PostgreSQL connection string for database access
- **SESSION_SECRET**: Flask session management security key

### Development Dependencies
- **Logging**: Built-in Python logging for debugging and monitoring
- **Debug Mode**: Flask development server with auto-reload capabilities