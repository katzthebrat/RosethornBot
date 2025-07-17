import discord
import logging
from discord.ext import commands

WELCOME_CHANNEL_ID = 1311536156009037945       # 🌸 Welcome Channel
LOG_CHANNEL_ID = 1327959433464123466           # 🗂️ Message Log Channel

class WelcomeButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Get Started", style=discord.ButtonStyle.success, custom_id="welcome_dm_button")
    async def send_dm(self, interaction: discord.Interaction, button: discord.ui.Button):
        logging.info(f"'Get Started' clicked by {interaction.user}")

        try:
            dm_embed = discord.Embed(
                title="🌟 Welcome to Rosethorn!",
                description="Here’s everything you need to start your journey:",
                color=discord.Color.green()
            )
            dm_embed.add_field(
                name="✅ Step 1",
                value="Read the rules with `/rules` and click the green 'I Agree' button.",
                inline=False
            )
            dm_embed.add_field(
                name="📝 Step 2",
                value="Add your gamertag to <#1315011793940119593> so admins can whitelist you.",
                inline=False
            )
            dm_embed.add_field(
                name="📌 Step 3",
                value="DM 'Thorn' to <@1349062201385684992> once you've completed the above.",
                inline=False
            )
            dm_embed.set_footer(text="Rosethorn Bot | Cozy begins here ✨")

            await interaction.user.send(embed=dm_embed)
            await interaction.followup.send("📬 Welcome instructions sent to your DMs!", ephemeral=True)

        except Exception as e:
            logging.error(f"Failed to send welcome DM: {e}", exc_info=True)
            await interaction.followup.send(
                "⚠️ Couldn’t send DM. Do you have messages from server members disabled?",
                ephemeral=True
            )

async def setup_events(bot):
    @bot.event
    async def on_member_join(member: discord.Member):
        logging.info(f"🪄 New member joined: {member.name}#{member.discriminator} (ID: {member.id})")

        embed = discord.Embed(
            title="🌸 Welcome to Rosethorn!",
            description="This server is built around kindness, creativity, and cozy vibes.",
            color=discord.Color.from_rgb(113, 20, 23)
        )
        embed.add_field(
            name="📜 Getting Started",
            value="Read the rules, agree, and add your gamertag. If you're not sure what to do next, click the button below.",
            inline=False
        )
        embed.set_thumbnail(url=member.guild.icon.url if member.guild.icon else discord.Embed.Empty)
        embed.set_footer(text="Rosethorn Bot | Let the magic begin ✨")

        channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(embed=embed, view=WelcomeButton())
            logging.info(f"Welcome embed sent to {channel.name} for {member.name}")
        else:
            logging.warning(f"❌ Welcome channel ID {WELCOME_CHANNEL_ID} not found in guild {member.guild.name}")

    @bot.event
    async def on_message_edit(before: discord.Message, after: discord.Message):
        if before.author.bot or before.content == after.content:
            return

        log_channel = before.guild.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return

        embed = discord.Embed(
            title="✏️ Message Edited",
            description=f"**Author:** {before.author.mention}\n**Channel:** {before.channel.mention}",
            color=discord.Color.orange()
        )
        embed.add_field(name="Before", value=before.content or "*No content*", inline=False)
        embed.add_field(name="After", value=after.content or "*No content*", inline=False)
        embed.set_footer(text=f"Message ID: {before.id}")
        embed.timestamp = discord.utils.utcnow()

        await log_channel.send(embed=embed)

    @bot.event
    async def on_message_delete(message: discord.Message):
        if message.author.bot:
            return

        log_channel = message.guild.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=f"**Author:** {message.author.mention}\n**Channel:** {message.channel.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Content", value=message.content or "*No content*", inline=False)
        embed.set_footer(text=f"Message ID: {message.id}")
        embed.timestamp = discord.utils.utcnow()

        await log_channel.send(embed=embed)
