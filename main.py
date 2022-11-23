import twitchio
from twitchio.ext import routines
from twitchio.ext import commands
from twitchio.ext import pubsub


from bs4 import BeautifulSoup
from lxml import etree
import requests

import asyncio
import twitch_token
import random

class Bot(commands.Bot):
    client = twitchio.Client(token=twitch_token.twitch_token())
    client.pubsub = pubsub.PubSubPool(client)

    URL = 'https://altermmo.pl'
    web_page = requests.get(URL)
    soup = BeautifulSoup(web_page.content, "html.parser")
    dom = etree.HTML(str(soup))

    def __init__(self):
        super().__init__(token=twitch_token.twitch_token(), prefix='?', initial_channels=['SitLetto'] )
    
    async def event_ready(self, ctx = commands.Context):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        #print(client.get_channel('SitLetto'))
        await self.test_routine.start()

    @routines.routine(seconds = 15.0)
    async def test_routine(self):
        chan = bot.get_channel("SitLetto")
        await chan.send(f'{self.dom.xpath("//*[@id]/div/div/a/@href")[0]}')
        

    async def event_message(self, message):
        if message.echo:
            return

        await self.handle_commands(message)

    
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
        # Append into chatters_list every chatters from chat.
        chatters_list = [chatters.name for chatters in get_uusers.chatters]
        
        # Get random chatters nickname and print it on stream
        await ctx.send(f'Random user is: {random.choice(chatters_list)}')
        return chatters_list

    @commands.command()
    async def ladneslowo(self, ctx: commands.Context):
       await ctx.send(f'{event_list}')
    
    @commands.command()
    async def komendy(self, ctx: commands.Context):
        await ctx.send('Dostępne komendy to, ?ladneslowo, ?rulet, ?hello, rekinodtylu')

bot = Bot() 
bot.run()
