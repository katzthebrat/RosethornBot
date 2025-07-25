"""
Elegant Error Message Design System for RosethornBot
Victorian Gothic themed error handling with comprehensive error types and recovery suggestions
"""

import discord
import logging
import traceback
from enum import Enum
from typing import Optional, Dict, Any, List
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Categories of errors with Victorian Gothic themes"""
    PERMISSION_DENIED = "permission_denied"
    MISSING_PERMISSIONS = "missing_permissions"
    INVALID_INPUT = "invalid_input"
    USER_NOT_FOUND = "user_not_found"
    CHANNEL_NOT_FOUND = "channel_not_found"
    ROLE_NOT_FOUND = "role_not_found"
    DATABASE_ERROR = "database_error"
    API_ERROR = "api_error"
    RATE_LIMITED = "rate_limited"
    FEATURE_DISABLED = "feature_disabled"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    COOLDOWN_ACTIVE = "cooldown_active"
    VALIDATION_FAILED = "validation_failed"
    SYSTEM_ERROR = "system_error"
    MAINTENANCE_MODE = "maintenance_mode"
    COMMAND_FAILED = "command_failed"

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"       # Minor issues, user can continue
    MEDIUM = "medium" # Moderate issues, affects functionality
    HIGH = "high"     # Major issues, blocks user actions
    CRITICAL = "critical" # System-level errors

class VictorianErrorHandler:
    """Elegant Victorian Gothic error message system"""
    
    EMBED_COLOR = 0x711417  # Deep red Victorian color
    ERROR_COLORS = {
        ErrorSeverity.LOW: 0x8B4513,      # Saddle brown
        ErrorSeverity.MEDIUM: 0x8B0000,   # Dark red
        ErrorSeverity.HIGH: 0xDC143C,     # Crimson
        ErrorSeverity.CRITICAL: 0x800000   # Maroon
    }
    
    # Victorian Gothic error titles
    ERROR_TITLES = {
        ErrorType.PERMISSION_DENIED: [
            "🚫 Manor Access Restricted",
            "⚔️ Forbidden Chambers",
            "🗝️ Locked Victorian Doors"
        ],
        ErrorType.MISSING_PERMISSIONS: [
            "👑 Noble Privileges Required",
            "🏰 Manor Authority Needed",
            "⚖️ Insufficient Manor Standing"
        ],
        ErrorType.INVALID_INPUT: [
            "📜 Illegible Parchment",
            "🖋️ Incomprehensible Script",
            "📝 Flawed Documentation"
        ],
        ErrorType.USER_NOT_FOUND: [
            "👻 Vanished Into the Mist",
            "🔍 Lost in the Manor Halls",
            "💨 Disappeared Like Morning Fog"
        ],
        ErrorType.CHANNEL_NOT_FOUND: [
            "🚪 Chamber Cannot Be Located",
            "🗝️ Room Key Misplaced",
            "🏰 Manor Wing Inaccessible"
        ],
        ErrorType.DATABASE_ERROR: [
            "📚 Manor Records Corrupted",
            "🗃️ Archive System Malfunction",
            "📖 Ancient Ledgers Damaged"
        ],
        ErrorType.API_ERROR: [
            "🌐 External Communication Failed",
            "📡 Mystical Connection Severed",
            "🔮 Divination Crystal Clouded"
        ],
        ErrorType.RATE_LIMITED: [
            "⏳ Manor Etiquette Violated",
            "🕰️ Excessive Haste Detected",
            "⌛ Patience Required, Dear Guest"
        ],
        ErrorType.INSUFFICIENT_FUNDS: [
            "💰 Treasury Coffers Empty",
            "🪙 Insufficient Rosebuds",
            "💎 Economic Hardship Detected"
        ],
        ErrorType.SYSTEM_ERROR: [
            "⚡ Manor Systems Disrupted",
            "🔧 Mechanical Complications",
            "⚙️ Victorian Machinery Malfunction"
        ]
    }
    
    # Victorian Gothic error descriptions
    ERROR_DESCRIPTIONS = {
        ErrorType.PERMISSION_DENIED: [
            "The manor's ancient wards prevent your passage through these hallowed halls.",
            "Access to this chamber is reserved for those of higher standing in our Victorian society.",
            "The ghostly guardians whisper that you lack the necessary permissions."
        ],
        ErrorType.MISSING_PERMISSIONS: [
            "Your current manor privileges are insufficient for this noble endeavor.",
            "The Butler requests you acquire proper authorization before proceeding.",
            "Lady Rosalind requires additional credentials for this distinguished task."
        ],
        ErrorType.INVALID_INPUT: [
            "Your parchment bears markings that confound our Victorian scribes.",
            "The syntax of your request eludes our manor's comprehension.",
            "Please rewrite your missive in a more coherent Victorian manner."
        ],
        ErrorType.DATABASE_ERROR: [
            "The manor's ancient record-keeping system has encountered mysterious complications.",
            "Our Victorian ledgers appear to have suffered from supernatural interference.",
            "The archive spirits are temporarily indisposed. Please try again momentarily."
        ],
        ErrorType.RATE_LIMITED: [
            "Your enthusiasm exceeds the manor's capacity for immediate response.",
            "Victorian etiquette demands a more measured pace of interaction.",
            "Please allow the servants time to process your previous requests."
        ]
    }
    
    # Recovery suggestions
    RECOVERY_SUGGESTIONS = {
        ErrorType.PERMISSION_DENIED: [
            "Contact a manor administrator for elevated privileges",
            "Verify your role assignments in the server settings",
            "Ensure you're using this command in the appropriate channel"
        ],
        ErrorType.MISSING_PERMISSIONS: [
            "Request additional roles from server moderators",
            "Check if you have the required permissions for this action",
            "Try using this command in a different channel"
        ],
        ErrorType.INVALID_INPUT: [
            "Review the command syntax and try again",
            "Ensure all required parameters are provided",
            "Check for typos in your command arguments"
        ],
        ErrorType.DATABASE_ERROR: [
            "Wait a few moments and try your request again",
            "Contact support if the issue persists",
            "Check if the bot is experiencing maintenance"
        ],
        ErrorType.RATE_LIMITED: [
            "Wait a few seconds before trying again",
            "Reduce the frequency of your commands",
            "Try again after the cooldown period expires"
        ]
    }
    
    @classmethod
    def create_error_embed(
        cls,
        error_type: ErrorType,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        custom_message: Optional[str] = None,
        details: Optional[str] = None,
        user: Optional[discord.User] = None,
        recovery_actions: Optional[List[str]] = None,
        footer_text: Optional[str] = None
    ) -> discord.Embed:
        """Create an elegant Victorian Gothic error embed"""
        
        # Select random title and description
        title = random.choice(cls.ERROR_TITLES.get(error_type, ["🥀 Manor Complication"]))
        description = custom_message or random.choice(cls.ERROR_DESCRIPTIONS.get(error_type, ["An unexpected complication has arisen in the manor."]))
        
        # Create embed with appropriate color
        embed = discord.Embed(
            title=title,
            description=description,
            color=cls.ERROR_COLORS.get(severity, cls.EMBED_COLOR),
            timestamp=datetime.now()
        )
        
        # Add user context if provided
        if user:
            embed.add_field(
                name="👤 Affected Guest",
                value=user.mention,
                inline=True
            )
        
        # Add severity indicator
        severity_icons = {
            ErrorSeverity.LOW: "🌿 Minor Inconvenience",
            ErrorSeverity.MEDIUM: "⚠️ Notable Concern",
            ErrorSeverity.HIGH: "🚨 Urgent Matter",
            ErrorSeverity.CRITICAL: "💀 Critical Situation"
        }
        
        embed.add_field(
            name="📊 Severity",
            value=severity_icons.get(severity, "⚠️ Unknown"),
            inline=True
        )
        
        # Add timestamp
        embed.add_field(
            name="🕰️ Occurred",
            value=discord.utils.format_dt(datetime.now(), style='R'),
            inline=True
        )
        
        # Add technical details if provided
        if details:
            embed.add_field(
                name="🔍 Technical Details",
                value=f"```{details[:1020]}```" if len(details) > 1020 else f"```{details}```",
                inline=False
            )
        
        # Add recovery suggestions
        suggestions = recovery_actions or cls.RECOVERY_SUGGESTIONS.get(error_type, [])
        if suggestions:
            suggestion_text = "\n".join([f"• {suggestion}" for suggestion in suggestions[:3]])
            embed.add_field(
                name="💡 Suggested Remedies",
                value=suggestion_text,
                inline=False
            )
        
        # Add footer
        footer_messages = [
            "The manor apologizes for this inconvenience",
            "Victorian complications require Victorian solutions",
            "Lady Rosalind is investigating this matter",
            "The Butler has been notified of this issue",
            "Manor maintenance is working to resolve this"
        ]
        
        embed.set_footer(
            text=footer_text or random.choice(footer_messages),
            icon_url="https://cdn.discordapp.com/emojis/987654321098765432.png"  # Victorian rose icon
        )
        
        return embed
    
    @classmethod
    async def handle_command_error(
        cls,
        interaction: discord.Interaction,
        error: Exception,
        command_name: Optional[str] = None
    ) -> None:
        """Handle command errors with elegant error messages"""
        
        try:
            # Determine error type and severity
            error_type, severity = cls._classify_error(error)
            
            # Create detailed error message
            error_details = str(error) if len(str(error)) < 500 else str(error)[:500] + "..."
            
            # Create error embed
            embed = cls.create_error_embed(
                error_type=error_type,
                severity=severity,
                details=error_details,
                user=interaction.user,
                custom_message=cls._get_user_friendly_message(error, command_name)
            )
            
            # Send error response
            if interaction.response.is_done():
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            # Log error for debugging
            logger.error(f"Command error in {command_name or 'unknown'}: {error}")
            logger.error(traceback.format_exc())
            
        except Exception as e:
            # Fallback error handling
            logger.error(f"Error in error handler: {e}")
            try:
                fallback_embed = discord.Embed(
                    title="🥀 Unexpected Manor Complication",
                    description="The manor has encountered an unforeseen difficulty. Our staff is working to resolve this matter.",
                    color=0x800000
                )
                
                if interaction.response.is_done():
                    await interaction.followup.send(embed=fallback_embed, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=fallback_embed, ephemeral=True)
            except:
                pass  # Last resort - do nothing if we can't even send fallback
    
    @classmethod
    def _classify_error(cls, error: Exception) -> tuple[ErrorType, ErrorSeverity]:
        """Classify error type and severity"""
        
        error_str = str(error).lower()
        error_type_name = type(error).__name__.lower()
        
        # Permission errors
        if any(keyword in error_str for keyword in ['permission', 'forbidden', 'unauthorized']):
            return ErrorType.PERMISSION_DENIED, ErrorSeverity.MEDIUM
        
        # Missing permissions
        if any(keyword in error_str for keyword in ['missing permissions', 'insufficient']):
            return ErrorType.MISSING_PERMISSIONS, ErrorSeverity.MEDIUM
        
        # Invalid input
        if any(keyword in error_str for keyword in ['invalid', 'bad request', 'malformed']):
            return ErrorType.INVALID_INPUT, ErrorSeverity.LOW
        
        # Not found errors
        if any(keyword in error_str for keyword in ['not found', 'unknown user', 'unknown channel']):
            if 'user' in error_str:
                return ErrorType.USER_NOT_FOUND, ErrorSeverity.LOW
            elif 'channel' in error_str:
                return ErrorType.CHANNEL_NOT_FOUND, ErrorSeverity.LOW
            elif 'role' in error_str:
                return ErrorType.ROLE_NOT_FOUND, ErrorSeverity.LOW
        
        # Database errors
        if any(keyword in error_type_name for keyword in ['database', 'sql', 'connection']):
            return ErrorType.DATABASE_ERROR, ErrorSeverity.HIGH
        
        # API errors
        if any(keyword in error_str for keyword in ['api', 'http', 'request failed']):
            return ErrorType.API_ERROR, ErrorSeverity.MEDIUM
        
        # Rate limiting
        if any(keyword in error_str for keyword in ['rate limit', 'too many requests', 'cooldown']):
            return ErrorType.RATE_LIMITED, ErrorSeverity.LOW
        
        # Default to system error
        return ErrorType.SYSTEM_ERROR, ErrorSeverity.MEDIUM
    
    @classmethod
    def _get_user_friendly_message(cls, error: Exception, command_name: Optional[str] = None) -> str:
        """Generate user-friendly error message"""
        
        error_str = str(error).lower()
        
        if 'permission' in error_str:
            return f"You lack the noble privileges required to use the `{command_name}` command in this chamber of the manor."
        
        if 'not found' in error_str:
            return f"The requested entity has vanished into the manor's mysterious corridors. Please verify your request and try again."
        
        if 'invalid' in error_str:
            return f"Your parchment contains illegible script. Please review the `{command_name}` command syntax and try again."
        
        if 'rate limit' in error_str or 'cooldown' in error_str:
            return f"Victorian etiquette requires a more measured pace. Please wait before using `{command_name}` again."
        
        # Default message
        return f"The manor's systems encountered an unexpected complication while processing your `{command_name}` request."

# Global error handler instance
error_handler = VictorianErrorHandler()

# Decorator for automatic error handling
def handle_errors(func):
    """Decorator to automatically handle command errors"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            # Find interaction in arguments
            interaction = None
            for arg in args:
                if isinstance(arg, discord.Interaction):
                    interaction = arg
                    break
            
            if interaction:
                await error_handler.handle_command_error(
                    interaction, e, func.__name__
                )
            else:
                logger.error(f"Error in {func.__name__}: {e}")
                logger.error(traceback.format_exc())
    
    wrapper.__name__ = func.__name__
    wrapper.__annotations__ = func.__annotations__.copy()
    return wrapper