import discord,json,time
from discord.ext import commands
from datetime import timedelta

with open('config.json','r') as f:
 config=json.load(f)

bot=commands.Bot(command_prefix='!',intents=discord.Intents.all())
start=time.time()

def format(seconds):
 days=int(seconds//86400)
 hours=int((seconds%86400)//3600)
 minutes=int((seconds%3600)//60)
 secs=int(seconds%60)
 years=days//365
 days=days%365
 parts=[]
 if years>0:
  parts.append(f'{years} year{"s" if years>1 else ""}')
 if days>0:
  parts.append(f'{days} day{"s" if days>1 else ""}')
 if hours>0:
  parts.append(f'{hours} hour{"s" if hours>1 else ""}')
 if minutes>0:
  parts.append(f'{minutes} minute{"s" if minutes>1 else ""}')
 if secs>0:
  parts.append(f'{secs} second{"s" if secs>1 else ""}')
 return ', '.join(parts) if parts else '0 seconds'

@bot.event
async def on_ready():
 await bot.tree.sync()
 print(f'{bot.user} ready')

@bot.hybrid_command(name='uptime')
async def uptime(ctx):
 current=time.time()
 elapsed=current-start
 embed=discord.Embed(title='Bot Uptime',description=format(elapsed),color=discord.Color.blue())
 embed.add_field(name='Total Seconds',value=f'{int(elapsed)}',inline=False)
 await ctx.send(embed=embed)

@bot.hybrid_command(name='link')
async def link(ctx):
 user_id=ctx.author.id
 api_url=f'http://localhost:5000/v1/users/{user_id}'
 embed=discord.Embed(title='Your API Link',description=api_url,color=discord.Color.green())
 await ctx.send(embed=embed)

def run():
 bot.run(config['token'])

def getbot():
 return bot

def getconfig():
 return config
 