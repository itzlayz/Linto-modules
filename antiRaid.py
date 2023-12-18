# █ ▀█▀ ▀█ █   ▄▀█ █▄█ ▀█
# █ ░█░ █▄ █▄▄ █▀█ ░█░ █▄
# https://t.me/itzlayz
                    
# 🔒 Licensed under the GNU AGPLv3
# https://www.gnu.org/licenses/agpl-3.0.html 

import asyncio
import random

from discord.ext import commands

class GuildAntiRaid(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.description = "Helps remove the consequences of a raid"

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
    async def deleteChannels(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_channels"):
            return await ctx.reply("```\n- No manage_channels permission\n```")
    
        for channel in filter(lambda x: x.name == name, ctx.guild.channels):
            if not channel:
                continue

            await self.acc_protect()
            await channel.delete()
        
        msg = await ctx.reply("Successful...")
        await asyncio.sleep(1)
        await msg.delete()
    
    @commands.command()
    async def deleteRoles(self, ctx: commands.Context, name: str):
        if not self.check_permissions(ctx, "manage_roles"):
            return await ctx.reply("```diff\n- No manage_roles permission\n```")
    
        for role in filter(lambda x: x.name == name, ctx.guild.roles):
            if not role:
                continue

            await self.acc_protect()
            await role.delete()
        
        msg = await ctx.reply("Successful...")
        await asyncio.sleep(1)
        await msg.delete()
    
async def setup(bot):
    await bot.add_cog(GuildAntiRaid(bot))