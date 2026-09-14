import os, json, random, datetime, asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = 1433457392917676138
GUILD_ID = 1544039840767803412
SERVER_INVITE = 'https://discord.gg/FtxqMbBs'
PERM_FILE = 'permissions.json'
STATE_FILE = 'state.json'

EMOJI_IDS = {
 'arrow':1549136782971379712,'crown':1549137817341268058,'butterfly':1549136722686644336,
 'loading':1549136416250921060,'dot':1544406593351844012,'fire':1549138871537639507,
 'hashy':1544406358152061038,'verify':1549136346902175754,'kick':1549138352618471434,
 'banned':1549138249988182147,'bot':1549139254712606830,'dance':1549138072694689943,
 'confuse':1549137286925648012,'diamond':1549139140803563644,'error':1549136020094717982,
 'hammer':1549138507539288126,'help':1549139550134075513,'link':1549139611123449997,
 'home':1549139446950269060,'mute':1549138714624655450,'heart':1549139076580511804,
 'star':1549138951413956631,'sparkles':1549138777660850216,'special':1549136671260278896,
 'support':1544406094451974173,'lock':1549137685954953318,'warn':1549136157898575942,
 'settings':1549139334425219163}
ROLE = {'welcome':'butterfly','brand':'sparkles','loading':'loading','owner':'crown','premium':'diamond','success':'verify','error':'error','warning':'warn','locked':'lock','moderation':'hammer','ban':'banned','kick':'kick','mute':'mute','help':'help','settings':'settings','support':'support','ticket':'support','buy':'diamond','report':'warn','close':'lock','important':'star','fire':'fire','link':'link','home':'home','bot':'bot'}

COMMANDS = [
'ping','help','server','userinfo','avatar','banner','roles','emojis','say','announce','embed','poll','botinfo','invite','support','channelinfo','roleinfo',
'ban','unban','kick','warn','warnings','warnings_clear','timeout','untimeout','mute','unmute','purge','slowmode','lock','unlock',
'ticket_panel','ticket_setup','ticket_close','ticket_reopen','ticket_add','ticket_remove','ticket_rename','ticket_claim','ticket_unclaim','ticket_transcript','ticket_lock','ticket_unlock','ticket_delete',
'report','report_setup','report_list','report_view','report_close','report_claim','report_delete',
'welcome_setup','welcome_test','welcome_disable','goodbye_setup','goodbye_test','giveaway_start','giveaway_end','giveaway_reroll','giveaway_list',
'lockdown','unlockdown','security_setup','security_whitelist_add','security_whitelist_remove','security_whitelist_list','access']

def load_json(path, default):
    try:
        with open(path, encoding='utf-8') as f: return json.load(f)
    except Exception: return default

data = load_json(PERM_FILE, {'users':{},'warnings':{}})
state = load_json(STATE_FILE, {'ticket_category':None,'report_channel':None,'welcome_channel':None,'goodbye_channel':None,'giveaways':{},'security':{'enabled':True,'whitelist':[]}})

def save():
    with open(PERM_FILE,'w',encoding='utf-8') as f: json.dump(data,f,indent=2)
    with open(STATE_FILE,'w',encoding='utf-8') as f: json.dump(state,f,indent=2)

def owner(uid): return uid == OWNER_ID

def allowed(uid, command): return owner(uid) or command in data.get('users',{}).get(str(uid),[])

def em(g, role, fallback='✨'):
    eid = EMOJI_IDS.get(ROLE.get(role, role))
    e = g.get_emoji(eid) if g and eid else None
    return str(e) if e else fallback

def E(g, title, desc, role='success'):
    return discord.Embed(title=f'{em(g,role)}  {title}', description=desc, colour=discord.Colour.gold(), timestamp=datetime.datetime.now(datetime.timezone.utc))

async def guard(i, cmd):
    if allowed(i.user.id, cmd): return True
    await i.response.send_message(embed=E(i.guild,'ACCESS DENIED',f'{em(i.guild,"error","❌")} You are not authorized to use `/{cmd}`.\n\n{em(i.guild,"owner","👑")} Ask the LIGHTNESS owner to grant access.\n{em(i.guild,"link","🔗")} {SERVER_INVITE}','locked'),ephemeral=True)
    return False

async def owner_guard(i):
    if owner(i.user.id): return True
    await i.response.send_message(embed=E(i.guild,'OWNER ONLY',f'{em(i.guild,"error","❌")} This control is reserved for the configured owner.','locked'),ephemeral=True)
    return False

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!', intents=discord.Intents.all())
    async def setup_hook(self):
        g=discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=g)
        await self.tree.sync(guild=g)
        self.add_view(TicketView())
        self.add_view(GiveawayView())

bot=Bot()

@bot.event
async def on_ready(): print(f'LIGHTNESS online as {bot.user} | guild={GUILD_ID}')

# ---------- General ----------
@bot.tree.command(name='ping',description='Check bot latency')
async def ping(i):
    if await guard(i,'ping'): await i.response.send_message(embed=E(i.guild,'LIGHTNESS ONLINE',f'{em(i.guild,"success","✅")} **{round(bot.latency*1000)}ms**\n{em(i.guild,"fire","🔥")} Security + service modules active.','bot'),ephemeral=True)

