"""
Phebe
A discord bot for the Python Experts Server
"""
import disnake
from disnake.ext import commands

import logging, sys

l = logging.getLogger("disnake.client")
l.setLevel(logging.INFO)
logging.root.setLevel(logging.INFO)
# logging.root.addHandler(logging.StreamHandler(sys.stderr))

from pathlib import Path
import os
import random
from threading import Thread
import asyncio
import StayAlive
from colorama import Fore


class Phebe(commands.Cog):
    """
    Official bot for the Pythonic Hangout server
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """show message when bot gets online"""
        print(Fore.BLUE +
              f'[+] Bot is running! \n[+] Ping: {self.bot.latency*1000} ms')
        self.bot.loop.create_task(self.status_task())

    async def status_task(self):
        while True:
            for activity in (disnake.Game(name=".help"),
                             disnake.Activity(type=disnake.ActivityType.watching,
                                              name="Members in Servers"),
                             disnake.Activity(type=disnake.ActivityType.listening,
                                              name="Moderation team command.")
                                              ):
                await self.bot.change_presence(activity=activity)
                await asyncio.sleep(10)

    @commands.command()
    async def ping(self, ctx):
        """Show latency in mili seconds"""
        await ctx.send(embed=disnake.Embed(
            title='Pong!',
            description=f"🕑 **Latency: **{round(self.bot.latency*1000, 3)} ms")
                       )

    @commands.command()
    async def warn(self, ctx, member: disnake.Member):
        """Warn a User"""
        await ctx.send(f"{member: disnake.Member} has been warned")

    @commands.command()
    async def timeout(self, ctx, time, member: disnake.Member = None):
        """Timeout a User"""
        await member.timeout(duration=time)

    # meeting command
    # @commands.command()
    # @commands.has_role("Moderation Team")
    # async def meeting(self, ctx: commands.Context, *topic: str):
    #     """Call a Moderation Team Meeting"""
    #     channel = self.bot.get_channel(927262021496471563)
    #     embed = disnake.Embed(
    #         title='Moderator Team Meeting')
    #     if topic:
    #         embed.add_field(name="topic", value=' '.join(topic))
    #     embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

    #     await channel.send("<@&927259243302776912>", embed=embed)

    @commands.command()
    async def pfp(self, ctx, member: disnake.Member = None):
        """Show profile picture of a user, or see yours"""

        embed = disnake.Embed(
            title=
            f'Profile Picture of {ctx.author.display_name if member is None else member.display_name}'
        )

        embed.set_image(
            url=ctx.author.avatar if member is None else member.avatar)
        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx):
        """Flip a vertual coin and get the result"""
        heads_url = "https://cdn-icons.flaticon.com/png/512/5700/premium/5700963.png?token=exp=1643128433~hmac=831aba311ab86e1ef73059e55178e712"
        tails_url = "https://cdn-icons.flaticon.com/png/512/2173/premium/2173470.png?token=exp=1643127144~hmac=a622b3080fe202709c7745ac894df97b"

        res = random.randint(1, 2)

        embed = disnake.Embed(
            title=f'Flipped a coin',
            description=f"**{('Heads' if res == 1 else 'Tails')}**")
        embed.set_thumbnail(heads_url if res == 1 else tails_url)

        await ctx.reply(embed=embed)
    
    @commands.command()
    async def format(self, ctx):
        await ctx.send(embed=disnake.Embed(title='Code formatting',
                                           description="""
		To properly format Python code in Discord, write your code like this:

\\`\\`\\`py
print("Hello world")\n\\`\\`\\`\n\n    **These are backticks, not quotes**. They are often under the Escape (esc) key on most keyboard orientations, they could be towards the right side of the keyboard if you are using eastern european/balkan language keyboards.
"""))


async def runserver():
    while True:
        StayAlive.start_server()
        await asyncio.sleep(8000)
        break


if __name__ == "__main__":
    intents = disnake.Intents.none()
    intents.messages = True
    intents.guilds = True
    intents.members = True
    try:
        intents.presences = True
        bot: commands.Bot = commands.Bot(
            command_prefix=".",
            description=Phebe.__doc__,
            intents=intents,
        )
    except:
        intents.presences = False
        bot: commands.Bot = commands.Bot(
            command_prefix=".",
            description=Phebe.__doc__,
            intents=intents,
        )
    bot.add_cog(Phebe(bot))
    dir: Path = Path("commands")
    for item in dir.iterdir():
        if item.name.endswith(".py"):
            name = f'{item.parent.name}.{item.stem}'
            print(f"Loading extension: {name}")
            bot.load_extension(name)

    t = Thread(target=StayAlive.start_server)
    t.start()

    while True:
        try:
            bot.run(
                os.getenv("Token")
                or __import__("dotenv").get_key(dotenv_path=".env",
                                                key_to_get="Token"))
        except disnake.errors.HTTPException:
            import traceback, sys, os
            traceback.print_exc(999, sys.stderr, True)
            import threading
            try:
                threading.shutdown()
            finally:
                os._exit(255)
