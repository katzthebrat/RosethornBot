import discord
import logging

class AgreeButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="I Agree", style=discord.ButtonStyle.success, custom_id="agree_button")
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        role_id = 1394518008570970172
        log_channel_id = 1394382797019418676

        role = interaction.guild.get_role(role_id)
        log_channel = interaction.guild.get_channel(log_channel_id)

        if role is None:
            logging.warning(f"Role ID {role_id} not found in guild {interaction.guild.name}")
            await interaction.response.send_message("⚠️ Role not found. Please contact an admin.", ephemeral=True)
            return

        try:
            await interaction.user.add_roles(role)
            logging.info(f"Assigned role '{role.name}' to {interaction.user}")
            await interaction.response.send_message(f"✅ You’ve been given the **{role.name}** role!", ephemeral=True)

            if log_channel:
                embed = discord.Embed(
                    title="📜 Member Agreed to Rules",
                    description=f"{interaction.user.mention} clicked **I Agree** and received the **{role.name}** role.",
                    color=discord.Color.green(),
                    timestamp=interaction.created_at
                )
                embed.set_footer(text="Rosethorn Bot | Role Assignment")
                embed.set_thumbnail(url=interaction.user.display_avatar.url)
                await log_channel.send(embed=embed)

        except Exception as e:
            logging.error(f"Failed to assign role: {e}", exc_info=True)
            await interaction.response.send_message("⚠️ Something went wrong while assigning your role.", ephemeral=True)

async def send_rules(interaction: discord.Interaction):
    try:
        await interaction.response.defer()
        logging.info(f"/rules command triggered by {interaction.user}")

        embed = discord.Embed(
            title="Rosethorn Realm Rules",
            description="Please follow these guidelines to keep our community kind, creative, and cozy.",
            color=discord.Color.from_rgb(113, 20, 23)
        )

        rules = [
            ("1. Building Restrictions", "Do NOT build within 1000 blocks of spawn. If visible from spawn, you’ll be asked to move."),
            ("2. No Stealing or Griefing", "Absolutely not tolerated. Violators will be banned — no second chances."),
            ("3. No Spamming", "Limit excessive messaging. Keep in mind that members may be in different time zones."),
            ("4. Respect Messaging Boundaries", "Do NOT DM without consent. Use <#1325432475387957288>. No admin DMs about tickets."),
            ("5. Respect Personal Space", "Don’t build too close or enter builds without permission. Use land claims to protect your base."),
            ("6. Auto Farms Regulations", "Must be admin-approved, community-use only, and have manual switches."),
            ("7. Zero Tolerance for Harassment", "Discrimination, witch-hunting, racism, sexism, and hate speech = instant ban."),
            ("8. Keep Chats Organized", "Use correct channels. Overwhelming threads may be moved for clarity."),
            ("9. Member Mode Requirements", "✔ Add gamertag to <#1315011793940119593>\n✔ Agree to rules\n✔ DM 'Thorn' to <@1349062201385684992>."),
            ("10. Realm Code Sharing", "Requires admin approval. New members must confirm rule agreement before joining."),
            ("11. Admin Requests", "Admins only provide basic blocks. Use community shops for other materials."),
            ("12. Ticket System", "You have 12 hours to respond to tickets. No admin DMs. Multiple open tickets = ban."),
        ]

        for name, value in rules:
            embed.add_field(name=name, value=value, inline=False)

        embed.set_footer(text="Rosethorn Bot | Violations may trigger a ticket for review")

        await interaction.channel.send(embed=embed, view=AgreeButton())
        logging.info("Rules embed sent successfully")

    except Exception as e:
        logging.error(f"Failed to send rules embed: {e}", exc_info=True)