@bot.tree.command(name='help',description='Beautiful LIGHTNESS command center')
async def help_cmd(i):
    if not await guard(i,'help'): return
    e=E(i.guild,'LIGHTNESS • COMMAND CENTER',f'{em(i.guild,"crown","👑")} **Premium server control**\n{em(i.guild,"sparkles","✨")} Animated/custom emoji UI\n{em(i.guild,"link","🔗")} {SERVER_INVITE}\n\n**Every command is permission-protected.**', 'brand')
    e.add_field(name=f'{em(i.guild,"home","🏠")} GENERAL',value='`/ping` `/server` `/userinfo` `/avatar` `/banner` `/roles` `/emojis` `/botinfo` `/invite` `/support` `/channelinfo` `/roleinfo`',inline=False)
    e.add_field(name=f'{em(i.guild,"moderation","🛡️")} MODERATION',value='`/ban` `/unban` `/kick` `/warn` `/warnings` `/warnings_clear` `/timeout` `/untimeout` `/mute` `/unmute` `/purge` `/slowmode` `/lock` `/unlock`',inline=False)
    e.add_field(name=f'{em(i.guild,"ticket","🎫")} TICKETS',value='`/ticket_panel` `/ticket_setup` `/ticket_close` `/ticket_reopen` `/ticket_add` `/ticket_remove` `/ticket_rename` `/ticket_claim` `/ticket_unclaim` `/ticket_transcript` `/ticket_lock` `/ticket_unlock` `/ticket_delete`',inline=False)
    e.add_field(name=f'{em(i.guild,"report","🚨")} REPORTS',value='`/report` `/report_setup` `/report_list` `/report_view` `/report_close` `/report_claim` `/report_delete`',inline=False)
    e.add_field(name=f'{em(i.guild,"welcome","👋")} WELCOME / GOODBYE',value='`/welcome_setup` `/welcome_test` `/welcome_disable` `/goodbye_setup` `/goodbye_test`',inline=False)
    e.add_field(name=f'{em(i.guild,"premium","💎")} GIVEAWAYS',value='`/giveaway_start` `/giveaway_end` `/giveaway_reroll` `/giveaway_list`',inline=False)
    e.add_field(name=f'{em(i.guild,"moderation","🛡️")} SECURITY',value='`/lockdown` `/unlockdown` `/security_setup` `/security_whitelist_add` `/security_whitelist_remove` `/security_whitelist_list`',inline=False)
    e.add_field(name=f'{em(i.guild,"owner","👑")} ACCESS',value='`/access` — owner controls who can use commands. Use `all` to grant everything.',inline=False)
    e.set_footer(text='LIGHTNESS • secure • animated • premium')
    await i.response.send_message(embed=e,ephemeral=True)

@bot.tree.command(name='server',description='Server information')
async def server(i):
    if await guard(i,'server'): await i.response.send_message(embed=E(i.guild,i.guild.name,f'{em(i.guild,"home")} Members: **{i.guild.member_count}**\nChannels: **{len(i.guild.channels)}**\nRoles: **{len(i.guild.roles)}**\nID: `{i.guild.id}`','home'),ephemeral=True)

@bot.tree.command(name='userinfo',description='Show member information')
@app_commands.describe(user='Member')
async def userinfo(i,user:discord.Member=None):
    if await guard(i,'userinfo'):
        u=user or i.user
        await i.response.send_message(embed=E(i.guild,'USER INFORMATION',f'{em(i.guild,"bot")} {u.mention}\nID: `{u.id}`\nCreated: <t:{int(u.created_at.timestamp())}:R>\nJoined: <t:{int(u.joined_at.timestamp())}:R>','bot'),ephemeral=True)

@bot.tree.command(name='avatar',description='Show avatar')
@app_commands.describe(user='Member')
async def avatar(i,user:discord.Member=None):
    if not await guard(i,'avatar'): return
    u=user or i.user; e=E(i.guild,f'{u.display_name} • AVATAR','', 'brand'); e.set_image(url=u.display_avatar.url); await i.response.send_message(embed=e,ephemeral=True)

@bot.tree.command(name='banner',description='Show user banner')
@app_commands.describe(user='Member')
async def banner(i,user:discord.Member=None):
    if not await guard(i,'banner'): return
    u=user or i.user; u=await bot.fetch_user(u.id)
    if not u.banner: return await i.response.send_message(embed=E(i.guild,'NO BANNER',f'{em(i.guild,"error")} This user has no banner.','error'),ephemeral=True)
    e=E(i.guild,f'{u.name} • BANNER','', 'brand'); e.set_image(url=u.banner.url); await i.response.send_message(embed=e,ephemeral=True)

@bot.tree.command(name='roles',description='List server roles')
async def roles(i):
    if await guard(i,'roles'):
        names=[r.mention for r in reversed(i.guild.roles) if r.name!='@everyone']
        await i.response.send_message(embed=E(i.guild,'SERVER ROLES',' '.join(names)[:3900] or 'No roles.','settings'),ephemeral=True)

@bot.tree.command(name='emojis',description='List custom emojis')
async def emojis(i):
    if await guard(i,'emojis'):
        text=' '.join(str(e) for e in i.guild.emojis)
        await i.response.send_message(embed=E(i.guild,'SERVER EMOJIS',text[:3900] or 'No custom emojis found.','brand'),ephemeral=True)

@bot.tree.command(name='say',description='Send a message')
@app_commands.describe(message='Message')
async def say(i,message:str):
    if await guard(i,'say'): await i.response.send_message(message)

@bot.tree.command(name='announce',description='Post an announcement')
@app_commands.describe(title='Title',message='Message')
async def announce(i,title:str,message:str):
    if await guard(i,'announce'): await i.response.send_message(embed=E(i.guild,title,f'{em(i.guild,"fire")} {message}','important'))

