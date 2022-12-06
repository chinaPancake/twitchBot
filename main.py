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
import sqlite3


class Bot(commands.Bot):
    global client

    client = twitchio.Client(token=twitch_token.bot_twitch_access_token())
    client.pubsub = pubsub.PubSubPool(client)

    # Get leatest post, form url
    URL = "https://altermmo.pl"
    web_page = requests.get(URL)
    soup = BeautifulSoup(web_page.content, "html.parser")
    dom = etree.HTML(str(soup))

    # channel token from brodcast channel
    user_int_id = 140267589
    user_id = twitch_token.user_client_id()
    user_oauth_token = twitch_token.user_oauth_token()
    user_twitch_token = twitch_token.user_twitch_token()
    bot_oauth_token = twitch_token.bot_oauth_token()
    bot_twitch_token = twitch_token.bot_twitch_token()

    def __init__(self, user_int_id=user_int_id):
        super().__init__(
            token=twitch_token.bot_twitch_access_token(),
            prefix="?",
            initial_channels=["SitLetto"],
        )
        self.user_int_id = user_int_id

    async def event_ready(self):
        print(f"Ready | {client.nick}")
        topics = [
            pubsub.channel_points(twitch_token.user_oauth_token())[self.user_int_id],
        ]
        await client.pubsub.subscribe_topics(topics)

    # Send message into channel every x seconds / minutes
    @routines.routine(minutes=5.0)
    async def test_routine(self):
        chan = bot.get_channel("SitLetto")
        await chan.send(f'{self.dom.xpath("//*[@id]/div/div/a/@href")[0]}')

    async def event_message(self, message):
        if message.echo:
            return
        await self.handle_commands(message)

    # insert quote into a db
    @client.event()
    async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
        conn = sqlite3.connect("quotes")
        cur = conn.cursor()

        cur.execute(
            f"INSERT INTO quotes (user_name, quote) VALUES (?, ?)",
            (event.user.name, event.input),
        )
        conn.commit()
        conn.close()
        print(event.user.name, event.input)

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
        conn = sqlite3.connect("quotes")
        cur = conn.cursor()
        cur.execute(""" SELECT * FROM quotes """)
        fetch_quote = cur.fetchall()
        random_quote = [quote for quote in fetch_quote]
        i = random.choice(range(len(random_quote)))
        await ctx.send(f"{random_quote[i][2]} ~{random_quote[i][1]}")

    # get all bot commends
    @commands.command()
    async def komendy(self, ctx: commands.Context):
        await ctx.send("Dostępne komendy to, ?ladneslowo, ?rulet, ?hello, rekinodtylu")


bot = Bot()
bot.run()
