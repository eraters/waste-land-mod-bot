import discord
import os
import asyncio
from discord.ext import commands, tasks

bot = commands.Bot(command_prefix="wls!")

@bot.event
async def on_ready():
    print("--------------------")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    return

bot.remove_command('help')

@bot.command()
async def ping(ctx):
    embed = discord.Embed(colour=0x00FF00)
    embed.add_field(name="Ping", value=f'🏓 {round(bot.latency * 1000)}ms')
    embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.command()
async def new(ctx):
    if ctx.message.guild.id == int("584623593682501652"):
      member = ctx.message.author
      server = ctx.message.guild
      createchannel = await server.create_text_channel(f"ticket-{member}")
      embed = discord.Embed(title=f"New ticket created",
                            description=f"Hello {member.mention}, thanks for reaching out to our support team, a member of staff will be with you as soon as possible.", color=0x7289DA)
      embed.set_footer(text=f"Request by {ctx.author}", icon_url=member.avatar_url)
      staff = discord.utils.get(ctx.message.author.guild.roles, name="Support")
      guest = discord.utils.get(ctx.message.author.guild.roles, name="member")
      everyone = ctx.message.author.guild.default_role
      disallow = discord.PermissionOverwrite()
      disallow.read_messages = False
      disallow.send_messages = False
      allow = discord.PermissionOverwrite()
      allow.read_messages = True
      allow.send_messages = True
      await createchannel.set_permissions(guest, overwrite=disallow)
      await createchannel.set_permissions(everyone, overwrite=disallow)
      await createchannel.set_permissions(ctx.message.author, overwrite=allow)
      await createchannel.set_permissions(staff, overwrite=allow)
      await createchannel.send(embed=embed)
      channel = bot.get_channel(createchannel)
      await ctx.send("Your ticket has been created!")
      await createchannel.send("<@&635609395627032596>")
    else:
      await ctx.send(":x: You have to be in the correct server [WasteLandSMP] to do this!")

@bot.command()
async def close(ctx):
    staff = discord.utils.get(ctx.message.author.guild.roles, name="Support")
    if staff in ctx.author.roles:
        channel = ctx.message.channel
        embed = discord.Embed(
            title="Closing ticket", description="This ticket will be closed in 30 seconds", color=0x7289DA)
        confirmmsg = await ctx.send(embed=embed)
        await asyncio.sleep(30)
        await channel.delete(reason="Ticket closed")
    else:
        await ctx.send(":x: You do not have permission to do that.")

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(
        title="WasteLandSMP'S Bot", description="Info", color=0x7289DA)

    embed.add_field(name="Bot Owner", value="ImLazyWithAZ#8327 and AliTheTerminator#5112")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    embed.add_field(name="User count",
                    value=f"{len(list(bot.get_all_members()))}")

    embed.set_footer(
        text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

#ban

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason='No reason provided.'):
    server = ctx.message.guild
    if member.bot == True:
        await member.ban(reason=reason)
        await ctx.message.delete()
        await ctx.send(f'{member} has been banned.')
    else:
        dm = discord.Embed(title=f"You have been banned from `{server.name}`!", color=0x7289DA)
        dm.add_field(name="Moderator:",
                        value=ctx.message.author.display_name)
        dm.add_field(name="Reason:", value=f"{reason}")
        dm.set_thumbnail(url=member.avatar_url)
        await member.send(embed=dm)  # Send DM
        await member.ban(reason=reason)  # Ban
        await ctx.message.delete()  # Delete The Message
        await ctx.send('member has been banned.')

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
        
#kick

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason='No reason provided.'):
    server = ctx.message.guild
    if member.bot == True:
        await member.kick(reason=reason)
        await ctx.message.delete()
        await ctx.send(f'{member} has been kicked.')
    else:
        dm = discord.Embed(title=f"You have been kicked from `{server.name}`!", color=0x7289DA)
        dm.set_thumbnail(url=member.avatar_url)
        dm.add_field(name="Reason:", value=f"{reason}")
        dm.add_field(name="Moderator:",
                        value=ctx.message.author.display_name)
        await member.send(embed=dm)  # Send DM
        await member.kick(reason=reason)  # Kick
        await ctx.message.delete()  # Delete The Message
        await ctx.send('member has been kicked.')
 
@bot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member=None):
    if discord.utils.get(ctx.guild.roles, name="muted") is None:
      guild = ctx.guild
      await guild.create_role(name="muted")
    if not member:
        await ctx.send("Please specify a member.")
        return
    else:
      role = discord.utils.get(ctx.guild.roles, name="muted")
      await member.add_roles(role)
      await ctx.send("Role added!")
    
@bot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member = None):
    role = discord.utils.get(ctx.guild.roles, name="muted")
    if not member:
        await ctx.send("Please specify a member.")
        return
    await member.remove_roles(role)
    await ctx.send("Role removed!")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Clears the amount of messages that you filled in."""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"{amount} messages got deleted.")
    
@bot.command()
async def hello(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {}!".format(member.mention))
    
@bot.command()
async def overrideenable(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {} your override mode is on!!".format(member.mention))

@bot.command()
async def overridedisable(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("Hello {} your override mode is off!!".format(member.mention))

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="WasteLandSMP's bot", description="Commands:", color=0x7289DA)

    embed.set_thumbnail(
        url='https://images.emojiterra.com/twitter/v12/512px/1f3d3.png')
    embed.add_field(name="*kick", value="Kicks a member.", inline=False)
    embed.add_field(name="*ban", value="Bans a member.", inline=False)
    embed.add_field(name="*mute", value="Mutes a member.", inline=False)
    embed.add_field(name="*unmute", value="Unmutes a member.", inline=False)
    embed.add_field(name="*unban", value="Unbans a user.", inline=False)
    embed.add_field(name="*clear", value="Clears the amount of messages that you filled in.", inline=False)
    embed.add_field(name="*new", value="Makes a new ticket. (WASTELANDSMP SERVER ONLY!!)", inline=False)
    embed.add_field(name="*ping", value="Pings the bot.", inline=False)
    embed.add_field(name="*help", value="Gives this message.", inline=False)
    embed.add_field(name="*support", value="Gets a link to the support server.", 
    embed.add_field(
        name="*botinfo", value="Gives info about the bot.", inline=False)
    embed.add_field(name="*hello", value="Says hello to you.", inline=False)
    embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)
    

@bot.command()
async def support(ctx, member : discord.Member= None):
    member = ctx.author if not member else member
    await ctx.send("The support server for AZ's Bot is https://discord.gg/NJ9mr9C!") 

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error:",
                              description=f"The command `{ctx.invoked_with}` was not found! We suggest you do `help` to see all of the commands",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        roleid = error.missing_role
        embed = discord.Embed(title="Error:",
                              description=f"You don't have permission to execute `{ctx.invoked_with}`, this requires the `{roleid}` role to be executed",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error:",
                              description=f"`{error}`",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
        raise error
    
bot.run(os.getenv('TOKEN'))