@bot.tree.command(name='embed',description='Send a styled embed')
@app_commands.describe(title='Title',message='Message')
async def embed_cmd(i,title:str,message:str):
    if await guard(i,'embed'): await i.response.send_message(embed=E(i.guild,title,message,'brand'))

@bot.tree.command(name='poll',description='Create a yes/no poll')
@app_commands.describe(question='Question')
async def poll(i,question:str):
    if not await guard(i,'poll'): return
    await i.response.send_message(embed=E(i.guild,'POLL',f'{em(i.guild,"help","❓")} {question}\n\n{em(i.guild,"success","✅")} Yes   {em(i.guild,"error","❌")} No','brand'))
    msg=await i.original_response(); await msg.add_reaction('✅'); await msg.add_reaction('❌')

@bot.tree.command(name='botinfo',description='Bot information')
async def botinfo(i):
    if await guard(i,'botinfo'): await i.response.send_message(embed=E(i.guild,'LIGHTNESS',f'{em(i.guild,"crown")} Premium Discord management\n{em(i.guild,"sparkles")} Nitro/custom emoji UI\n{em(i.guild,"moderation")} Anti-nuke protection\n{em(i.guild,"link")} {SERVER_INVITE}','brand'),ephemeral=True)

@bot.tree.command(name='invite',description='Show server invite')
async def invite(i):
    if await guard(i,'invite'): await i.response.send_message(embed=E(i.guild,'SERVER INVITE',f'{em(i.guild,"link")} {SERVER_INVITE}','link'),ephemeral=True)

@bot.tree.command(name='support',description='Support information')
async def support(i):
    if await guard(i,'support'): await i.response.send_message(embed=E(i.guild,'LIGHTNESS SUPPORT',f'{em(i.guild,"support")} Use the ticket panel for help.\n{em(i.guild,"link")} {SERVER_INVITE}','support'),ephemeral=True)

@bot.tree.command(name='channelinfo',description='Channel information')
async def channelinfo(i):
    if await guard(i,'channelinfo'): await i.response.send_message(embed=E(i.guild,'CHANNEL INFO',f'{em(i.guild,"hashy")} {i.channel.mention}\nID: `{i.channel.id}`\nType: `{i.channel.type}`','home'),ephemeral=True)

@bot.tree.command(name='roleinfo',description='Role information')
@app_commands.describe(role='Role')
async def roleinfo(i,role:discord.Role):
    if await guard(i,'roleinfo'): await i.response.send_message(embed=E(i.guild,'ROLE INFO',f'{em(i.guild,"settings")} {role.mention}\nID: `{role.id}`\nMembers: **{len(role.members)}**','settings'),ephemeral=True)

# ---------- Moderation ----------
@bot.tree.command(name='ban',description='Ban member')
@app_commands.describe(member='Member',reason='Reason')
async def ban(i,member:discord.Member,reason:str='No reason provided'):
    if not await guard(i,'ban'): return
    await member.ban(reason=reason); await i.response.send_message(embed=E(i.guild,'USER BANNED',f'{em(i.guild,"ban")} {member.mention}\nReason: {reason}','ban'))

@bot.tree.command(name='unban',description='Unban by user ID')
@app_commands.describe(user_id='User ID',reason='Reason')
async def unban(i,user_id:str,reason:str='No reason provided'):
    if not await guard(i,'unban'): return
    await i.guild.unban(discord.Object(id=int(user_id)),reason=reason); await i.response.send_message(embed=E(i.guild,'USER UNBANNED',f'{em(i.guild,"success")} `{user_id}`','success'))

@bot.tree.command(name='kick',description='Kick member')
@app_commands.describe(member='Member',reason='Reason')
async def kick(i,member:discord.Member,reason:str='No reason provided'):
    if not await guard(i,'kick'): return
    await member.kick(reason=reason); await i.response.send_message(embed=E(i.guild,'USER KICKED',f'{em(i.guild,"kick")} {member.mention}\nReason: {reason}','kick'))

@bot.tree.command(name='warn',description='Warn member')
@app_commands.describe(member='Member',reason='Reason')
async def warn(i,member:discord.Member,reason:str='No reason provided'):
    if not await guard(i,'warn'): return
    data.setdefault('warnings',{}).setdefault(str(member.id),[]).append({'reason':reason,'by':i.user.id,'at':datetime.datetime.now(datetime.timezone.utc).isoformat()});save()
    await i.response.send_message(embed=E(i.guild,'WARNING ISSUED',f'{em(i.guild,"warning")} {member.mention}\n{reason}\nTotal: **{len(data["warnings"][str(member.id)])}**','warning'))

@bot.tree.command(name='warnings',description='View member warnings')
@app_commands.describe(member='Member')
async def warnings(i,member:discord.Member):
    if not await guard(i,'warnings'): return
    ws=data.get('warnings',{}).get(str(member.id),[]); text='\n'.join(f'**{n}.** {x["reason"]}' for n,x in enumerate(ws,1)) or 'No warnings.'
    await i.response.send_message(embed=E(i.guild,'WARNINGS',f'{member.mention}\n{text}','warning'),ephemeral=True)

@bot.tree.command(name='warnings_clear',description='Clear member warnings')
@app_commands.describe(member='Member')
async def warnings_clear(i,member:discord.Member):
    if not await guard(i,'warnings_clear'): return
    data.get('warnings',{}).pop(str(member.id),None);save();await i.response.send_message(embed=E(i.guild,'WARNINGS CLEARED',f'{em(i.guild,"success")} {member.mention}','success'))

