"""Utility cog with slash commands."""
import discord
from discord import app_commands
from discord.ext import commands
import config
from datetime import datetime

class Utility(commands.Cog):
    """Utility and information commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="ping", description="Check bot latency")
    async def ping(self, interaction: discord.Interaction):
        """Check bot latency."""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title=f"{config.get_emoji('go_cougs')} Pong!",
            description=f"Bot latency: `{latency}ms`",
            color=config.INFO_COLOR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="serverinfo", description="Get server information")
    async def serverinfo(self, interaction: discord.Interaction):
        """Get information about the server."""
        guild = interaction.guild
        
        embed = discord.Embed(
            title=f"{config.get_emoji('big12')} Server Info - {guild.name}",
            color=config.PRIMARY_COLOR,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention if guild.owner else "Unknown", inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Members", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Text Channels", value=len(guild.text_channels), inline=True)
        embed.add_field(name="Voice Channels", value=len(guild.voice_channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Verification Level", value=str(guild.verification_level), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="userinfo", description="Get user information")
    @app_commands.describe(member="User to lookup (defaults to yourself)")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        """Get information about a user."""
        if member is None:
            member = interaction.user
        
        embed = discord.Embed(
            title=f"User Info - {member}",
            color=config.PRIMARY_COLOR,
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
        
        embed.add_field(name="Username", value=member.mention, inline=True)
        embed.add_field(name="User ID", value=member.id, inline=True)
        embed.add_field(name="Bot", value="Yes" if member.bot else "No", inline=True)
        embed.add_field(name="Account Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d") if member.joined_at else "Unknown", inline=True)
        
        roles = [role.mention for role in member.roles if role != interaction.guild.default_role]
        embed.add_field(name="Roles", value=" ".join(roles) if roles else "None", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="roleinfo", description="Get role information")
    @app_commands.describe(role="Role to lookup")
    async def roleinfo(self, interaction: discord.Interaction, role: discord.Role):
        """Get information about a role."""
        embed = discord.Embed(
            title=f"{config.get_emoji('student')} Role Info - {role.name}",
            color=role.color if role.color != discord.Color.default() else config.INFO_COLOR,
            timestamp=datetime.now()
        )
        
        embed.add_field(name="Role ID", value=role.id, inline=True)
        embed.add_field(name="Created", value=role.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
        embed.add_field(name="Hoisted", value="Yes" if role.hoist else "No", inline=True)
        embed.add_field(name="Managed", value="Yes" if role.managed else "No", inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="help", description="Show help information")
    async def help_command(self, interaction: discord.Interaction):
        """Show help information."""
        embed = discord.Embed(
            title=f"{config.get_emoji('go_cougs')} BYU Bot Help",
            description="Available slash commands and features",
            color=config.PRIMARY_COLOR
        )
        
        embed.add_field(
            name=f"{config.get_emoji('alert')} Moderation",
            value="`/warn` - Warn a user\n"
                  "`/warnings` - View user warnings\n"
                  "`/kick` - Kick a user\n"
                  "`/ban` - Ban a user\n"
                  "`/mute` - Mute a user\n"
                  "`/purge` - Delete messages",
            inline=False
        )
        
        embed.add_field(
            name="📝 Embeds",
            value="`/create_embed` - Create custom embed\n"
                  "`/send_embed` - Send embed to channel\n"
                  "`/announcement` - Post announcement",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('partner')} Reaction Roles",
            value="`/add_reaction_role` - Add reaction role\n"
                  "`/list_reaction_roles` - List reaction roles\n"
                  "`/create_reaction_role_message` - Create role message",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('go_cougs')} Welcome",
            value="`/set_welcome` - Set welcome message\n"
                  "`/view_welcome` - View settings\n"
                  "`/toggle_welcome` - Toggle welcome",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('staff')} Staff Management",
            value="`/staff_add` - Add staff member\n"
                  "`/staff_list` - List staff\n"
                  "`/staff_info` - Staff info",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('alert')} Staff Tasks",
            value="`/task_assign` - Assign task to staff\n"
                  "`/my_tasks` - View your tasks\n"
                  "`/task_complete` - Mark task complete\n"
                  "`/all_tasks` - View all tasks",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('alert')} Reminders",
            value="`/remind` - Set a reminder\n"
                  "`/reminders` - View reminders\n"
                  "`/delete_reminder` - Delete reminder",
            inline=False
        )
        
        embed.add_field(
            name=f"{config.get_emoji('alert')} Sticky Messages",
            value="`/sticky_set` - Set sticky message\n"
                  "`/sticky_remove` - Remove sticky\n"
                  "`/sticky_view` - View sticky\n"
                  "`/sticky_toggle` - Toggle sticky",
            inline=False
        )
        
        embed.add_field(
            name="ℹ️ Utility",
            value="`/ping` - Bot latency\n"
                  "`/serverinfo` - Server info\n"
                  "`/userinfo` - User info",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Utility(bot))
