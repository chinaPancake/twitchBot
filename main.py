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
    client = twitchio.Client(token=twitch_token.bot_twitch_access_token())
    client.pubsub = pubsub.PubSubPool(client)

    # Get leatest post, form url
    URL = "https://altermmo.pl"
    web_page = requests.get(URL)
    soup = BeautifulSoup(web_page.content, "html.parser")
    dom = etree.HTML(str(soup))

    def __init__(self):
        super().__init__(
            token=twitch_token.bot_twitch_access_token(),
            prefix="?",
            initial_channels=["SitLetto"],
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")
        # start test_routine function
        await self.test_routine.start()

    # Send message into channel every x seconds / minutes
    @routines.routine(seconds=60.0)
    async def test_routine(self):
        chan = bot.get_channel("SitLetto")
        await chan.send(f'{self.dom.xpath("//*[@id]/div/div/a/@href")[0]}')

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    @client.event()
    async def main(self):
        # channel token from brodcast channel
        user_id = twitch_token.user_client_id
        user_oauth_token = twitch_token.user_oauth_token()
        user_twitch_token = twitch_token.user_twitch_token()
        bot_oauth_token = twitch_token.bot_oauth_token()
        bot_twitch_token = twitch_token.bot_twitch_token()

        topic = [
            pubsub.channel_points(user_oauth_token)[user_id],
            pubsub.bits(user_oauth_token)[user_id],
        ]
        await client.pubsub.subscribe_topics(topic)
        await client.start()

    @client.event()
    async def event_pubsub_channel_points(
        self, event: pubsub.PubSubChannelPointsMessage
    ):
        print("get-event")

    # Printing hello {author.name} message
    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello, {ctx.author.name}!")

    # Get random user from chat, and print his/her name
    @commands.command()
    async def rulet(self, ctx: commands.Context):
        get_uusers = ctx.bot.get_channel("SitLetto")
        # Append into chatters_list every chatters from chat.
        chatters_list = [chatters.name for chatters in get_uusers.chatters]

        # Get random chatters nickname and print it on stream
        await ctx.send(f"Random user is: {random.choice(chatters_list)}")
        return chatters_list

    # print nice quote about females
    @commands.command()
    async def ladneslowo(self, ctx: commands.Context):
        await ctx.send(
            f"tutaj będzie lista ładnych słów, ale póki co jest tylko rekinodtylu "
        )

    # get all bot commends
    @commands.command()
    async def komendy(self, ctx: commands.Context):
        await ctx.send("Dostępne komendy to, ?ladneslowo, ?rulet, ?hello, rekinodtylu")


# PODCAST HERE


bot = Bot()
bot.client.loop.run_until_complete(bot.main())
bot.run()