@bot.tree.command(name='timeout',description='Timeout member')
@app_commands.describe(member='Member',minutes='Minutes')
async def timeout(i,member:discord.Member,minutes:int):
    if not await guard(i,'timeout'): return
    minutes=max(1,min(minutes,40320)); await member.timeout(datetime.timedelta(minutes=minutes),reason='LIGHTNESS moderation'); await i.response.send_message(embed=E(i.guild,'TIMEOUT',f'{em(i.guild,"mute")} {member.mention} • **{minutes}m**','mute'))

@bot.tree.command(name='untimeout',description='Remove timeout')
@app_commands.describe(member='Member')
async def untimeout(i,member:discord.Member):
    if not await guard(i,'untimeout'): return
    await member.timeout(None);await i.response.send_message(embed=E(i.guild,'TIMEOUT REMOVED',f'{em(i.guild,"success")} {member.mention}','success'))

@bot.tree.command(name='mute',description='Mute member')
@app_commands.describe(member='Member',minutes='Minutes')
async def mute(i,member:discord.Member,minutes:int=10):
    if not await guard(i,'mute'): return
    await member.timeout(datetime.timedelta(minutes=max(1,min(minutes,40320))));await i.response.send_message(embed=E(i.guild,'MUTED',f'{em(i.guild,"mute")} {member.mention}','mute'))

@bot.tree.command(name='unmute',description='Unmute member')
@app_commands.describe(member='Member')
async def unmute(i,member:discord.Member):
    if not await guard(i,'unmute'): return
    await member.timeout(None);await i.response.send_message(embed=E(i.guild,'UNMUTED',f'{em(i.guild,"success")} {member.mention}','success'))

@bot.tree.command(name='purge',description='Delete messages')
@app_commands.describe(amount='1-100')
async def purge(i,amount:int):
    if not await guard(i,'purge'): return
    amount=max(1,min(amount,100));await i.response.defer(ephemeral=True);deleted=await i.channel.purge(limit=amount);await i.followup.send(embed=E(i.guild,'MESSAGES CLEARED',f'{em(i.guild,"moderation")} Deleted **{len(deleted)}**','moderation'),ephemeral=True)

@bot.tree.command(name='slowmode',description='Set channel slowmode')
@app_commands.describe(seconds='0-21600')
async def slowmode(i,seconds:int):
    if not await guard(i,'slowmode'): return
    await i.channel.edit(slowmode_delay=max(0,min(seconds,21600)));await i.response.send_message(embed=E(i.guild,'SLOWMODE UPDATED',f'{em(i.guild,"settings")} **{seconds}s**','settings'))

@bot.tree.command(name='lock',description='Lock channel')
async def lock(i):
    if not await guard(i,'lock'): return
    await i.channel.set_permissions(i.guild.default_role,send_messages=False);await i.response.send_message(embed=E(i.guild,'CHANNEL LOCKED',f'{em(i.guild,"locked")} {i.channel.mention}','locked'))

@bot.tree.command(name='unlock',description='Unlock channel')
async def unlock(i):
    if not await guard(i,'unlock'): return
    await i.channel.set_permissions(i.guild.default_role,send_messages=None);await i.response.send_message(embed=E(i.guild,'CHANNEL UNLOCKED',f'{em(i.guild,"success")} {i.channel.mention}','success'))

# ---------- Tickets ----------
async def get_ticket_category(g):
    cid=state.get('ticket_category'); c=g.get_channel(cid) if cid else None
    if not isinstance(c,discord.CategoryChannel): c=await g.create_category('🎫・LIGHTNESS TICKETS'); state['ticket_category']=c.id;save()
    return c

class TicketView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label='BUY / PURCHASE',style=discord.ButtonStyle.primary,emoji='💎',custom_id='lightness:buy')
    async def buy(self,i,b): await create_ticket(i,'purchase')
    @discord.ui.button(label='SUPPORT',style=discord.ButtonStyle.secondary,emoji='🛟',custom_id='lightness:support')
    async def support_btn(self,i,b): await create_ticket(i,'support')
    @discord.ui.button(label='REPORT',style=discord.ButtonStyle.danger,emoji='🚨',custom_id='lightness:report')
    async def report_btn(self,i,b): await create_ticket(i,'report')
    @discord.ui.button(label='GENERAL HELP',style=discord.ButtonStyle.success,emoji='✨',custom_id='lightness:help')
    async def help_btn(self,i,b): await create_ticket(i,'help')

async def create_ticket(i,kind):
    category=await get_ticket_category(i.guild)
    existing=discord.utils.get(category.text_channels,name=f'{kind}-{i.user.id}')
    if existing: return await i.response.send_message(embed=E(i.guild,'TICKET ALREADY OPEN',f'{em(i.guild,"ticket")} {existing.mention}','ticket'),ephemeral=True)
    overwrites={i.guild.default_role:discord.PermissionOverwrite(view_channel=False),i.user:discord.PermissionOverwrite(view_channel=True,send_messages=True,read_message_history=True)}
    me=i.guild.me
    if me: overwrites[me]=discord.PermissionOverwrite(view_channel=True,send_messages=True,manage_channels=True,manage_messages=True,read_message_history=True)
    ch=await category.create_text_channel(f'{kind}-{i.user.id}',overwrites=overwrites,topic=f'LIGHTNESS ticket • {kind} • {i.user.id}')
    e=E(i.guild,f'{kind.upper()} TICKET',f'{em(i.guild,"ticket")} Welcome {i.user.mention}!\n{em(i.guild,"support")} Explain what you need and staff will help you.\n{em(i.guild,"close")} Use `/ticket_close` when finished.','ticket')
    await ch.send(content=i.user.mention,embed=e)
    await i.response.send_message(embed=E(i.guild,'TICKET CREATED',f'{em(i.guild,"success")} {ch.mention}','success'),ephemeral=True)

