import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the bot"""
    
    # Twitch Bot Configuration
    TWITCH_TOKEN = os.getenv('TWITCH_TOKEN', 'oauth:your_token_here')
    TWITCH_CHANNELS = os.getenv('TWITCH_CHANNELS', 'kufric,kufrbot,marqetka').split(',')
    COMMAND_PREFIX = os.getenv('COMMAND_PREFIX', '>')
    
    # API Keys
    APEX_API_KEY = os.getenv('APEX_API_KEY', 'your_apex_api_key_here')
    
    # Bot Settings
    REQUEST_COOLDOWN = int(os.getenv('REQUEST_COOLDOWN', '5'))  # seconds
    
    # Flask Configuration
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required_vars = ['TWITCH_TOKEN', 'APEX_API_KEY']
        missing_vars = []
        
        for var in required_vars:
            if not getattr(cls, var) or getattr(cls, var).startswith('your_'):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        return True
