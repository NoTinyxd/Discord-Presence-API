from flask import Flask,jsonify
from flask_cors import CORS
import discord
import bot
#..
app=Flask(__name__)
CORS(app)
discord_bot=None
config=None

def setup():
 global discord_bot,config
 discord_bot=bot.getbot()
 config=bot.getconfig()

@app.route('/v1/users/<user_id>')
def user(user_id):
 try:
  guild=discord_bot.get_guild(int(config['server_id']))
  if not guild:
   return jsonify({'success':False,'error':'Server not found'}),404
  member=guild.get_member(int(user_id))
  if not member:
   return jsonify({'success':False,'error':'User not in server'}),404
  avatar_hash=None
  if member.avatar:
   avatar_hash=member.avatar.key
  elif member.default_avatar:
   avatar_hash=None
  avatar_decoration=None
  if member.avatar_decoration:
   avatar_decoration={'asset':member.avatar_decoration.key,'expires_at':None,'sku_id':str(member.avatar_decoration_sku_id) if hasattr(member,'avatar_decoration_sku_id') else None}
  banner_hash=None
  accent_color=None
  if hasattr(member,'banner') and member.banner:
   banner_hash=member.banner.key
  if hasattr(member,'accent_color') and member.accent_color:
   accent_color=f'#{member.accent_color.value:06x}'
  user_data={'avatar':avatar_hash,'avatar_decoration_data':avatar_decoration,'banner':banner_hash,'accent_color':accent_color,'bot':member.bot,'collectibles':None,'discriminator':'0','display_name':member.display_name,'display_name_styles':None,'global_name':member.global_name,'id':str(member.id),'primary_guild':None,'public_flags':member.public_flags.value,'username':member.name}
  activities_data=[]
  spotify_data=None
  for activity in member.activities:
   if isinstance(activity,discord.Spotify):
    spotify_data={'album':activity.album,'album_art_url':activity.album_cover_url,'artist':'; '.join(activity.artists),'song':activity.title,'timestamps':{'start':int(activity.start.timestamp()*1000),'end':int(activity.end.timestamp()*1000)},'track_id':activity.track_id}
    activities_data.append({'type':2,'name':'Spotify','id':'spotify:1','details':activity.title,'state':'; '.join(activity.artists),'assets':{'large_image':f'spotify:{activity.album_cover_url.split("/")[-1]}','large_text':activity.album},'timestamps':{'start':int(activity.start.timestamp()*1000),'end':int(activity.end.timestamp()*1000)},'party':{'id':f'spotify:{user_id}'},'flags':48,'sync_id':activity.track_id,'session_id':'generated','created_at':int(activity.start.timestamp()*1000)})
   elif isinstance(activity,discord.CustomActivity):
    activities_data.append({'type':4,'name':'Custom Status','id':'custom','state':activity.name,'created_at':int(activity.created_at.timestamp()*1000) if activity.created_at else None,'session_id':'generated'})
   elif isinstance(activity,discord.Activity):
    act_data={'type':activity.type.value,'name':activity.name,'id':str(activity.application_id) if activity.application_id else 'generated','created_at':int(activity.created_at.timestamp()*1000) if activity.created_at else None,'session_id':'generated'}
    if activity.details:
     act_data['details']=activity.details
    if activity.state:
     act_data['state']=activity.state
    if activity.assets:
     assets={}
     if hasattr(activity,'large_image_url') and activity.large_image_url:
      assets['large_image']=activity.large_image_url
     if hasattr(activity,'large_image_text') and activity.large_image_text:
      assets['large_text']=activity.large_image_text
     if hasattr(activity,'small_image_url') and activity.small_image_url:
      assets['small_image']=activity.small_image_url
     if hasattr(activity,'small_image_text') and activity.small_image_text:
      assets['small_text']=activity.small_image_text
     if assets:
      act_data['assets']=assets
    if activity.start:
     act_data['timestamps']={'start':int(activity.start.timestamp()*1000)}
    if activity.end:
     if 'timestamps' not in act_data:
      act_data['timestamps']={}
     act_data['timestamps']['end']=int(activity.end.timestamp()*1000)
    activities_data.append(act_data)
  status_map={'online':'online','idle':'idle','dnd':'dnd','offline':'offline','invisible':'offline'}
  response={'success':True,'data':{'kv':{},'discord_user':user_data,'activities':activities_data,'discord_status':status_map.get(str(member.status),'offline'),'active_on_discord_web':member.web_status!=discord.Status.offline,'active_on_discord_desktop':member.desktop_status!=discord.Status.offline,'active_on_discord_mobile':member.mobile_status!=discord.Status.offline,'active_on_discord_embedded':False,'listening_to_spotify':spotify_data is not None,'spotify':spotify_data}}
  return jsonify(response)
 except Exception as e:
  return jsonify({'success':False,'error':str(e)}),500

def run():

 app.run(host='0.0.0.0',port=5000)
