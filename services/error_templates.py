"""
Error Message Templates for RosethornBot
Pre-defined Victorian Gothic error messages for common scenarios
"""

from typing import Dict, List
import discord
from datetime import datetime

class ErrorTemplates:
    """Collection of pre-built error message templates"""
    
    EMBED_COLOR = 0x711417
    
    @staticmethod
    def permission_denied(user: discord.User, required_permission: str, channel_name: str = None) -> discord.Embed:
        """Permission denied error template"""
        embed = discord.Embed(
            title="🚫 Manor Access Restricted",
            description=f"The ancient wards of the manor prevent your passage, {user.mention}.",
            color=0x8B0000,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🗝️ Required Permission",
            value=f"`{required_permission}`",
            inline=True
        )
        
        if channel_name:
            embed.add_field(
                name="🏰 Chamber",
                value=f"#{channel_name}",
                inline=True
            )
        
        embed.add_field(
            name="💡 Solution",
            value="Contact a manor administrator to grant you the necessary noble privileges.",
            inline=False
        )
        
        embed.set_footer(text="The Butler has been notified of this access attempt")
        return embed
    
    @staticmethod
    def user_not_found(username: str) -> discord.Embed:
        """User not found error template"""
        embed = discord.Embed(
            title="👻 Vanished Into the Mist",
            description=f"The guest **{username}** appears to have disappeared into the manor's mysterious corridors.",
            color=0x8B4513,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🔍 Search Attempts",
            value="• Checked the grand ballroom\n• Searched the library archives\n• Inquired with the manor staff",
            inline=False
        )
        
        embed.add_field(
            name="💡 Suggestions",
            value="• Verify the exact spelling of the name\n• Ensure the user is in this server\n• Check if they've recently changed their name",
            inline=False
        )
        
        embed.set_footer(text="Perhaps they've simply stepped out for evening tea")
        return embed
    
    @staticmethod
    def invalid_input(command_name: str, expected_format: str) -> discord.Embed:
        """Invalid input error template"""
        embed = discord.Embed(
            title="📜 Illegible Parchment",
            description="Your manuscript contains script that confounds our Victorian scribes.",
            color=0x8B4513,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🖋️ Command",
            value=f"`/{command_name}`",
            inline=True
        )
        
        embed.add_field(
            name="📝 Expected Format",
            value=f"`{expected_format}`",
            inline=False
        )
        
        embed.add_field(
            name="💡 Writing Tips",
            value="• Ensure all required parameters are included\n• Check spelling and syntax\n• Review command examples",
            inline=False
        )
        
        embed.set_footer(text="Lady Rosalind's writing instructor is available for consultation")
        return embed
    
    @staticmethod
    def database_error(operation: str = "database operation") -> discord.Embed:
        """Database error template"""
        embed = discord.Embed(
            title="📚 Manor Records Corrupted",
            description="The ancient ledgers have suffered from supernatural interference.",
            color=0xDC143C,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📖 Affected Operation",
            value=operation,
            inline=True
        )
        
        embed.add_field(
            name="🔮 Status",
            value="Archive spirits are investigating",
            inline=True
        )
        
        embed.add_field(
            name="⏳ Recovery Actions",
            value="• Wait a few moments and try again\n• Contact support if issue persists\n• Check system status announcements",
            inline=False
        )
        
        embed.set_footer(text="The manor's record-keepers are working to restore order")
        return embed
    
    @staticmethod
    def rate_limited(cooldown_seconds: int, command_name: str) -> discord.Embed:
        """Rate limit error template"""
        embed = discord.Embed(
            title="⏳ Manor Etiquette Violated",
            description="Your enthusiasm exceeds the manor's capacity for immediate response.",
            color=0x8B4513,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="⌛ Cooldown Remaining",
            value=f"{cooldown_seconds} seconds",
            inline=True
        )
        
        embed.add_field(
            name="🖋️ Command",
            value=f"`/{command_name}`",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Victorian Etiquette",
            value="Patience is a virtue most becoming of distinguished guests.",
            inline=False
        )
        
        embed.set_footer(text="The servants require time to process your previous requests")
        return embed
    
    @staticmethod
    def insufficient_funds(current_balance: int, required_amount: int) -> discord.Embed:
        """Insufficient funds error template"""
        embed = discord.Embed(
            title="💰 Treasury Coffers Empty",
            description="Your rosebud reserves are insufficient for this noble transaction.",
            color=0x8B0000,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🪙 Current Balance",
            value=f"{current_balance:,} Rosebuds",
            inline=True
        )
        
        embed.add_field(
            name="💎 Required Amount",
            value=f"{required_amount:,} Rosebuds",
            inline=True
        )
        
        embed.add_field(
            name="📊 Shortfall",
            value=f"{required_amount - current_balance:,} Rosebuds",
            inline=True
        )
        
        embed.add_field(
            name="💡 Wealth Building Suggestions",
            value="• Use `/daily` for regular income\n• Complete `/work` tasks\n• Participate in manor activities\n• Check `/shop` for earning opportunities",
            inline=False
        )
        
        embed.set_footer(text="The manor's financial advisor is available for consultation")
        return embed
    
    @staticmethod
    def feature_disabled(feature_name: str, reason: str = "maintenance") -> discord.Embed:
        """Feature disabled error template"""
        embed = discord.Embed(
            title="⚙️ Manor Systems Under Maintenance",
            description=f"The **{feature_name}** feature is temporarily unavailable while our Victorian engineers perform essential maintenance.",
            color=0x8B4513,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🔧 Reason",
            value=reason.title(),
            inline=True
        )
        
        embed.add_field(
            name="⏱️ Expected Resolution",
            value="Soon™",
            inline=True
        )
        
        embed.add_field(
            name="📢 Updates",
            value="Manor announcements will provide progress updates",
            inline=False
        )
        
        embed.set_footer(text="We apologize for any inconvenience during this improvement period")
        return embed
    
    @staticmethod
    def command_on_cooldown(command_name: str, retry_after: float) -> discord.Embed:
        """Command cooldown error template"""
        minutes = int(retry_after // 60)
        seconds = int(retry_after % 60)
        
        time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
        
        embed = discord.Embed(
            title="🕰️ Patience Required, Dear Guest",
            description=f"The `/{command_name}` command requires a moment of respite before it can be used again.",
            color=0x8B4513,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="⏳ Time Remaining",
            value=time_str,
            inline=True
        )
        
        embed.add_field(
            name="🎭 Manor Philosophy",
            value="All good things come to those who wait with Victorian grace.",
            inline=False
        )
        
        embed.set_footer(text="Use this time to explore other manor amenities")
        return embed
    
    @staticmethod
    def maintenance_mode() -> discord.Embed:
        """Maintenance mode error template"""
        embed = discord.Embed(
            title="🏰 Manor Under Renovation",
            description="The entire manor is currently undergoing essential improvements to better serve our distinguished guests.",
            color=0xDC143C,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🔨 Current Work",
            value="• Polishing the grand chandeliers\n• Updating the ancient automation systems\n• Enhancing the guest experience",
            inline=False
        )
        
        embed.add_field(
            name="⏰ Expected Completion",
            value="The renovation will be completed shortly. Please check back soon.",
            inline=False
        )
        
        embed.add_field(
            name="📬 Stay Informed",
            value="Follow manor announcements for updates on our progress.",
            inline=False
        )
        
        embed.set_footer(text="Thank you for your patience during this improvement period")
        return embed

# Export templates for easy import
templates = ErrorTemplates()