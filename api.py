#All API-related code goes in the api.py file.
from flask import Flask,jsonify
from flask_cors import CORS
import discord,time,bot,asyncio,concurrent.futures
app=Flask(__name__)
CORS(app)
discord_bot=None
config=None
last_request={}

def setup():
 global discord_bot,config
 discord_bot=bot.getbot()
 config=bot.getconfig()

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

def fetch_user_data(user_id,member):
 async def async_fetch():
  user_obj=await discord_bot.fetch_user(int(user_id))
  return user_obj
 future=asyncio.run_coroutine_threadsafe(async_fetch(),discord_bot.loop)
 user_obj=future.result(timeout=10)
 ps=member.premium_since.timestamp() if member.premium_since else None
 banner=user_obj.banner.key if user_obj.banner else None
 accent=f'#{user_obj.accent_color.value:06x}' if user_obj.accent_color else None
 return {'banner':banner,'accent_color':accent,'premium_since':ps}

@app.route('/v1/users/<user_id>')
def user(user_id):
 try:
  if user_id in last_request:
   elapsed=time.time()-last_request[user_id]
   if elapsed<5:return jsonify({'success':False,'error':'Rate limit exceeded'}),429
  last_request[user_id]=time.time()
  guild=discord_bot.get_guild(int(config['server_id']))
  if not guild:return jsonify({'success':False,'error':'Server not found'}),404
  member=guild.get_member(int(user_id))
  if not member:return jsonify({'success':False,'error':'User not in server'}),404
  user_data_cache=bot.getcache()
  if user_id not in user_data_cache:
   try:
    fetched_data=fetch_user_data(user_id,member)
    user_data_cache[user_id]=fetched_data
   except:
    pass
  banner_hash=None
  accent_color=None
  premium_since=None
  if user_id in user_data_cache:
   banner_hash=user_data_cache[user_id].get('banner')
   accent_color=user_data_cache[user_id].get('accent_color')
   premium_since=user_data_cache[user_id].get('premium_since')
  avatar_hash=member.avatar.key if member.avatar else None
  avatar_decoration=None
  if member.avatar_decoration:
   avatar_decoration={'asset':member.avatar_decoration.key,'expires_at':None,'sku_id':str(member.avatar_decoration_sku_id) if hasattr(member,'avatar_decoration_sku_id') else None}
  user_data={'avatar':avatar_hash,'avatar_decoration_data':avatar_decoration,'banner':banner_hash,'accent_color':accent_color,'bot':member.bot,'discriminator':member.discriminator,'display_name':member.display_name,'global_name':member.global_name,'id':str(member.id),'public_flags':member.public_flags.value,'username':member.name,'premium_since':premium_since}
  activities_data=[]
  spotify_data=None
  current_track_id=None
  for activity in member.activities:
   if isinstance(activity,discord.Spotify):
    current_track_id=activity.track_id
    spotify_data={'album':activity.album,'album_art_url':activity.album_cover_url,'artist':'; '.join(activity.artists),'song':activity.title,'timestamps':{'start':int(activity.start.timestamp()*1000),'end':int(activity.end.timestamp()*1000)},'track_id':activity.track_id}
    activities_data.append({'type':2,'name':'Spotify','id':'spotify:1','details':activity.title,'state':'; '.join(activity.artists),'assets':{'large_image':f'spotify:{activity.album_cover_url.split("/")[-1]}','large_text':activity.album},'timestamps':{'start':int(activity.start.timestamp()*1000),'end':int(activity.end.timestamp()*1000)},'party':{'id':f'spotify:{user_id}'},'flags':48,'sync_id':activity.track_id,'session_id':'generated','created_at':int(activity.start.timestamp()*1000)})
   elif isinstance(activity,discord.CustomActivity):
    activities_data.append({'type':4,'name':'Custom Status','id':'custom','state':activity.name,'created_at':int(activity.created_at.timestamp()*1000) if activity.created_at else None,'session_id':'generated'})
   elif isinstance(activity,discord.Activity):
    act_data={'type':activity.type.value,'name':activity.name,'id':str(activity.application_id) if activity.application_id else 'generated','created_at':int(activity.created_at.timestamp()*1000) if activity.created_at else None,'session_id':'generated'}
    if activity.details:act_data['details']=activity.details
    if activity.state:act_data['state']=activity.state
    if activity.assets:
     assets={}
     if hasattr(activity,'large_image_url') and activity.large_image_url:assets['large_image']=activity.large_image_url
     if hasattr(activity,'large_image_text') and activity.large_image_text:assets['large_text']=activity.large_image_text
     if hasattr(activity,'small_image_url') and activity.small_image_url:assets['small_image']=activity.small_image_url
     if hasattr(activity,'small_image_text') and activity.small_image_text:assets['small_text']=activity.small_image_text
     if assets:act_data['assets']=assets
    if activity.start:act_data['timestamps']={'start':int(activity.start.timestamp()*1000)}
    if activity.end:
     if 'timestamps' not in act_data:act_data['timestamps']={}
     act_data['timestamps']['end']=int(activity.end.timestamp()*1000)
    activities_data.append(act_data)
  status_map={'online':'online','idle':'idle','dnd':'dnd','offline':'offline','invisible':'offline'}
  current_status=status_map.get(str(member.status),'offline')
  uid=str(member.id)
  last_seen=bot.getseen()
  seen_ago=None
  if current_status=='offline' and uid in last_seen:
   elapsed=time.time()-last_seen[uid]
   seen_ago=formattime(elapsed)
  spotify_history=bot.getspotify()
  recent_tracks=[]
  if uid in spotify_history:
   for track in spotify_history[uid][:5]:
    if current_track_id and track['track_id']==current_track_id:continue
    elapsed=time.time()-track['played_at']
    recent_tracks.append({'album':track['album'],'album_art_url':track['album_art_url'],'artist':track['artist'],'song':track['song'],'track_id':track['track_id'],'played_ago':formattime(elapsed)})
  response={'success':True,'data':{'discord_user':user_data,'activities':activities_data,'discord_status':current_status,'active_on_discord_web':member.web_status!=discord.Status.offline,'active_on_discord_desktop':member.desktop_status!=discord.Status.offline,'active_on_discord_mobile':member.mobile_status!=discord.Status.offline,'listening_to_spotify':spotify_data is not None,'spotify':spotify_data,'last_seen':seen_ago,'spotify_recent':recent_tracks}}
  return jsonify(response)
 except Exception as e:
  return jsonify({'success':False,'error':str(e)}),500

def run():
 app.run(host='0.0.0.0',port=5000)
