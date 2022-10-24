from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self, token: str, *, prefix: Union[str, list, tuple, set, Callable, Coroutine], client_secret: str = None, initial_channels: Union[list, tuple, Callable] = None, heartbeat: Optional[float] = 30, retain_cache: Optional[bool] = True, **kwargs):
        super().__init__(token, prefix=prefix, client_secret, initial_channels, heartbeat, retain_cache, **kwargs)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')
        return await super().event_ready()
    
    
    @commands.command()
    async def hello(self, ctx: commands.Context):
        # send a hello back!

        await ctx.send(f'Hello {ctx.author.name}!')