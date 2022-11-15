from twitchio.ext import commands
import twitch_token

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_token.twitch_token(), prefix='?', initial_channels=['SitLetto'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'Usaer id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello, {ctx.author.name}!')

bot = Bot()
bot.run()