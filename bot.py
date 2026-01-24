import discord,json,time
from discord.ext import commands
from datetime import timedelta
with open('config.json','r') as f:config=json.load(f)
bot=commands.Bot(command_prefix='!',intents=discord.Intents.all(),help_command=None)
start=time.time()
last_seen={}
spotify_history={}
user_cache={}
base_url='http://localhost:5000' #Your own API URL that you want the Discord bot to give the user, including the user ID, when the link command is executed.

def formattime(seconds):
 days=int(seconds//86400)
 hours=int((seconds%86400)//3600)
 minutes=int((seconds%3600)//60)
 secs=int(seconds%60)
 years=days//365
 days=days%365
 parts=[]
 if years>0:parts.append(f'{years} year{"s" if years>1 else ""}')
 if days>0:parts.append(f'{days} day{"s" if days>1 else ""}')
 if hours>0:parts.append(f'{hours} hour{"s" if hours>1 else ""}')
 if minutes>0:parts.append(f'{minutes} minute{"s" if minutes>1 else ""}')
 if secs>0:parts.append(f'{secs} second{"s" if secs>1 else ""}')
 return ', '.join(parts) if parts else '0 seconds'

@bot.event
async def on_ready():
 await bot.tree.sync()
 print(f'{bot.user} ready')
 guild=bot.get_guild(int(config['server_id']))
 if guild:
  for member in guild.members:
   try:
    user=await bot.fetch_user(member.id)
    premium_since=member.premium_since.timestamp() if member.premium_since else None
    banner=user.banner.key if user.banner else None
    accent=f'#{user.accent_color.value:06x}' if user.accent_color else None
    user_cache[str(member.id)]={'banner':banner,'accent_color':accent,'premium_since':premium_since}
   except:
    pass

@bot.event
async def on_member_join(member):
 try:
  user=await bot.fetch_user(member.id)
  premium_since=member.premium_since.timestamp() if member.premium_since else None
  user_cache[str(member.id)]={'banner':user.banner.key if user.banner else None,'accent_color':f'#{user.accent_color.value:06x}' if user.accent_color else None,'premium_since':premium_since}
 except:
  pass

@bot.event
async def on_user_update(before,after):
 try:
  user=await bot.fetch_user(after.id)
  guild=bot.get_guild(int(config['server_id']))
  member=guild.get_member(after.id) if guild else None
  premium_since=member.premium_since.timestamp() if member and member.premium_since else None
  user_cache[str(after.id)]={'banner':user.banner.key if user.banner else None,'accent_color':f'#{user.accent_color.value:06x}' if user.accent_color else None,'premium_since':premium_since}
 except:
  pass

@bot.event
async def on_presence_update(before,after):
 status_map={'online':'online','idle':'idle','dnd':'dnd','offline':'offline','invisible':'offline'}
 before_status=status_map.get(str(before.status),'offline')
 after_status=status_map.get(str(after.status),'offline')
 uid=str(after.id)
 if after_status!='offline':last_seen[uid]=time.time()
 elif before_status!='offline' and after_status=='offline':last_seen[uid]=time.time()
 before_spotify=None
 after_spotify=None
 for activity in before.activities:
  if isinstance(activity,discord.Spotify):
   before_spotify=activity
   break
 for activity in after.activities:
  if isinstance(activity,discord.Spotify):
   after_spotify=activity
   break
 if before_spotify and not after_spotify:
  if uid not in spotify_history:spotify_history[uid]=[]
  track_data={'album':before_spotify.album,'album_art_url':before_spotify.album_cover_url,'artist':'; '.join(before_spotify.artists),'song':before_spotify.title,'track_id':before_spotify.track_id,'played_at':time.time()}
  if not spotify_history[uid] or spotify_history[uid][0]['track_id']!=before_spotify.track_id:
   spotify_history[uid].insert(0,track_data)
   if len(spotify_history[uid])>10:spotify_history[uid]=spotify_history[uid][:10]
 elif before_spotify and after_spotify and before_spotify.track_id!=after_spotify.track_id:
  if uid not in spotify_history:spotify_history[uid]=[]
  track_data={'album':before_spotify.album,'album_art_url':before_spotify.album_cover_url,'artist':'; '.join(before_spotify.artists),'song':before_spotify.title,'track_id':before_spotify.track_id,'played_at':time.time()}
  if not spotify_history[uid] or spotify_history[uid][0]['track_id']!=before_spotify.track_id:
   spotify_history[uid].insert(0,track_data)
   if len(spotify_history[uid])>10:spotify_history[uid]=spotify_history[uid][:10]

@bot.hybrid_command(name='link',hidden=True)
async def link(ctx):
 user_id=ctx.author.id
 api_url=f'{base_url}/v1/users/{user_id}'
 avatar_url=ctx.author.display_avatar.url
 embed=discord.Embed(title='Your Profile API Link',description='Access your Discord profile data through this API endpoint. Use it to display your status, activities, and Spotify listening history on external websites or applications.',color=0x5865F2)
 embed.add_field(name='API Endpoint',value=f'`{api_url}`',inline=False)
 embed.set_thumbnail(url=avatar_url)
 embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=avatar_url)
 view=discord.ui.View()
 button=discord.ui.Button(label='Open Link',style=discord.ButtonStyle.link,url=api_url,emoji='📊')
 view.add_item(button)
 await ctx.send(embed=embed,view=view,ephemeral=True)

@bot.hybrid_command(name='uptime',hidden=True)
async def uptime(ctx):
 current=time.time()
 elapsed=current-start
 embed=discord.Embed(title='Bot Uptime',description=formattime(elapsed),color=discord.Color.blue())
 await ctx.send(embed=embed)

@bot.hybrid_command(name='help',hidden=True)
async def help(ctx):
 embed=discord.Embed(title='Bot Commands',description='Here are all available commands for this bot.',color=0x5865F2)
 embed.add_field(name='!link',value='Get your API link with a clickable panel button',inline=False)
 embed.add_field(name='!uptime',value='Check how long the bot has been running',inline=False)
 embed.add_field(name='!help',value='Show this help message',inline=False)
 embed.set_footer(text=f'Requested by {ctx.author.name}',icon_url=ctx.author.display_avatar.url)
 await ctx.send(embed=embed)

def run():
 bot.run(config['token'])

def getbot():
 return bot

def getconfig():
 return config

def getseen():
 return last_seen

def getspotify():
 return spotify_history

def getcache():
 return user_cache
