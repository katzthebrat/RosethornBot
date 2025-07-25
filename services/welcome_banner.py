"""
Animated Welcome Banner Service
Creates beautiful animated welcome banners for new Discord server members
"""

import os
import asyncio
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import discord
from datetime import datetime
import random

class WelcomeBannerService:
    def __init__(self):
        self.banner_templates = [
            "victorian_rose",
            "gothic_manor", 
            "elegant_throne",
            "mystical_garden"
        ]
        self.color_schemes = {
            "victorian_rose": {
                "primary": (113, 20, 23),    # Deep red #711417
                "secondary": (139, 69, 19),   # Saddle brown
                "accent": (218, 165, 32),     # Golden rod
                "text": (245, 245, 220)      # Beige
            },
            "gothic_manor": {
                "primary": (25, 25, 25),     # Dark charcoal
                "secondary": (113, 20, 23),  # Deep red
                "accent": (169, 169, 169),   # Dark gray
                "text": (245, 245, 245)     # Off white
            },
            "elegant_throne": {
                "primary": (72, 61, 139),    # Dark slate blue
                "secondary": (113, 20, 23),  # Deep red
                "accent": (218, 165, 32),    # Golden rod
                "text": (248, 248, 255)     # Ghost white
            },
            "mystical_garden": {
                "primary": (34, 139, 34),    # Forest green
                "secondary": (113, 20, 23),  # Deep red
                "accent": (255, 215, 0),     # Gold
                "text": (240, 248, 255)     # Alice blue
            }
        }

    async def create_welcome_banner(self, member: discord.Member, guild: discord.Guild) -> io.BytesIO:
        """Create an animated welcome banner for a new member"""
        
        # Select random template and colors
        template = random.choice(self.banner_templates)
        colors = self.color_schemes[template]
        
        # Create base banner
        width, height = 800, 300
        banner = Image.new('RGBA', (width, height), colors["primary"])
        draw = ImageDraw.Draw(banner)
        
        # Add Victorian decorative elements
        await self._add_decorative_elements(draw, width, height, colors, template)
        
        # Add member avatar
        try:
            avatar_bytes = await member.display_avatar.read()
            avatar = Image.open(io.BytesIO(avatar_bytes))
            avatar = await self._process_avatar(avatar, colors)
            banner.paste(avatar, (50, 75), avatar)
        except Exception:
            # Fallback: draw a placeholder circle
            draw.ellipse([50, 75, 200, 225], fill=colors["accent"], outline=colors["text"], width=3)
            draw.text((125, 150), "👤", fill=colors["text"], anchor="mm")
        
        # Add welcome text
        await self._add_welcome_text(draw, member, guild, colors, width, height)
        
        # Add Victorian flourishes
        await self._add_flourishes(draw, width, height, colors)
        
        # Convert to bytes
        banner_bytes = io.BytesIO()
        banner.save(banner_bytes, format='PNG', quality=95)
        banner_bytes.seek(0)
        
        return banner_bytes

    async def _add_decorative_elements(self, draw, width, height, colors, template):
        """Add template-specific decorative elements"""
        
        if template == "victorian_rose":
            # Rose border pattern
            for i in range(0, width, 40):
                draw.ellipse([i-5, 10, i+5, 20], fill=colors["accent"])
                draw.ellipse([i-5, height-20, i+5, height-10], fill=colors["accent"])
            
            # Corner roses
            draw.ellipse([10, 10, 30, 30], fill=colors["secondary"])
            draw.ellipse([width-30, 10, width-10, 30], fill=colors["secondary"])
            draw.ellipse([10, height-30, 30, height-10], fill=colors["secondary"])
            draw.ellipse([width-30, height-30, width-10, height-10], fill=colors["secondary"])
            
        elif template == "gothic_manor":
            # Gothic arch patterns
            for x in range(0, width, 100):
                draw.arc([x, 0, x+50, 50], 0, 180, fill=colors["accent"], width=2)
                draw.arc([x, height-50, x+50, height], 180, 360, fill=colors["accent"], width=2)
            
        elif template == "elegant_throne":
            # Throne-like geometric patterns
            for i in range(3):
                y = 50 + i * 70
                draw.rectangle([0, y, 20, y+20], fill=colors["accent"])
                draw.rectangle([width-20, y, width, y+20], fill=colors["accent"])
            
        elif template == "mystical_garden":
            # Garden vine patterns
            for i in range(0, width, 60):
                draw.arc([i, 0, i+30, 30], 0, 180, fill=colors["accent"], width=3)
                draw.arc([i+15, height-30, i+45, height], 180, 360, fill=colors["accent"], width=3)

    async def _process_avatar(self, avatar, colors):
        """Process member avatar with Victorian styling"""
        # Resize and make circular
        avatar = avatar.resize((150, 150))
        mask = Image.new('L', (150, 150), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, 150, 150], fill=255)
        
        # Apply mask
        avatar_rgba = avatar.convert('RGBA')
        avatar_rgba.putalpha(mask)
        
        # Add decorative border
        border = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse([0, 0, 160, 160], outline=colors["accent"], width=5)
        border_draw.ellipse([3, 3, 157, 157], outline=colors["text"], width=2)
        
        # Combine avatar with border
        final_avatar = Image.new('RGBA', (160, 160), (0, 0, 0, 0))
        final_avatar.paste(border, (0, 0))
        final_avatar.paste(avatar_rgba, (5, 5), avatar_rgba)
        
        return final_avatar

    async def _add_welcome_text(self, draw, member, guild, colors, width, height):
        """Add welcome text with Victorian styling"""
        try:
            # Try to load a nice font (fallback to default if not available)
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 36)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 24)
            info_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        # Welcome message
        welcome_text = "Welcome to the Manor!"
        text_x = 250
        draw.text((text_x, 80), welcome_text, fill=colors["text"], font=title_font)
        
        # Member name with Victorian titles
        titles = ["Lady", "Lord", "Sir", "Dame", "Noble"]
        title = random.choice(titles)
        member_text = f"{title} {member.display_name}"
        draw.text((text_x, 130), member_text, fill=colors["accent"], font=subtitle_font)
        
        # Server info
        server_text = f"Joining {guild.name}"
        draw.text((text_x, 170), server_text, fill=colors["text"], font=info_font)
        
        # Member count
        count_text = f"Member #{guild.member_count}"
        draw.text((text_x, 200), count_text, fill=colors["accent"], font=info_font)
        
        # Date
        date_text = datetime.now().strftime("%B %d, %Y")
        draw.text((text_x, 230), date_text, fill=colors["text"], font=info_font)

    async def _add_flourishes(self, draw, width, height, colors):
        """Add Victorian decorative flourishes"""
        
        # Corner flourishes
        flourish_points = [
            # Top left flourish
            [(0, 40), (20, 20), (40, 0)],
            # Top right flourish  
            [(width, 40), (width-20, 20), (width-40, 0)],
            # Bottom left flourish
            [(0, height-40), (20, height-20), (40, height)],
            # Bottom right flourish
            [(width, height-40), (width-20, height-20), (width-40, height)]
        ]
        
        for points in flourish_points:
            draw.polygon(points, fill=colors["accent"])
        
        # Central decorative line
        center_y = height // 2
        for i in range(220, width-50, 20):
            draw.ellipse([i-2, center_y-2, i+2, center_y+2], fill=colors["accent"])

    async def create_animated_embed(self, member: discord.Member, guild: discord.Guild) -> discord.Embed:
        """Create an animated embed to accompany the banner"""
        
        embed = discord.Embed(
            title="🌹 A Distinguished Guest Arrives! 🌹",
            description=f"The manor doors open to welcome **{member.display_name}**",
            color=0x711417,
            timestamp=datetime.now()
        )
        
        # Victorian welcome messages
        welcome_messages = [
            f"Hark! {member.mention} has graced our Victorian manor with their presence!",
            f"Behold! A new soul enters our Gothic sanctuary - {member.mention}!",
            f"The roses bloom brighter as {member.mention} joins our elegant assembly!",
            f"By candlelight and moonbeam, {member.mention} arrives at our manor!",
            f"A distinguished guest crosses our threshold - welcome {member.mention}!"
        ]
        
        embed.add_field(
            name="🎭 Grand Entrance",
            value=random.choice(welcome_messages),
            inline=False
        )
        
        embed.add_field(
            name="🏰 Manor Statistics",
            value=f"👥 Total Residents: **{guild.member_count}**\n📅 Joined: {discord.utils.format_dt(member.joined_at, 'R')}\n🌹 Member Number: **#{guild.member_count}**",
            inline=True
        )
        
        embed.add_field(
            name="🗝️ Getting Started",
            value="• Use `/rules` to review manor etiquette\n• Try `/tutorial` for a guided tour\n• Visit `/balance` to check your Rosebuds\n• Create `/tickets` if you need assistance",
            inline=True
        )
        
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="Welcome to Rosewood Manor • May your stay be filled with Victorian elegance",
            icon_url=guild.icon.url if guild.icon else None
        )
        
        return embed

# Global service instance
welcome_banner_service = WelcomeBannerService()