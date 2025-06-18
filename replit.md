# KufrBOT - Twitch Chatbot

## Overview

KufrBOT is a Python-based Twitch chatbot that provides interactive features for Twitch streamers and their communities. The bot connects to multiple Twitch channels and responds to commands, with additional integrations for external APIs like Apex Legends statistics. The application includes a Flask-based web dashboard for monitoring and controlling the bot.

## System Architecture

The application follows a multi-threaded architecture with separate components for bot functionality and web interface:

1. **Bot Component**: Asynchronous Twitch bot using TwitchIO library
2. **Web Dashboard**: Flask-based web interface for bot management
3. **Configuration Management**: Environment-based configuration system
4. **Logging System**: Comprehensive logging with file and console output

## Key Components

### Bot Engine (`bot.py`)
- Built on TwitchIO framework for Twitch IRC integration
- Asynchronous event handling for messages and commands
- Multi-channel support with configurable channel list
- Command prefix system for user interactions
- Request cooldown mechanism to prevent spam

### Web Dashboard (`main.py`)
- Flask web server providing bot status monitoring
- RESTful API endpoints for bot control
- Real-time status updates with auto-refresh functionality
- Bootstrap-based responsive UI

### Configuration System (`config.py`)
- Environment variable-based configuration
- Support for `.env` files using python-dotenv
- Configuration validation with required variable checking
- Flexible settings for tokens, channels, and API keys

### Frontend Interface
- HTML templates using Jinja2 templating
- Bootstrap CSS framework for responsive design
- Feather icons for modern UI elements
- Real-time status updates via JavaScript

## Data Flow

1. **Bot Initialization**: Configuration loaded from environment variables
2. **Connection**: Bot connects to specified Twitch channels using OAuth token
3. **Message Processing**: Incoming messages filtered and processed for commands
4. **Command Execution**: Valid commands trigger appropriate responses
5. **Web Interface**: Flask app provides real-time bot status and control
6. **Logging**: All activities logged to both file and console

## External Dependencies

### Core Libraries
- **TwitchIO**: Twitch IRC client for bot functionality
- **Flask**: Web framework for dashboard interface
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for external API calls

### External Services
- **Twitch IRC**: Primary chat platform integration
- **Apex Legends API**: Game statistics integration (configured but not implemented)

### Authentication
- OAuth token-based authentication for Twitch API access
- Environment variable storage for sensitive credentials

## Deployment Strategy

The application is configured for Replit deployment with the following setup:

1. **Runtime**: Python 3.11 with Nix package management
2. **Process Management**: Parallel workflow execution for bot and web server
3. **Port Configuration**: Flask server on port 5000
4. **Dependencies**: Automatic installation via pip during startup
5. **Environment**: Development server configuration (not production-ready)

### Deployment Considerations
- Uses Flask development server (should be replaced with WSGI server for production)
- Requires manual configuration of environment variables
- Bot runs in separate thread to avoid blocking web interface
- Log files stored locally (consider external logging service for production)

## Changelog

- June 18, 2025: Initial setup and deployment preparation
  - Integrated user's existing ChatGPT-generated Twitch bot code
  - Fixed threading and event loop issues in bot initialization
  - Added secure environment variable configuration for TWITCH_TOKEN and APEX_API_KEY
  - Created Flask web dashboard with bot management controls
  - Successfully connected to Twitch channels: kufric, kufrbot, marqetka
  - Bot commands working: >apex, >cau, >stinky, >uh, >plink, >slots, >uptime
  - Ready for Replit deployment with 24/7 hosting capability

## User Preferences

Preferred communication style: Simple, everyday language.