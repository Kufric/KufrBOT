import random
import requests
import asyncio
import signal
import logging
import os
from datetime import datetime
from twitchio.ext import commands
from config import Config

class KufrBOT(commands.Bot):
    def __init__(self):
        # Get configuration from environment variables
        token = Config.TWITCH_TOKEN
        channels = Config.TWITCH_CHANNELS
        
        if not token:
            raise ValueError("TWITCH_TOKEN environment variable is required")
        
        if not channels:
            raise ValueError("TWITCH_CHANNELS environment variable is required")
        
        super().__init__(
            token=token, 
            prefix=Config.COMMAND_PREFIX,
            initial_channels=channels
        )
        
        self.prefix = Config.COMMAND_PREFIX  # Store prefix for later use
        self.last_request_time = 0
        self.logger = logging.getLogger('KufrBOT')
        self.start_time = datetime.now()
        
        self.logger.info(f'Bot initialized for channels: {channels}')

    async def event_ready(self):
        """Called when the bot is ready"""
        self.logger.info(f'Bot logged in as: {self.nick}')
        self.logger.info(f'Command prefix: {self.prefix}')
        
        # Announce bot is online
        for channel in self.connected_channels:
            try:
                await channel.send('yo')
                self.logger.info(f'Announced presence in channel: {channel.name}')
            except Exception as e:
                self.logger.error(f'Failed to announce in channel {channel.name}: {e}')

    async def event_command_error(self, context, error):
        """Handle command errors"""
        self.logger.error(f'Command error in {context.command}: {error}')
        await context.send(f'Nastala chyba s příkazem. <@{context.author.name}>')

    async def event_message(self, message):
        """Handle incoming messages"""
        if message.author is None:
            self.logger.warning("Received message with no author, skipping")
            return

        # Ignore messages from the bot itself
        if message.author.name.lower() == self.nick.lower():
            return

        self.logger.debug(f'Message from {message.author.name}: {message.content}')

        # Always process commands - this is crucial!
        await self.handle_commands(message)

    async def announce_shutdown(self):
        """Announce bot shutdown"""
        self.logger.info("Announcing bot shutdown")
        for channel in self.connected_channels:
            try:
                await channel.send('leavuju, papa')
            except Exception as e:
                self.logger.error(f'Failed to announce shutdown in {channel.name}: {e}')

    @staticmethod
    async def fetch_player_stats(player_name, ctx, platform='PC'):
        """Fetch Apex Legends player statistics"""
        api_key = Config.APEX_API_KEY
        
        if not api_key:
            return f"Apex API key není nakonfigurován. <@{ctx.author.name}>"
        
        url = f"https://api.mozambiquehe.re/bridge?auth={api_key}&player={player_name}&platform={platform}"
        
        try:
            response = requests.get(url, timeout=10)
            
            logging.info(f"Apex API request - URL: {url}")
            logging.info(f"Apex API response - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # Parse player statistics
                career_kills_data = data.get('total', {}).get('career_kills', {})
                career_kills_value = career_kills_data.get('value', 'N/A')
                
                # Get rank information
                rank_name = data.get('global', {}).get('rank', {}).get('rankName', 'Unranked')
                rank_div = data.get('global', {}).get('rank', {}).get('rankDiv', 'N/A')
                rank = f"{rank_name} {rank_div}" if rank_div != 'N/A' else rank_name
                
                # Get selected legend
                selected_legend = data.get('legends', {}).get('selected', {}).get('LegendName', 'Unknown')
                
                # Get BR kills for selected legend
                selected_legend_kills_data = data.get('legends', {}).get('selected', {}).get('data', [])
                selected_legend_br_kills = 'N/A'
                
                for stat in selected_legend_kills_data:
                    if stat.get('name') == 'BR Kills':
                        selected_legend_br_kills = stat.get('value', 'N/A')
                        break
                
                return (f"Apex statistiky uživatele {player_name}: Rank: {rank} // "
                       f"Selected Legend: {selected_legend} with {selected_legend_br_kills} Kills // "
                       f"Career Kills: {career_kills_value} <@{ctx.author.name}>")
                       
            elif response.status_code == 429:
                return f"Limit překročen. Chvíli počkej a zkus to znovu. <@{ctx.author.name}>"
            elif response.status_code == 404:
                return f"Nelze načíst statistiky, zkus nejdříve najít svůj profil na apexlegendsstatus.com <@{ctx.author.name}>"
            else:
                return f"Nelze načíst statistiky pro {player_name}. Status: {response.status_code}. <@{ctx.author.name}>"
                
        except requests.exceptions.RequestException as e:
            logging.error(f"Apex API request failed: {e}")
            return f"Chyba při načítání statistik. Zkus to znovu později. <@{ctx.author.name}>"

    @commands.command(name='apex')
    async def apex(self, ctx, player_name: str = None, platform: str = None):
        """Get Apex Legends player statistics"""
        if player_name is None or platform is None or player_name.lower() == "help":
            await ctx.send(f'Použij >apex (username) (PC/PS4/X1/SWITCH) <@{ctx.author.name}>')
            return

        current_time = asyncio.get_event_loop().time()
        
        # Rate limiting
        if current_time - self.last_request_time < 5:
            await ctx.send(f'Chvíli počkej a zkus to znovu. <@{ctx.author.name}>')
            return

        try:
            player_stats = await KufrBOT.fetch_player_stats(player_name, ctx, platform)
            await ctx.send(player_stats)
            self.last_request_time = current_time
            self.logger.info(f'Apex command executed for {player_name} by {ctx.author.name}')
        except Exception as e:
            self.logger.error(f'Apex command error: {e}')
            await ctx.send(f'Nastala chyba při načítání statistik. <@{ctx.author.name}>')

    @commands.command(name='cau')
    async def cau(self, ctx):
        """Say hello"""
        await ctx.send(f'cau {ctx.author.name}')
        self.logger.info(f'Cau command executed by {ctx.author.name}')

    @commands.command(name='stinky')
    async def stinky(self, ctx):
        """Generate random stinky percentage"""
        stinky_percentage = random.randint(1, 100)
        await ctx.send(f'{ctx.author.name} je z {stinky_percentage}% smradoch.')
        self.logger.info(f'Stinky command executed by {ctx.author.name}: {stinky_percentage}%')

    @commands.command(name='uh')
    async def uh(self, ctx):
        """Random uh response"""
        uh_list = ['buh', 'wuh', 'puh', 'guh', 'muh', 'duh', 'cuh', 'ruh', 'vuh', 'euh', 'nuh', 'zuh', 'kuh', 'huh']
        selected_word = random.choice(uh_list)
        await ctx.send(f"{selected_word} <@{ctx.author.name}>")
        self.logger.info(f'Uh command executed by {ctx.author.name}: {selected_word}')

    @commands.command(name='plink')
    async def plink(self, ctx):
        """Random plink response"""
        plink_list = [
            "plink", "plonk", "bitrate", "wink", "plink-182", "LETHIMPLINK", "plinkge", "clean", "eww",
            "plunk", "plinkerton", "plinkplink", "Shocked", "mlem", "pleep", "plinktosis", "plenk", "star",
            "yum", "plinkStare", "crunch", "Buggin", "plinkChamp", "pl", "blepping", "SmolestPlink", "pwink",
            "framerate"
        ]
        selected_word = random.choice(plink_list)
        await ctx.send(f"{selected_word} <@{ctx.author.name}>")
        self.logger.info(f'Plink command executed by {ctx.author.name}: {selected_word}')

    @commands.command(name='slots')
    async def slots(self, ctx):
        """Slot machine game"""
        slots_list = [" maxwin ", "🍆", "🍇", "🍏", "🍒", "🍋", "🍍", "🍑", "🍓", "🍉", "🫐", "🍌", "🍎", "🍊"]
        result = [random.choice(slots_list) for _ in range(3)]
        await ctx.send(f"[{''.join(result)}] <@{ctx.author.name}>")
        self.logger.info(f'Slots command executed by {ctx.author.name}: {result}')

    @commands.command(name='uptime')
    async def uptime(self, ctx):
        """Show bot uptime"""
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
        await ctx.send(f'Bot běží {uptime_str} <@{ctx.author.name}>')
        self.logger.info(f'Uptime command executed by {ctx.author.name}: {uptime_str}')

    @commands.command(name='help')
    async def help(self, ctx):
        """List all available commands"""
        help_text = (
            f"Dostupné příkazy <@{ctx.author.name}>: "
            f">apex [player] [platform] - Apex Legends statistiky // "
            f">cau - Pozdrav // "
            f">stinky - Náhodné smradoch % // "
            f">uh - Náhodná uh odpověď // "
            f">plink - Náhodná plink odpověď // "
            f">slots - Hrací automat // "
            f">uptime - Doba běhu bota // "
            f">help - Zobrazí tento seznam"
        )
        await ctx.send(help_text)
        self.logger.info(f'Help command executed by {ctx.author.name}')

    async def close(self):
        """Graceful shutdown"""
        self.logger.info("Bot shutting down...")
        await self.announce_shutdown()
        await super().close()


# Signal handler for graceful shutdown
def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logging.info(f"Received signal {signum}, shutting down...")
    # This will be handled by the main application

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the bot
    bot = KufrBOT()
    try:
        bot.run()
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.error(f"Bot crashed: {e}")
