
from flask import Flask, render_template, jsonify
import asyncio
import threading
import logging
import os
from datetime import datetime
from bot import KufrBOT
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
bot_instance = None
bot_task = None
bot_loop = None
bot_status = {
    'running': False,
    'start_time': None,
    'last_message': None,
    'channels': [],
    'error': None
}

def run_bot_loop():
    """Run the bot in a separate thread with its own event loop"""
    global bot_instance, bot_task, bot_loop, bot_status
    try:
        # Create new event loop for the thread
        bot_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(bot_loop)
        
        bot_instance = KufrBOT()
        bot_status['running'] = True
        bot_status['start_time'] = datetime.now()
        bot_status['error'] = None
        bot_status['channels'] = bot_instance.initial_channels
        
        logging.info("Starting bot in separate thread...")
        
        # Run the bot
        bot_loop.run_until_complete(bot_instance.start())
        
    except Exception as e:
        logging.error(f"Bot error: {e}")
        bot_status['running'] = False
        bot_status['error'] = str(e)
    finally:
        if bot_loop and not bot_loop.is_closed():
            bot_loop.close()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', status=bot_status)

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    current_status = bot_status.copy()
    if bot_instance and hasattr(bot_instance, 'connected_channels'):
        current_status['channels'] = [ch.name for ch in bot_instance.connected_channels]
    return jsonify(current_status)

@app.route('/api/start')
def start_bot():
    """Start the bot"""
    global bot_status
    
    if bot_status['running']:
        return jsonify({'success': False, 'message': 'Bot is already running'})
    
    try:
        bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
        bot_thread.start()
        return jsonify({'success': True, 'message': 'Bot started successfully'})
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        return jsonify({'success': False, 'message': f'Failed to start bot: {e}'})

@app.route('/api/stop')
def stop_bot():
    """Stop the bot"""
    global bot_instance, bot_status, bot_loop
    
    if not bot_status['running']:
        return jsonify({'success': False, 'message': 'Bot is not running'})
    
    try:
        if bot_instance and bot_loop:
            # Schedule the close coroutine in the bot's event loop
            future = asyncio.run_coroutine_threadsafe(bot_instance.close(), bot_loop)
            future.result(timeout=5)  # Wait up to 5 seconds
        
        bot_status['running'] = False
        return jsonify({'success': True, 'message': 'Bot stopped successfully'})
    except Exception as e:
        logging.error(f"Failed to stop bot: {e}")
        bot_status['running'] = False  # Force status update
        return jsonify({'success': True, 'message': 'Bot force stopped'})

@app.route('/logs')
def logs():
    """Display bot logs"""
    try:
        with open('bot.log', 'r') as f:
            logs = f.read().split('\n')[-100:]  # Last 100 lines
        return render_template('logs.html', logs=logs)
    except FileNotFoundError:
        return render_template('logs.html', logs=['No logs available'])

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    global bot_instance, bot_loop
    logging.info(f"Received signal {signum}, shutting down...")
    
    if bot_instance and bot_loop:
        try:
            future = asyncio.run_coroutine_threadsafe(bot_instance.close(), bot_loop)
            future.result(timeout=5)
        except:
            pass
    
    sys.exit(0)

if __name__ == '__main__':
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    
    # Start the bot automatically
    bot_thread = threading.Thread(target=run_bot_loop, daemon=True)
    bot_thread.start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=port, debug=False)