@bot.tree.command(name='ticket_panel',description='Post animated ticket panel')
async def ticket_panel(i):
    if not await guard(i,'ticket_panel'): return
    e=E(i.guild,'LIGHTNESS • SUPPORT CENTER',f'{em(i.guild,"brand")} Choose a service below.\n\n{em(i.guild,"buy")} **BUY / PURCHASE**\n{em(i.guild,"support")} **SUPPORT**\n{em(i.guild,"report")} **REPORT**\n{em(i.guild,"help")} **GENERAL HELP**\n\n{em(i.guild,"star")} Fast • clean • permission protected','brand')
    await i.response.send_message(embed=e,view=TicketView())

@bot.tree.command(name='ticket_setup',description='Create ticket category')
async def ticket_setup(i):
    if not await guard(i,'ticket_setup'): return
    c=await get_ticket_category(i.guild);await i.response.send_message(embed=E(i.guild,'TICKET SYSTEM READY',f'{em(i.guild,"success")} Category: {c.mention}\n{em(i.guild,"ticket")} Run `/ticket_panel` to post the panel.','ticket'),ephemeral=True)

def current_ticket(i): return i.channel if isinstance(i.channel,discord.TextChannel) and i.channel.category_id==state.get('ticket_category') else None

@bot.tree.command(name='ticket_close',description='Close current ticket')
async def ticket_close(i):
    if not await guard(i,'ticket_close'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message(embed=E(i.guild,'NOT A TICKET',f'{em(i.guild,"error")} Use this inside a ticket.','error'),ephemeral=True)
    await ch.set_permissions(i.guild.default_role,view_channel=False);await i.response.send_message(embed=E(i.guild,'TICKET CLOSED',f'{em(i.guild,"locked")} Ticket locked. Use `/ticket_reopen` if needed.','locked'))

@bot.tree.command(name='ticket_reopen',description='Reopen current ticket')
async def ticket_reopen(i):
    if not await guard(i,'ticket_reopen'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message(embed=E(i.guild,'NOT A TICKET','Use this inside a ticket.','error'),ephemeral=True)
    await ch.set_permissions(i.guild.default_role,view_channel=False);await i.response.send_message(embed=E(i.guild,'TICKET REOPEN',f'{em(i.guild,"success")} Ask the ticket owner/staff to restore access if required.','success'))

@bot.tree.command(name='ticket_add',description='Add member to ticket')
@app_commands.describe(user='Member')
async def ticket_add(i,user:discord.Member):
    if not await guard(i,'ticket_add'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await ch.set_permissions(user,view_channel=True,send_messages=True,read_message_history=True);await i.response.send_message(embed=E(i.guild,'MEMBER ADDED',f'{em(i.guild,"success")} {user.mention}','success'))

@bot.tree.command(name='ticket_remove',description='Remove member from ticket')
@app_commands.describe(user='Member')
async def ticket_remove(i,user:discord.Member):
    if not await guard(i,'ticket_remove'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await ch.set_permissions(user,view_channel=False);await i.response.send_message(embed=E(i.guild,'MEMBER REMOVED',f'{em(i.guild,"error")} {user.mention}','error'))

@bot.tree.command(name='ticket_rename',description='Rename current ticket')
@app_commands.describe(name='New name')
async def ticket_rename(i,name:str):
    if not await guard(i,'ticket_rename'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await ch.edit(name=name[:90]);await i.response.send_message(embed=E(i.guild,'TICKET RENAMED',f'{em(i.guild,"success")} `{name[:90]}`','success'))

@bot.tree.command(name='ticket_claim',description='Claim ticket')
async def ticket_claim(i):
    if not await guard(i,'ticket_claim'): return
    if not current_ticket(i): return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await i.response.send_message(embed=E(i.guild,'TICKET CLAIMED',f'{em(i.guild,"crown")} Claimed by {i.user.mention}.','owner'))

@bot.tree.command(name='ticket_unclaim',description='Unclaim ticket')
async def ticket_unclaim(i):
    if not await guard(i,'ticket_unclaim'): return
    if not current_ticket(i): return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await i.response.send_message(embed=E(i.guild,'TICKET UNCLAIMED',f'{em(i.guild,"success")} Ticket is available again.','success'))

@bot.tree.command(name='ticket_transcript',description='Create a simple ticket transcript')
async def ticket_transcript(i):
    if not await guard(i,'ticket_transcript'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    lines=[]
    async for m in ch.history(limit=100,oldest_first=True): lines.append(f'[{m.created_at:%Y-%m-%d %H:%M}] {m.author}: {m.content}')
    text='\n'.join(lines)[-1800:] or 'No messages.'
    await i.response.send_message(embed=E(i.guild,'TICKET TRANSCRIPT',f'```text\n{text}\n```','ticket'),ephemeral=True)

@bot.tree.command(name='ticket_lock',description='Lock current ticket')
async def ticket_lock(i):
    if not await guard(i,'ticket_lock'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await ch.set_permissions(i.guild.default_role,send_messages=False);await i.response.send_message(embed=E(i.guild,'TICKET LOCKED',f'{em(i.guild,"locked")} {ch.mention}','locked'))

@bot.tree.command(name='ticket_unlock',description='Unlock current ticket')
async def ticket_unlock(i):
    if not await guard(i,'ticket_unlock'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await ch.set_permissions(i.guild.default_role,send_messages=None);await i.response.send_message(embed=E(i.guild,'TICKET UNLOCKED',f'{em(i.guild,"success")} {ch.mention}','success'))

@bot.tree.command(name='ticket_delete',description='Delete current ticket')
async def ticket_delete(i):
    if not await guard(i,'ticket_delete'): return
    ch=current_ticket(i)
    if not ch:return await i.response.send_message('Use inside a ticket.',ephemeral=True)
    await i.response.send_message(embed=E(i.guild,'DELETING TICKET',f'{em(i.guild,"loading")} Closing in **3 seconds**...','close'));await asyncio.sleep(3);await ch.delete(reason='LIGHTNESS ticket delete')

# ---------- Reports ----------
@bot.tree.command(name='report_setup',description='Set report channel to current channel')
async def report_setup(i):
    if not await guard(i,'report_setup'): return
    state['report_channel']=i.channel.id;save();await i.response.send_message(embed=E(i.guild,'REPORT SYSTEM READY',f'{em(i.guild,"success")} Reports will be sent to {i.channel.mention}.','report'),ephemeral=True)

@bot.tree.command(name='report',description='Report a member')
@app_commands.describe(member='Member',reason='Reason')
async def report(i,member:discord.Member,reason:str):
    if not await guard(i,'report'): return
    cid=state.get('report_channel'); ch=i.guild.get_channel(cid) if cid else None
    if not ch: return await i.response.send_message(embed=E(i.guild,'REPORT NOT CONFIGURED',f'{em(i.guild,"settings")} Run `/report_setup` first.','warning'),ephemeral=True)
    e=E(i.guild,'NEW REPORT',f'{em(i.guild,"report")} Reporter: {i.user.mention}\nTarget: {member.mention}\nReason: **{reason}**','report');await ch.send(embed=e);await i.response.send_message(embed=E(i.guild,'REPORT SENT',f'{em(i.guild,"success")} Staff has received the report.','success'),ephemeral=True)

@bot.tree.command(name='report_list',description='List recent reports')
async def report_list(i):
    if not await guard(i,'report_list'): return
    ch=i.guild.get_channel(state.get('report_channel')) if state.get('report_channel') else None
    await i.response.send_message(embed=E(i.guild,'REPORT CENTER',f'{em(i.guild,"report")} Channel: {ch.mention if ch else "Not configured"}\nUse `/report` to create a report.','report'),ephemeral=True)

@bot.tree.command(name='report_view',description='View report center')
async def report_view(i):
    if await guard(i,'report_view'):
        channel_text = f'<#{state["report_channel"]}>' if state.get('report_channel') else 'Not configured'
        await i.response.send_message(embed=E(i.guild,'REPORT VIEW',f'{em(i.guild,"report")} Current report channel: {channel_text}','report'),ephemeral=True)

@bot.tree.command(name='report_close',description='Close current report channel')
async def report_close(i):
    if not await guard(i,'report_close'): return
    await i.response.send_message(embed=E(i.guild,'REPORT CLOSED',f'{em(i.guild,"locked")} Marked as handled by {i.user.mention}.','locked'))

@bot.tree.command(name='report_claim',description='Claim a report')
async def report_claim(i):
    if not await guard(i,'report_claim'): return
    await i.response.send_message(embed=E(i.guild,'REPORT CLAIMED',f'{em(i.guild,"crown")} {i.user.mention} claimed this report.','owner'))

@bot.tree.command(name='report_delete',description='Delete current report channel')
async def report_delete(i):
    if not await guard(i,'report_delete'): return
    await i.response.send_message(embed=E(i.guild,'REPORT DELETE',f'{em(i.guild,"warning")} Use Discord channel management to permanently remove a report channel.','warning'),ephemeral=True)

# ---------- Welcome / Goodbye ----------
@bot.tree.command(name='welcome_setup',description='Set current channel for welcomes')
async def welcome_setup(i):
    if not await guard(i,'welcome_setup'): return
    state['welcome_channel']=i.channel.id;save();await i.response.send_message(embed=E(i.guild,'WELCOME READY',f'{em(i.guild,"welcome")} New members will be welcomed in {i.channel.mention}.','welcome'),ephemeral=True)

@bot.tree.command(name='welcome_test',description='Test welcome message')
async def welcome_test(i):
    if not await guard(i,'welcome_test'): return
    await i.response.send_message(embed=E(i.guild,'WELCOME TO LIGHTNESS',f'{em(i.guild,"welcome")} Welcome {i.user.mention}!\n{em(i.guild,"sparkles")} Enjoy the server and open a ticket if you need help.','welcome'))

@bot.tree.command(name='welcome_disable',description='Disable welcome messages')
async def welcome_disable(i):
    if not await guard(i,'welcome_disable'): return
    state['welcome_channel']=None;save();await i.response.send_message(embed=E(i.guild,'WELCOME DISABLED',f'{em(i.guild,"locked")} Welcome messages are off.','locked'),ephemeral=True)

@bot.tree.command(name='goodbye_setup',description='Set current channel for goodbye messages')
async def goodbye_setup(i):
    if not await guard(i,'goodbye_setup'): return
    state['goodbye_channel']=i.channel.id;save();await i.response.send_message(embed=E(i.guild,'GOODBYE READY',f'{em(i.guild,"home")} Goodbye messages will be sent in {i.channel.mention}.','home'),ephemeral=True)

@bot.tree.command(name='goodbye_test',description='Test goodbye message')
async def goodbye_test(i):
    if not await guard(i,'goodbye_test'): return
    await i.response.send_message(embed=E(i.guild,'GOODBYE TEST',f'{em(i.guild,"home")} Goodbye test message.','home'),ephemeral=True)

@bot.event
async def on_member_join(member):
    ch=member.guild.get_channel(state.get('welcome_channel')) if state.get('welcome_channel') else None
    if ch:
        try: await ch.send(embed=E(member.guild,'WELCOME',f'{em(member.guild,"welcome")} Welcome {member.mention} to **{member.guild.name}**!\n{em(member.guild,"sparkles")} Have fun and enjoy the community.','welcome'))
        except: pass

@bot.event
async def on_member_remove(member):
    ch=member.guild.get_channel(state.get('goodbye_channel')) if state.get('goodbye_channel') else None
    if ch:
        try: await ch.send(embed=E(member.guild,'MEMBER LEFT',f'{em(member.guild,"home")} **{member.display_name}** has left the server.','home'))
        except: pass

# ---------- Giveaways ----------
class GiveawayView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label='ENTER GIVEAWAY',style=discord.ButtonStyle.success,emoji='🎁',custom_id='lightness:giveaway_enter')
    async def enter(self,i,b):
        gid=str(i.message.id); g=state.setdefault('giveaways',{}).get(gid)
        if not g or g.get('ended'): return await i.response.send_message('This giveaway has ended.',ephemeral=True)
        if i.user.id not in g['entries']: g['entries'].append(i.user.id);save();msg='Entry added!'
        else: msg='You are already entered.'
        await i.response.send_message(f'{em(i.guild,"premium","💎")} {msg}',ephemeral=True)

@bot.tree.command(name='giveaway_start',description='Start a giveaway')
@app_commands.describe(prize='Prize',minutes='Duration in minutes')
async def giveaway_start(i,prize:str,minutes:int):
    if not await guard(i,'giveaway_start'): return
    minutes=max(1,min(minutes,10080));end=datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=minutes)
    e=E(i.guild,'GIVEAWAY',f'{em(i.guild,"premium")} Prize: **{prize}**\n{em(i.guild,"loading")} Ends: <t:{int(end.timestamp())}:R>\n\n{em(i.guild,"star")} Click **ENTER GIVEAWAY** below!','premium')
    await i.response.send_message(embed=e,view=GiveawayView());msg=await i.original_response();state['giveaways'][str(msg.id)]={'prize':prize,'entries':[],'ended':False,'channel':i.channel.id,'end':end.isoformat()};save()
    await asyncio.sleep(minutes*60)
    g=state['giveaways'].get(str(msg.id));
    if g and not g['ended']:
        g['ended']=True;save();
        if g['entries']:
            winner=random.choice(g['entries']); await i.channel.send(embed=E(i.guild,'GIVEAWAY ENDED',f'{em(i.guild,"success")} Winner: <@{winner}>\nPrize: **{prize}**','success'))
        else: await i.channel.send(embed=E(i.guild,'GIVEAWAY ENDED',f'{em(i.guild,"error")} No entries.','error'))

@bot.tree.command(name='giveaway_end',description='End a giveaway by message ID')
@app_commands.describe(message_id='Giveaway message ID')
async def giveaway_end(i,message_id:str):
    if not await guard(i,'giveaway_end'): return
    g=state.get('giveaways',{}).get(message_id)
    if not g:return await i.response.send_message('Giveaway not found.',ephemeral=True)
    g['ended']=True;save();winner=random.choice(g['entries']) if g['entries'] else None;await i.response.send_message(embed=E(i.guild,'GIVEAWAY ENDED',f'{em(i.guild,"success")} Winner: {f"<@{winner}>" if winner else "No entries."}','success'))

@bot.tree.command(name='giveaway_reroll',description='Reroll a giveaway')
@app_commands.describe(message_id='Giveaway message ID')
async def giveaway_reroll(i,message_id:str):
    if not await guard(i,'giveaway_reroll'): return
    g=state.get('giveaways',{}).get(message_id)
    if not g or not g['entries']: return await i.response.send_message('No eligible entries.',ephemeral=True)
    await i.response.send_message(embed=E(i.guild,'GIVEAWAY REROLL',f'{em(i.guild,"premium")} New winner: <@{random.choice(g["entries"])}>','premium'))

@bot.tree.command(name='giveaway_list',description='List giveaways')
async def giveaway_list(i):
    if not await guard(i,'giveaway_list'): return
    gs=state.get('giveaways',{});text='\n'.join(f'`{k}` • **{v["prize"]}** • {len(v["entries"])} entries • {"ended" if v["ended"] else "active"}' for k,v in list(gs.items())[-10:]) or 'No giveaways.';await i.response.send_message(embed=E(i.guild,'GIVEAWAYS',text,'premium'),ephemeral=True)

# ---------- Access ----------
@bot.tree.command(name='access',description='OWNER: grant/remove/list command access')
@app_commands.describe(action='add/remove/list/check/all',user='Member',command='Command name')
@app_commands.choices(action=[app_commands.Choice(name=x,value=x) for x in ['add','remove','list','check','all']])
async def access(i,action:str,user:discord.Member=None,command:str=None):
    if not await owner_guard(i): return
    users=data.setdefault('users',{})
    if action=='list':
        text='\n'.join(f'<@{uid}> — **{len(cs)}** commands' for uid,cs in users.items()) or 'No custom access.'
        return await i.response.send_message(embed=E(i.guild,'ACCESS LIST',text,'owner'),ephemeral=True)
    if not user:return await i.response.send_message('Select a user.',ephemeral=True)
    key=str(user.id)
    if action=='all': users[key]=COMMANDS.copy(); msg='All commands granted.'
    elif action=='check': msg=', '.join('/'+x for x in users.get(key,[])) or 'No permissions.'
    elif action=='add':
        c=(command or '').lower().lstrip('/')
        if c not in COMMANDS:return await i.response.send_message(f'Invalid command. Use `/help`.',ephemeral=True)
        users.setdefault(key,[])
        if c not in users[key]: users[key].append(c)
        msg=f'/{c} granted.'
    else:
        c=(command or '').lower().lstrip('/')
        if c=='all': users.pop(key,None);msg='All custom permissions removed.'
        else: users.setdefault(key,[]);users[key]=[x for x in users[key] if x!=c];msg=f'/{c} removed.'
    save();await i.response.send_message(embed=E(i.guild,'ACCESS UPDATED',f'{em(i.guild,"owner")} {user.mention}\n{msg}','owner'),ephemeral=True)

# ---------- Anti-nuke ----------
async def audit_actor(guild, action, limit, reason):
    if not state.setdefault('security',{}).get('enabled',True): return
    try:
        entries=[]
        async for entry in guild.audit_logs(limit=10,action=action): entries.append(entry)
        if not entries:return
        now=datetime.datetime.now(datetime.timezone.utc)
        for entry in entries:
            if entry.user and entry.user.id!=bot.user.id and not owner(entry.user.id) and entry.user.id not in state['security'].get('whitelist',[]):
                # If several recent matching actions exist, timeout the actor defensively.
                recent=[x for x in entries if x.user and x.user.id==entry.user.id and (now-x.created_at).total_seconds()<15]
                if len(recent)>=limit:
                    m=guild.get_member(entry.user.id)
                    if m:
                        try: await m.timeout(datetime.timedelta(hours=1),reason=reason)
                        except: pass
                    return
    except Exception as ex: print('security:',ex)

@bot.event
async def on_guild_channel_delete(channel): await audit_actor(channel.guild,discord.AuditLogAction.channel_delete,3,'LIGHTNESS Anti-Nuke: repeated channel deletion')
@bot.event
async def on_guild_role_delete(role): await audit_actor(role.guild,discord.AuditLogAction.role_delete,3,'LIGHTNESS Anti-Nuke: repeated role deletion')
@bot.event
async def on_guild_channel_create(channel): await audit_actor(channel.guild,discord.AuditLogAction.channel_create,5,'LIGHTNESS Anti-Nuke: repeated channel creation')
@bot.event
async def on_guild_role_create(role): await audit_actor(role.guild,discord.AuditLogAction.role_create,5,'LIGHTNESS Anti-Nuke: repeated role creation')

@bot.tree.command(name='lockdown',description='OWNER: emergency lockdown')
async def lockdown(i):
    if not await owner_guard(i): return
    for ch in i.guild.text_channels:
        try: await ch.set_permissions(i.guild.default_role,send_messages=False)
        except: pass
    await i.response.send_message(embed=E(i.guild,'EMERGENCY LOCKDOWN',f'{em(i.guild,"locked","🔒")} Server channels locked.','locked'))

@bot.tree.command(name='unlockdown',description='OWNER: lift lockdown')
async def unlockdown(i):
    if not await owner_guard(i): return
    for ch in i.guild.text_channels:
        try: await ch.set_permissions(i.guild.default_role,send_messages=None)
        except: pass
    await i.response.send_message(embed=E(i.guild,'LOCKDOWN LIFTED',f'{em(i.guild,"success","✅")} Normal permissions restored where possible.','success'))

@bot.tree.command(name='security_setup',description='OWNER: security status')
async def security_setup(i):
    if not await owner_guard(i): return
    wl=state.setdefault('security',{}).get('whitelist',[]);await i.response.send_message(embed=E(i.guild,'LIGHTNESS SECURITY',f'{em(i.guild,"moderation")} Anti-nuke: **ON**\n{em(i.guild,"warning")} Channel delete threshold: **3 / 15s**\n{em(i.guild,"warning")} Role delete threshold: **3 / 15s**\n{em(i.guild,"owner")} Whitelisted IDs: **{len(wl)}**','moderation'),ephemeral=True)

@bot.tree.command(name='security_whitelist_add',description='OWNER: whitelist user')
@app_commands.describe(user='Member')
async def security_whitelist_add(i,user:discord.Member):
    if not await owner_guard(i): return
    wl=state.setdefault('security',{}).setdefault('whitelist',[])
    if user.id not in wl: wl.append(user.id);save()
    await i.response.send_message(embed=E(i.guild,'SECURITY WHITELIST',f'{em(i.guild,"success")} Added {user.mention}.','success'),ephemeral=True)

@bot.tree.command(name='security_whitelist_remove',description='OWNER: remove whitelist user')
@app_commands.describe(user='Member')
async def security_whitelist_remove(i,user:discord.Member):
    if not await owner_guard(i): return
    wl=state.setdefault('security',{}).setdefault('whitelist',[])
    if user.id in wl: wl.remove(user.id);save()
    await i.response.send_message(embed=E(i.guild,'SECURITY WHITELIST',f'{em(i.guild,"error")} Removed {user.mention}.','warning'),ephemeral=True)

@bot.tree.command(name='security_whitelist_list',description='OWNER: list whitelist')
async def security_whitelist_list(i):
    if not await owner_guard(i): return
    wl=state.setdefault('security',{}).get('whitelist',[]);await i.response.send_message(embed=E(i.guild,'SECURITY WHITELIST','\n'.join(f'<@{x}>' for x in wl) or 'No extra users.','owner'),ephemeral=True)

if not TOKEN: raise RuntimeError('DISCORD_TOKEN is missing. Add it in Railway Variables.')
bot.run(TOKEN)
