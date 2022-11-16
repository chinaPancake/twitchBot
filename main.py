from twitchio.ext import commands
from twitchio import Channel
from twitchio import User
import twitch_token

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_token.twitch_token(), prefix='?', initial_channels=['SitLetto'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'Usaer id is | {self.user_id}')

    # Printing hello {author.name} message
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello, {ctx.author.name}!')

    @commands.command()
    async def rulet(self, ctx: commands.Context):
        get_uusers = ctx.bot.get_channel('SitLetto')
        chatters_list = []
        for chatters in get_uusers.chatters:
            chatters_list.append(chatters.name)

        await ctx.send(f'List of users{chatters_list}')


bot = Bot()
bot.run()