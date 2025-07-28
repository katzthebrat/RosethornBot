"""
Sticky Message Service for RosethornBot
Automatically resends messages to keep them at the bottom of channels
"""

import discord
import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional
import json

logger = logging.getLogger(__name__)

class StickyMessageService:
    """Service to manage sticky messages that automatically resend to stay at bottom"""
    
    def __init__(self, bot):
        self.bot = bot
        self.sticky_messages: Dict[int, Dict] = {}  # channel_id -> sticky_config
        self.message_counts: Dict[int, int] = {}    # channel_id -> message_count
        self.resend_threshold = 3  # Resend after 3 messages
        
    def add_sticky_message(self, channel_id: int, content: str, embed_data: dict, created_by: int):
        """Add a sticky message to a channel"""
        self.sticky_messages[channel_id] = {
            'content': content,
            'embed_data': embed_data,
            'created_by': created_by,
            'created_at': datetime.now(),
            'last_message_id': None,
            'active': True
        }
        self.message_counts[channel_id] = 0
        logger.info(f"Added sticky message to channel {channel_id}")
    
    def remove_sticky_message(self, channel_id: int):
        """Remove sticky message from a channel"""
        if channel_id in self.sticky_messages:
            del self.sticky_messages[channel_id]
        if channel_id in self.message_counts:
            del self.message_counts[channel_id]
        logger.info(f"Removed sticky message from channel {channel_id}")
    
    async def on_message(self, message: discord.Message):
        """Handle new messages and resend sticky if needed"""
        if message.author.bot:
            return
            
        channel_id = message.channel.id
        
        if channel_id not in self.sticky_messages:
            return
            
        if not self.sticky_messages[channel_id]['active']:
            return
        
        # Increment message count
        self.message_counts[channel_id] = self.message_counts.get(channel_id, 0) + 1
        
        # Check if we need to resend sticky
        if self.message_counts[channel_id] >= self.resend_threshold:
            await self._resend_sticky_message(message.channel)
            self.message_counts[channel_id] = 0
    
    async def _resend_sticky_message(self, channel: discord.TextChannel):
        """Resend the sticky message"""
        channel_id = channel.id
        sticky_config = self.sticky_messages.get(channel_id)
        
        if not sticky_config:
            return
        
        try:
            # Delete the previous sticky message if it exists
            if sticky_config['last_message_id']:
                try:
                    old_message = await channel.fetch_message(sticky_config['last_message_id'])
                    await old_message.delete()
                except (discord.NotFound, discord.Forbidden):
                    pass  # Message already deleted or no permission
            
            # Create new embed from stored data
            embed_data = sticky_config['embed_data']
            embed = discord.Embed(
                title=embed_data.get('title', '📌 Manor Notice'),
                description=embed_data.get('description', sticky_config['content']),
                color=embed_data.get('color', 0x711417)
            )
            
            # No fields to add - keeping it simple with just title and description
            
            # Send new sticky message
            new_message = await channel.send(embed=embed)
            sticky_config['last_message_id'] = new_message.id
            
            logger.info(f"Resent sticky message in channel {channel_id}")
            
        except Exception as e:
            logger.error(f"Error resending sticky message in channel {channel_id}: {e}")
    
    async def manual_resend(self, channel: discord.TextChannel) -> bool:
        """Manually resend sticky message"""
        try:
            await self._resend_sticky_message(channel)
            return True
        except Exception as e:
            logger.error(f"Error manually resending sticky message: {e}")
            return False
    
    def get_sticky_info(self, channel_id: int) -> Optional[Dict]:
        """Get sticky message info for a channel"""
        return self.sticky_messages.get(channel_id)
    
    def is_sticky_active(self, channel_id: int) -> bool:
        """Check if channel has an active sticky message"""
        return (channel_id in self.sticky_messages and 
                self.sticky_messages[channel_id]['active'])
    
    def toggle_sticky(self, channel_id: int) -> bool:
        """Toggle sticky message active state"""
        if channel_id in self.sticky_messages:
            current_state = self.sticky_messages[channel_id]['active']
            self.sticky_messages[channel_id]['active'] = not current_state
            return not current_state
        return False
    
    def get_all_sticky_channels(self) -> list:
        """Get all channels with sticky messages"""
        return [
            {
                'channel_id': channel_id,
                'config': config
            }
            for channel_id, config in self.sticky_messages.items()
        ]

# Global instance
sticky_service = None

def initialize_sticky_service(bot):
    """Initialize the sticky service with bot instance"""
    global sticky_service
    sticky_service = StickyMessageService(bot)
    return sticky_service