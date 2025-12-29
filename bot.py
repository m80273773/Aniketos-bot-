import discord
from discord.ext import commands

# Bot token
TOKEN = 'MTQ1NDg0MzQ2MTM4Njc2ODY2MA.G814hp.ThE3Pr1Y-DR7hZ3nV1qQZjEXQ39xMzsW4iM28E'

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store XP
xp_data = {}  # renamed to avoid conflict with command

# Voice channels and corresponding roles
vc_roles = {
    'Gooning !': 'Gooning in vc',
    'Music for now': 'Listening in vc'
}

# Bot ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# Track messages for XP
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    user_id = str(message.author.id)
    xp_data[user_id] = xp_data.get(user_id, 0) + 1  # Add 1 XP per message

    await bot.process_commands(message)  # keep this at the end

# XP command
@bot.command()
async def xp(ctx):
    user_id = str(ctx.author.id)
    user_xp = xp_data.get(user_id, 0)
    await ctx.send(f'{ctx.author.name}, your XP is {user_xp}')

# Auto-role for voice channels
@bot.event
async def on_voice_state_update(member, before, after):
    guild = member.guild
    
    # Leaving a VC
    if before.channel and before.channel.name in vc_roles:
        role_name = vc_roles[before.channel.name]
        role = discord.utils.get(guild.roles, name=role_name)
        if role in member.roles:
            await member.remove_roles(role)
            print(f'Removed {role_name} from {member.name}')

    # Joining a VC
    if after.channel and after.channel.name in vc_roles:
        role_name = vc_roles[after.channel.name]
        role = discord.utils.get(guild.roles, name=role_name)
        if role and role not in member.roles:
            await member.add_roles(role)
            print(f'Assigned {role_name} to {member.name}')

# Run the bot
bot.run(TOKEN)