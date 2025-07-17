import discord
import logging

WELCOME_CHANNEL_ID = 1325102526143664148  # 🌸 Your desired welcome channel

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
            await interaction.response.send_message("📬 Welcome instructions sent to your DMs!", ephemeral=True)

        except Exception as e:
            logging.error(f"Failed to send welcome DM: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ Couldn’t send DM. Do you have messages from server members disabled?", ephemeral=True)

async def send_welcome_embed(interaction: discord.Interaction):
    logging.info(f"/welcome command triggered by {interaction.user}")

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
    embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else discord.Embed.Empty)
    embed.set_footer(text="Rosethorn Bot | Let the magic begin ✨")

    channel = interaction.guild.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(embed=embed, view=WelcomeButton())
        await interaction.response.send_message("✅ Welcome message posted.", ephemeral=True)
        logging.info("Welcome embed sent to channel")
    else:
        await interaction.response.send_message("⚠️ Welcome channel not found.", ephemeral=True)
        logging.warning("Could not find welcome channel")

