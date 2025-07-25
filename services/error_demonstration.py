"""
Error Demonstration Commands for RosethornBot
Commands to showcase the elegant error message design system
"""

import discord
from discord.ext import commands
from services.error_handler import handle_errors, ErrorType, ErrorSeverity
from services.error_templates import templates as error_templates
import random

class ErrorDemonstrationCommands:
    """Commands to demonstrate the error handling system"""
    
    @staticmethod
    @handle_errors
    async def demo_permission_error(interaction: discord.Interaction):
        """Demonstrate permission denied error"""
        embed = error_templates.permission_denied(
            user=interaction.user,
            required_permission="manage_guild",
            channel_name=interaction.channel.name
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_user_not_found(interaction: discord.Interaction, username: str):
        """Demonstrate user not found error"""
        embed = error_templates.user_not_found(username)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_invalid_input(interaction: discord.Interaction, command_name: str):
        """Demonstrate invalid input error"""
        embed = error_templates.invalid_input(
            command_name=command_name,
            expected_format=f"/{command_name} <required_param> [optional_param]"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_database_error(interaction: discord.Interaction):
        """Demonstrate database error"""
        embed = error_templates.database_error("user balance retrieval")
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_rate_limited(interaction: discord.Interaction):
        """Demonstrate rate limit error"""
        embed = error_templates.rate_limited(
            cooldown_seconds=30,
            command_name="daily"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_insufficient_funds(interaction: discord.Interaction):
        """Demonstrate insufficient funds error"""
        embed = error_templates.insufficient_funds(
            current_balance=150,
            required_amount=500
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_maintenance_mode(interaction: discord.Interaction):
        """Demonstrate maintenance mode error"""
        embed = error_templates.maintenance_mode()
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @staticmethod
    @handle_errors
    async def demo_random_error(interaction: discord.Interaction):
        """Demonstrate a random error type"""
        error_types = [
            "permission_denied",
            "user_not_found", 
            "invalid_input",
            "database_error",
            "rate_limited",
            "insufficient_funds",
            "maintenance_mode"
        ]
        
        selected_error = random.choice(error_types)
        
        if selected_error == "permission_denied":
            embed = error_templates.permission_denied(
                user=interaction.user,
                required_permission="administrator",
                channel_name=interaction.channel.name
            )
        elif selected_error == "user_not_found":
            embed = error_templates.user_not_found("MysteriousGuest#1234")
        elif selected_error == "invalid_input":
            embed = error_templates.invalid_input("balance", "/balance [user]")
        elif selected_error == "database_error":
            embed = error_templates.database_error("transaction processing")
        elif selected_error == "rate_limited":
            embed = error_templates.rate_limited(45, "work")
        elif selected_error == "insufficient_funds":
            embed = error_templates.insufficient_funds(75, 200)
        else:  # maintenance_mode
            embed = error_templates.maintenance_mode()
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Export the class for easy import
error_demo = ErrorDemonstrationCommands()