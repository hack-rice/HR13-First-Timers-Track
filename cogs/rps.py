import discord
from discord.ext import commands
import asyncio


# cogs let you put related commands and functions together under a class
class RPS(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='challenge',
                      # brief and description are what show up in the help menu
                      brief='Play Rock, Paper, Scissors',
                      description='Play Rock, Paper, Scissors by pinging a friend; can also set how many rounds you want to play',
                      # aliases give shorthands for the command
                      aliases=['chall', 'rps'])
    async def challenge(self,
                        ctx: commands.Context,
                        # descriptions of parameters appear in help menu with this command specified
                        member: discord.Member = commands.parameter(description='The member you want to challenge'),
                        rounds: int = commands.parameter(default=1,
                                                         description='The number of rounds you want to play for, defaults to 1')):
        """
        Play Rock, Paper, Scissors
        :param ctx: provides context for command call (who called it, which channel was it called in, etc)
        :param member: the opponent
        :param rounds: the number of rounds to play for; defaults to 1 if not specified
        """
        p1_wins = 0
        p2_wins = 0
        # the user should not be able to play themselves
        if ctx.author == member:
            await ctx.channel.send("You can't challenge yourself!")
            return
        await ctx.channel.send(
            f'{ctx.author.mention} challenged {member.mention} to a game of Rock, Paper, Scissors! {rounds} game(s) will be played.')
        for round in range(rounds):
            # print(f'Playing round {round}')
            # send this message before each round to inform users about game state
            await ctx.channel.send(
                f'It is currently round {round + 1} out of {rounds}. {ctx.author.mention} has won {p1_wins} game(s) so far. {member.mention} has won {p2_wins} game(s) so far.')
            await ctx.channel.send(f'{ctx.author.mention} and {member.mention} need to DM me their responses!')

            resp = None
            choices = {"rock": 0, "paper": 1, "scissors": 2}
            p1_choice = None
            p2_choice = None

            def check(msg):
                """
                Check if incoming messages are valid player responses; to be passed into loop
                """
                # specify p1_choice and p2_choice as nonlocal to be able to use them outside of the function
                nonlocal p1_choice, p2_choice
                # check if incoming message is one of {rock, paper, scissors} and the message was sent in a DM to the bot
                if msg.content.lower() in choices.keys() and isinstance(msg.channel, discord.DMChannel):
                    if msg.author == ctx.author:
                        p1_choice = msg.content
                    if msg.author == member:
                        p2_choice = msg.content
                # once we receive valid responses from both players, return True
                return p1_choice != None and p2_choice != None

            try:
                # resp will not be None if both players respond within 45 seconds
                resp = await self.client.wait_for("message", timeout=45, check=check)
            except asyncio.TimeoutError:
                # exit the loop (and therefore the game) if players take too long
                await ctx.channel.send(f'You took too long to respond!')
                break

            # if resp is not None (i.e. the above try catch statement did not receive an exception), determine game results
            if resp:
                await ctx.channel.send(f'{ctx.author.mention} played {p1_choice}! {member.mention} played {p2_choice}!')
                # game logic: since rock loses to paper, paper loses to scissors, and scissors loses to rock, we can shorten the code to determine the winner using mod math
                if ((choices[p1_choice] + 1) % 3) == choices[p2_choice]:
                    await ctx.channel.send(
                        f'{member.mention} won this round! Better luck next time {ctx.author.mention}!')
                    p2_wins += 1
                elif p1_choice == p2_choice:
                    await ctx.channel.send(f'This round was a tie!')
                else:
                    await ctx.channel.send(
                        f'{ctx.author.mention} won this round! Better luck next time {member.mention}!')
                    p1_wins += 1
        # once all rounds have been played or players took too long to respond, give game summary
        await ctx.channel.send(
            f'The game ended with {ctx.author.mention} winning {p1_wins} rounds and {member.mention} winning {p2_wins} rounds.')


# add this cog to the client
async def setup(client):
    await client.add_cog(RPS(client))
