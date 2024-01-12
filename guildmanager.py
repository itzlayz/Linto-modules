# █ ▀█▀ ▀█ █   ▄▀█ █▄█ ▀█
# █ ░█░ █▄ █▄▄ █▀█ ░█░ █▄
# https://t.me/itzlayz
                    
# 🔒 Licensed under the GNU AGPLv3
# https://www.gnu.org/licenses/agpl-3.0.html 

import asyncio
import random

import discord
from discord.ext import commands

class GuildManager(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.deleting_channels = []
        self.deleting_roles = []

        self.description = "Help work with guilds"

    def check_permissions(self, ctx, perm: str):
        perms = ctx.guild.get_member(ctx.author.id).guild_permissions

        return getattr(
            perms,
            perm, 
            getattr(
                perms,
                "administrator",
                False
            )
        )
    
    async def acc_protect(self):
        await asyncio.sleep(random.uniform(0.01, 0.25))

    @commands.command()
    async def permclear(self, ctx):
        await ctx.send('ﾠﾠ' + '\n' * 400 + 'ﾠﾠ')

    @commands.command()
    async def deleteChannels(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_channels"):
            return await ctx.reply("```diff\n- No manage_channels permission\n```")

        if ctx.guild.id in self.deleting_channels:
            return await ctx.reply("```diff\n- Proccess still deleting channels\n```")
        
        self.deleting_channels.append(ctx.guild.id)
        for channel in filter(lambda x: x.name == name, ctx.guild.channels):
            if not channel:
                continue

            if channel.id == ctx.channel.id:
                continue

            await self.acc_protect()
            await channel.delete()

        self.deleting_channels = list(filter(lambda guild: guild.id != ctx.guild.id))

        msg = await ctx.reply("Successful...")
        await asyncio.sleep(1)
        await msg.delete()
    
    @commands.command()
    async def deleteRoles(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_roles"):
            return await ctx.reply("```diff\n- No manage_roles permission\n```")
        
        if ctx.guild.id in self.deleting_channels:
            return await ctx.reply("```diff\n- Proccess still deleting roles\n```")
    
        self.deleting_roles.append(ctx.guild.id)
        for role in filter(lambda x: x.name == name, ctx.guild.roles):
            if not role:
                continue

            await self.acc_protect()
            await role.delete()
        
        self.deleting_roles = list(filter(lambda guild: guild.id != ctx.guild.id))

        msg = await ctx.reply("Successful...")
        await asyncio.sleep(1)
        await msg.delete()

    @commands.command(aliases=["renamechannel", "rnchannel"])
    async def rename_channel(self, ctx, name: str):
        if not self.check_permissions(ctx, "manage_channels"):
            return await ctx.reply("```diff\n- No manage_channels permission\n```")
        
        channel: discord.TextChannel = ctx.channel
        await channel.edit(name=name)
    
    @commands.command(aliases=["renamecategory", "rncategory"])
    async def rename_category(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_guild"):
            return await ctx.reply("```diff\n- No manage_guild permission\n```")
        
        category: discord.CategoryChannel = ctx.channel.category
        await category.edit(name=name)
    
    @commands.command(aliases=["createchannel", "newchannel"])
    async def create_channel(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_channels"):
            return await ctx.reply("```diff\n- No manage_channels permission\n```")
        
        guild: discord.guild.Guild = ctx.guild
        await guild.create_text_channel(name)
    
    @commands.command(aliases=["createvoice", "newvoice"])
    async def create_voice(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_channels"):
            return await ctx.reply("```diff\n- No manage_channels permission\n```")
        
        guild: discord.guild.Guild = ctx.guild
        await guild.create_voice_channel(name)