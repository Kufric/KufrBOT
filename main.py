from flask import Flask, render_template, jsonify
import asyncio
import threading
import logging
import os
from datetime import datetime
from bot import KufrBOT

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
bot_thread = None
bot_status = {
    'running': False,
    'start_time': None,
    'last_message': None,
    'channels': [],
    'error': None
}

def run_bot():
    """Run the bot in a separate thread"""
    global bot_instance, bot_status
    try:
        # Create new event loop for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        bot_instance = KufrBOT()
        bot_status['running'] = True
        bot_status['start_time'] = datetime.now()
        bot_status['error'] = None
        
        # Run the bot
        bot_instance.run()
        
    except Exception as e:
        logging.error(f"Bot error: {e}")
        bot_status['running'] = False
        bot_status['error'] = str(e)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html', status=bot_status)

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify(bot_status)

@app.route('/api/start')
def start_bot():
    """Start the bot"""
    global bot_thread, bot_status
    
    if bot_status['running']:
        return jsonify({'success': False, 'message': 'Bot is already running'})
    
    try:
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        return jsonify({'success': True, 'message': 'Bot started successfully'})
    except Exception as e:
        logging.error(f"Failed to start bot: {e}")
        return jsonify({'success': False, 'message': f'Failed to start bot: {e}'})

@app.route('/api/stop')
def stop_bot():
    """Stop the bot"""
    global bot_instance, bot_status
    
    if not bot_status['running']:
        return jsonify({'success': False, 'message': 'Bot is not running'})
    
    try:
        if bot_instance:
            asyncio.run_coroutine_threadsafe(bot_instance.close(), bot_instance.loop)
        bot_status['running'] = False
        return jsonify({'success': True, 'message': 'Bot stopped successfully'})
    except Exception as e:
        logging.error(f"Failed to stop bot: {e}")
        return jsonify({'success': False, 'message': f'Failed to stop bot: {e}'})

@app.route('/logs')
def logs():
    """Display bot logs"""
    try:
        with open('bot.log', 'r') as f:
            logs = f.read().split('\n')[-100:]  # Last 100 lines
        return render_template('logs.html', logs=logs)
    except FileNotFoundError:
        return render_template('logs.html', logs=['No logs available'])

if __name__ == '__main__':
    # Start the bot automatically
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start the Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
