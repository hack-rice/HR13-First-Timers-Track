import discord
from discord.ext import commands
import asyncio


class PollButton(discord.ui.Button):
    message = ''
    count = 0

    def __init__(self, message):
        super().__init__(label=message, style=discord.ButtonStyle.primary)
        self.message = message

    # defines the behavior after a user clicks a poll button (returns user choice and increments poll)
    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's choice and increment the poll
        # self.style = discord.ButtonStyle.grey
        self.count += 1
        user1 = interaction.user
        # await user.send(f'Your choice is {self.message}')
        await interaction.response.send_message(f'{user1.mention}\'s choice is {self.message}', ephemeral = True)


class Poll(discord.ui.View):

    def __init__(self, ctx, question: str, args: list, timeout):
        super().__init__(timeout=timeout)
        self.question = question
        self.ctx = ctx
        for choice in args:
            self.add_item(PollButton(choice))

    async def on_timeout(self):
        await self.ctx.send(self.question)
        for item in self.children:
            await self.ctx.send(f'{item.message}: {item.count} votes')

# cogs let you put related commands and functions together under a class
class Util(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='timer',
                      # brief and description are what show up in the help menu
                      brief='Get pinged after given number of seconds elapses',
                      description='Get pinged after given number of seconds elapses',
                      # aliases give shorthands for the command
                      aliases=['remind'])
    async def timer(self,
                    ctx: commands.Context,
                    time: int):
        """
        Make a random choice between the arguments given
        :param ctx: provides context for command call (who called it, which channel was it called in, etc)
        :param time: the number of seconds to count down from
        """
        await asyncio.sleep(time)
        await ctx.send(f'{ctx.author.mention} your timer ran out! {time} seconds have passed.')

    @commands.command(name='poll',
                      # brief and description are what show up in the help menu
                      brief='Make a poll that closes in a given amount of minutes',
                      description='Vote on choices!',
                      # aliases give shorthands for the command
                      )
    async def poll(self, ctx, mins, question: str, *args: str):
        '''
        Creates a poll on discord, with the first argument being the question asked, and the following arguments being the choices for the poll
        :param ctx: the character that denotes a command for this bot (?)
        :param question: the question that is being polled
        :param args: an arbitrary amount of choices to poll
        :param mins: the number of minutes before the poll closes
        :return: None
        '''
        view = Poll(ctx, question, args, int(mins) * 60)
        await ctx.send(question, view=view)


# add this cog to the client
async def setup(client):
    await client.add_cog(Util(client))
