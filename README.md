# KufrBOT - Twitch Chatbot

A Python-based Twitch chatbot with web dashboard for managing bot operations.

## Features

- Multiple Twitch channel support
- Apex Legends player statistics integration
- Fun interactive commands (slots, stinky percentage, random responses)
- Web dashboard for bot control and monitoring
- Real-time status updates

## Commands

- `>apex [player] [platform]` - Get Apex Legends player statistics
- `>cau` - Say hello
- `>stinky` - Generate random stinky percentage
- `>uh` - Random uh response
- `>plink` - Random plink response  
- `>slots` - Slot machine game
- `>uptime` - Show bot uptime

## Deployment

### Railway.app (Free)

1. Create account at railway.app
2. Connect your GitHub repository
3. Add environment variables:
   - `TWITCH_TOKEN`: Your Twitch OAuth token
   - `APEX_API_KEY`: Your Apex Legends API key
4. Deploy

### Render.com (Free)

1. Create account at render.com
2. Connect repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variables
6. Deploy

## Environment Variables

- `TWITCH_TOKEN`: OAuth token from twitchapps.com/tmi/
- `APEX_API_KEY`: API key from apexlegendsapi.com
- `TWITCH_CHANNELS`: Comma-separated list of channels (default: kufric,kufrbot,marqetka)
- `COMMAND_PREFIX`: Bot command prefix (default: >)

## Local Development

1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your tokens
3. Run: `python main.py`
4. Access dashboard at http://localhost:5000