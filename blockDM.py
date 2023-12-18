# █ ▀█▀ ▀█ █   ▄▀█ █▄█ ▀█
# █ ░█░ █▄ █▄▄ █▀█ ░█░ █▄
# https://t.me/itzlayz
                    
# 🔒 Licensed under the GNU AGPLv3
# https://www.gnu.org/licenses/agpl-3.0.html 

import discord
from discord.ext import commands

class BlockDM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.description = "Blocks DM spam"
        self.hello_message = f"🛡 **DM protection blocked you, please wait for owner**"

    @property
    def blocking(self):
        return self.bot.db.get("blockdm", "blocking", False)

    @blocking.setter
    def blocking(self, value: bool):
        self.bot.db.set("blockdm", "blocking", value)
    
    @commands.command()
    async def toggleBlock(self, ctx):
        self.blocking = not self.blocking
        action = '`enabled`' if self.blocking else '`disabled`'

        await ctx.reply(f"DM blocking is - {action}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not self.blocking:
            return
        
        if isinstance(message.channel, discord.DMChannel):
            if isinstance(message.author, discord.ClientUser):
                return
            
            if (
                message.author not in self.bot.friends and
                 message.author.id not in self.bot.db.get(
                    "blockdm", "blocked_users", [])
            ):
                await message.reply(self.hello_message)
                await message.author.block()

                self.bot.db.set(
                    "blockdm", 
                    "blocked_users", 
                    self.bot.db.get(
                        "blockdm", 
                        "blocked_users", []
                    ) + [message.author.id]
                )

async def setup(bot):
    await bot.add_cog(BlockDM(bot))