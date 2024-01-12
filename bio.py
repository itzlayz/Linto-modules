import discord
from discord.ext import commands

class Biomanager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Manages your user's biography"

    @commands.command(aliases=["change_bio", "changebio"])
    async def editbio(self, ctx, *, bio: str = ""):
        color = self.bot.user.accent_color
        if not bio:
            await self.bot.edit_bio(
                banner_color=color,
                bio=""
            )
            return await ctx.reply(
                "✔ **Successfuly cleared bio**"
            )

        await self.bot.edit_bio(bio=bio)
        await ctx.reply("✔ **Successfuly changed bio**")
    
    @commands.command(aliases=["change_banner", "changebanner"])
    async def editbanner(self, ctx, color: int = 0):
        bio = self.bot.user.bio
        if not color:
            await self.bot.edit_bio(
                bio=bio,
                banner_color=0
            )
            return await ctx.reply(
                "✔ **Successfuly cleared banner_color**"
            )
        
        await self.bot.edit_bio(bio=bio, banner_color=color)
        await ctx.reply("✔ **Successfuly changed banner_color**")
    
    @commands.command(aliases=["scrap_bio", "scrapbio"])
    async def copybio(self, ctx, *, user: discord.User):
        bio = user.bio
        color = self.bot.user.accent_color

        await self.bot.edit_bio(bio=bio, banner_color=color)
        await ctx.reply("✔ **Successfuly copied bio**")
    
    @commands.command(aliases=["scrap_banner", "scrapbanner"])
    async def copybanner(self, ctx, user: discord.User):
        bio = self.bot.user.bio
        color = user.accent_color

        await self.bot.edit_bio(bio=bio, banner_color=color)
        await ctx.reply("✔ **Successfuly copied banner_color**")