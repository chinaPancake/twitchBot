import twitchio
from twitchio.ext import commands
from twitchio.ext import pubsub

import twitch_token
import random

class Bot(commands.Bot):
    client = twitchio.Client(token=twitch_token.twitch_token())
    client.pubsub = pubsub.PubSubPool(client)
    def __init__(self):
        super().__init__(token=twitch_token.twitch_token(), prefix='?', initial_channels=['SitLetto'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        event_points = pubsub.PubSubChannelPointsMessage
        event_list = []
        event_list.append(event_points.input)
        return event_list

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

        await ctx.send(f'Random user is: {random.choice(chatters_list)}')

        return chatters_list

    @commands.command()
    async def ladneslowo(self, ctx: commands.Context):
        await ctx.send(f'{event_list}')

bot = Bot()
bot.run()