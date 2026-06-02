"""Alert Log cog for managing alert logging settings."""
import discord
from discord import app_commands
from discord.ext import commands
import config
from database import db
from datetime import datetime

class AlertLog(commands.Cog):
    """Manage alert log settings."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.group(name="alertlog", description="Alert log commands")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def alertlog_group(self, interaction: discord.Interaction):
        """Alert log command group."""
        if interaction.invoked_subcommand is None:
            embed = discord.Embed(
                title=f"{config.get_emoji('alert')} Alert Log Commands",
                description="Manage what events are logged to the alert log",
                color=config.INFO_COLOR
            )
            embed.add_field(
                name="Setup",
                value="`/alertlog set_channel` - Set alert log channel",
                inline=False
            )
            embed.add_field(
                name="Toggle Events",
                value="`/alertlog toggle` - Toggle individual event types",
                inline=False
            )
            embed.add_field(
                name="View",
                value="`/alertlog view` - View current settings\n`/alertlog status` - View all event statuses",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @alertlog_group.command(name="set_channel", description="Set the alert log channel")
    @app_commands.describe(channel="Channel to use for alert logs")
    async def set_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the alert log channel."""
        try:
            await db.set_alert_log_channel(interaction.guild.id, channel.id)
            
            embed = discord.Embed(
                title=f"{config.get_emoji('success')} Alert Log Channel Set",
                description=f"Alert log channel set to {channel.mention}",
                color=config.SUCCESS_COLOR,
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title=f"{config.get_emoji('error')} Error",
                description=f"Failed to set alert log channel: {str(e)}",
                color=config.ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @alertlog_group.command(name="toggle", description="Toggle an alert event type")
    @app_commands.describe(
        event="Event type to toggle",
        enabled="Enable or disable"
    )
    async def toggle_event(self, interaction: discord.Interaction, event: str, enabled: bool):
        """Toggle an alert event type."""
        valid_events = ["warn", "kick", "ban", "mute", "unmute", "message_delete", "message_edit", "member_join", "member_leave", "role_change", "channel_create", "channel_delete"]
        
        if event.lower() not in valid_events:
            embed = discord.Embed(
                title=f"{config.get_emoji('error')} Invalid Event",
                description=f"Valid events: {', '.join(valid_events)}",
                color=config.ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            await db.toggle_alert_event(interaction.guild.id, event.lower(), enabled)
            
            state = "✅ Enabled" if enabled else "❌ Disabled"
            embed = discord.Embed(
                title=f"{config.get_emoji('alert')} Alert Event Updated",
                description=f"`{event.lower()}` has been {state.lower()}",
                color=config.SUCCESS_COLOR,
                timestamp=datetime.now()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title=f"{config.get_emoji('error')} Error",
                description=f"Failed to toggle event: {str(e)}",
                color=config.ERROR_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @alertlog_group.command(name="view", description="View current alert log settings")
    async def view_settings(self, interaction: discord.Interaction):
        """View current alert log settings."""
        settings = await db.get_alert_log_settings(interaction.guild.id)
        
        if not settings:
            embed = discord.Embed(
                title="No Alert Log Configured",
                description="Use `/alertlog set_channel` to configure the alert log.",
                color=config.INFO_COLOR
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        channel_id = settings[0]
        channel = interaction.guild.get_channel(channel_id) if channel_id else None
        
        embed = discord.Embed(
            title=f"{config.get_emoji('alert')} Alert Log Settings",
            color=config.PRIMARY_COLOR
        )
        embed.add_field(
            name="Alert Log Channel",
            value=channel.mention if channel else "Not configured",
            inline=False
        )
        embed.add_field(
            name="Configure events with:",
            value="`/alertlog toggle <event> <true/false>`",
            inline=False
        )
        embed.add_field(
            name="View all statuses:",
            value="`/alertlog status`",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @alertlog_group.command(name="status", description="View all alert event statuses")
    async def view_status(self, interaction: discord.Interaction):
        """View status of all alert events."""
        settings = await db.get_alert_log_settings(interaction.guild.id)
        
        embed = discord.Embed(
            title=f"{config.get_emoji('alert')} Alert Event Statuses",
            description="Current status of all alert event types",
            color=config.PRIMARY_COLOR
        )
        
        events = ["warn", "kick", "ban", "mute", "unmute", "message_delete", "message_edit", "member_join", "member_leave", "role_change", "channel_create", "channel_delete"]
        
        if not settings:
            for event in events:
                embed.add_field(name=event.title(), value="❌ Disabled (Not configured)", inline=True)
        else:
            columns = ["warn", "kick", "ban", "mute", "unmute", "message_delete", "message_edit", "member_join", "member_leave", "role_change", "channel_create", "channel_delete"]
            for i, event in enumerate(events):
                if i + 1 < len(settings):
                    status = "✅ Enabled" if settings[i + 1] else "❌ Disabled"
                else:
                    status = "❌ Disabled"
                embed.add_field(name=event.title(), value=status, inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(AlertLog(bot))
