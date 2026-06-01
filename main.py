"""Main bot file for BYU Bot with slash commands."""
import discord
from discord.ext import commands
import config
from database import db
import os
import asyncio

# Create bot with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    """Bot is ready."""
    print(f"✅ Bot logged in as {bot.user}")
    print(f"✅ Syncing slash commands...")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="BYU campus"))

@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle slash command errors."""
    if isinstance(error, discord.app_commands.CommandNotFound):
        embed = discord.Embed(
            title=f"{config.get_emoji('error')} Command Not Found",
            description="That command doesn't exist.",
            color=config.ERROR_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif isinstance(error, discord.app_commands.MissingPermissions):
        embed = discord.Embed(
            title=f"{config.get_emoji('error')} Permission Denied",
            description="You don't have permission to use this command.",
            color=config.ERROR_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    elif isinstance(error, discord.app_commands.MissingRole):
        embed = discord.Embed(
            title=f"{config.get_emoji('error')} Missing Role",
            description="You don't have the required role for this command.",
            color=config.ERROR_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    else:
        embed = discord.Embed(
            title=f"{config.get_emoji('error')} Error",
            description=f"An error occurred: {str(error)}",
            color=config.ERROR_COLOR
        )
        if not interaction.response.is_done():
            await interaction.response.send_message(embed=embed, ephemeral=True)
        print(f"Error: {error}")

async def load_cogs():
    """Load all cogs from the cogs folder."""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")

async def main():
    """Main async function."""
    async with bot:
        # Initialize database
        await db.init_db()
        print("✅ Database initialized")
        
        # Load cogs
        await load_cogs()
        
        # Start bot
        await bot.start(config.DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot shutting down...")
