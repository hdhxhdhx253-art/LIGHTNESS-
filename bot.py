import os, json, datetime
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
TOKEN=os.getenv("DISCORD_TOKEN")
OWNER_ID=1433457392917676138
GUILD_ID=1544039840767803412
PERM_FILE="permissions.json"

# Emoji IDs are entered ONCE here. Names do not matter.
EMOJI_IDS={
"arrow":1549136782971379712,"crown":1549137817341268058,"butterfly":1549136722686644336,
"loading":1549136416250921060,"dot":1544406593351844012,"fire":1549138871537639507,
"hashy":1544406358152061038,"verify":1549136346902175754,"kick":1549138352618471434,
"banned":1549138249988182147,"bot":1549139254712606830,"dance":1549138072694689943,
"confuse":1549137286925648012,"diamond":1549139140803563644,"error":1549136020094717982,
"hammer":1549138507539288126,"help":1549139550134075513,"link":1549139611123449997,
"home":1549139446950269060,"mute":1549138714624655450,"heart":1549139076580511804,
"star":1549138951413956631,"sparkles":1549138777660850216,"special":1549136671260278896,
"support":1544406094451974173,"lock":1549137685954953318,"warn":1549136157898575942,
"settings":1549139334425219163}
ROLE={"welcome":"butterfly","brand":"sparkles","loading":"loading","owner":"crown","premium":"diamond",
"success":"verify","error":"error","warning":"warn","locked":"lock","moderation":"hammer","ban":"banned",
"kick":"kick","mute":"mute","help":"help","settings":"settings","support":"support","ticket":"support",
"buy":"diamond","report":"warn","close":"lock","important":"star","fire":"fire","link":"link","home":"home","bot":"bot"}
COMMANDS=["ping","help","server","userinfo","avatar","banner","roles","emojis","say","announce","embed","poll",
"ban","unban","kick","warn","warnings","warnings_clear","timeout","untimeout","mute","unmute","purge","slowmode",
"lock","unlock","ticket_panel","ticket_setup","ticket_close","ticket_reopen","ticket_add","ticket_remove",
"ticket_rename","ticket_claim","ticket_unclaim","ticket_transcript","ticket_lock","ticket_unlock","ticket_delete",
"report","report_setup","report_list","report_view","report_close","report_claim","report_delete",
"welcome_setup","welcome_test","welcome_disable","goodbye_setup","goodbye_test",
"giveaway_start","giveaway_end","giveaway_reroll","giveaway_list","botinfo","invite","support","channelinfo","roleinfo","permissions"]
def load():
    try:return json.load(open(PERM_FILE,encoding="utf8"))
    except:return {"users":{},"warnings":{}}
data=load()
def save():json.dump(data,open(PERM_FILE,"w",encoding="utf8"),indent=2)
def owner(uid):return uid==OWNER_ID
def allowed(uid,c):return owner(uid) or c in data.get("users",{}).get(str(uid),[])
def em(g,role,fb="✨"):
    x=EMOJI_IDS.get(ROLE.get(role,role))
    o=g.get_emoji(x) if g and x else None
    return str(o) if o else fb
def embed(g,title,desc,role="success"):
    return discord.Embed(title=f"{em(g,role)} {title}",description=desc,color=0xD4AF37)
async def guard(i,c):
    if allowed(i.user.id,c):return True
    await i.response.send_message(embed=embed(i.guild,"ACCESS DENIED",f"{em(i.guild,'error','❌')} **You don't have permission to use this command.**\n\n{em(i.guild,'owner','👑')} Ask the LIGHTNESS owner for access.\n{em(i.guild,'link','🔗')} discord.gg/FtxqMbBs","locked"),ephemeral=True)
    return False
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!",intents=discord.Intents.all())
    async def setup_hook(self):
        g=discord.Object(id=GUILD_ID);self.tree.copy_global_to(guild=g);await self.tree.sync(guild=g)
bot=Bot()
@bot.event
async def on_ready():print(f"LIGHTNESS online as {bot.user} | guild={GUILD_ID}")

@bot.tree.command(name="ping",description="Check latency")
async def ping(i):
    if await guard(i,"ping"):await i.response.send_message(embed=embed(i.guild,"LIGHTNESS ONLINE",f"{em(i.guild,'success','✅')} **{round(bot.latency*1000)}ms**","bot"))
@bot.tree.command(name="help",description="Command center")
async def help(i):
    if not await guard(i,"help"):return
    e=embed(i.guild,"LIGHTNESS COMMAND CENTER",f"{em(i.guild,'brand')} Premium server control\n{em(i.guild,'fire')} discord.gg/FtxqMbBs","brand")
    e.add_field(name="General",value="`/ping` `/server` `/userinfo` `/avatar` `/banner` `/roles` `/emojis` `/botinfo` `/invite` `/support`",inline=False)
    e.add_field(name="Moderation",value="`/ban` `/unban` `/kick` `/warn` `/warnings` `/timeout` `/untimeout` `/mute` `/unmute` `/purge` `/slowmode` `/lock` `/unlock`",inline=False)
    e.add_field(name="Ticket",value="`/ticket_panel` `/ticket_setup` `/ticket_close` `/ticket_reopen` `/ticket_add` `/ticket_remove` `/ticket_rename` `/ticket_claim` `/ticket_transcript`",inline=False)
    e.add_field(name="Report / Welcome / Giveaway",value="`/report` `/report_setup` `/report_list` `/report_close` `/welcome_setup` `/welcome_test` `/welcome_disable` `/giveaway_start` `/giveaway_end` `/giveaway_reroll`",inline=False)
    e.add_field(name="Owner",value="`/access` is replaced by the owner-only `/access` command below.",inline=False)
    await i.response.send_message(embed=e,ephemeral=True)
@bot.tree.command(name="server",description="Server info")
async def server(i):
    if await guard(i,"server"):await i.response.send_message(embed=embed(i.guild,i.guild.name,f"{em(i.guild,'home')} Members: **{i.guild.member_count}**\nID: `{i.guild.id}`","home"),ephemeral=True)
@bot.tree.command(name="userinfo",description="User info")
@app_commands.describe(user="Member")
async def userinfo(i,user:discord.Member=None):
    if await guard(i,"userinfo"):
        u=user or i.user;await i.response.send_message(embed=embed(i.guild,"USER INFO",f"{em(i.guild,'bot')} {u.mention}\nID: `{u.id}`","bot"),ephemeral=True)
@bot.tree.command(name="avatar",description="Show avatar")
@app_commands.describe(user="Member")
async def avatar(i,user:discord.Member=None):
    if not await guard(i,"avatar"):return
    u=user or i.user;e=embed(i.guild,f"{u.display_name} • AVATAR","","brand");e.set_image(url=u.display_avatar.url);await i.response.send_message(embed=e,ephemeral=True)
@bot.tree.command(name="botinfo",description="Bot info")
async def botinfo(i):
    if await guard(i,"botinfo"):await i.response.send_message(embed=embed(i.guild,"LIGHTNESS",f"{em(i.guild,'owner')} Premium Discord management\n{em(i.guild,'brand')} Animated emoji system\n{em(i.guild,'link')} discord.gg/FtxqMbBs","brand"),ephemeral=True)
@bot.tree.command(name="invite",description="Server invite")
async def invite(i):
    if await guard(i,"invite"):await i.response.send_message(embed=embed(i.guild,"LIGHTNESS SERVER",f"{em(i.guild,'link')} discord.gg/FtxqMbBs","link"),ephemeral=True)
@bot.tree.command(name="support",description="Support")
async def support(i):
    if await guard(i,"support"):await i.response.send_message(embed=embed(i.guild,"LIGHTNESS SUPPORT",f"{em(i.guild,'support')} discord.gg/FtxqMbBs","support"),ephemeral=True)
@bot.tree.command(name="say",description="Send message")
@app_commands.describe(message="Message")
async def say(i,message:str):
    if await guard(i,"say"):await i.response.send_message(message)
@bot.tree.command(name="announce",description="Announcement")
@app_commands.describe(title="Title",message="Message")
async def announce(i,title:str,message:str):
    if await guard(i,"announce"):await i.response.send_message(embed=embed(i.guild,title,message,"important"))
@bot.tree.command(name="ban",description="Ban member")
@app_commands.describe(member="Member",reason="Reason")
async def ban(i,member:discord.Member,reason:str="No reason provided"):
    if not await guard(i,"ban"):return
    await member.ban(reason=reason);await i.response.send_message(embed=embed(i.guild,"USER BANNED",f"{em(i.guild,'ban')} {member.mention}\n{reason}","ban"))
@bot.tree.command(name="kick",description="Kick member")
@app_commands.describe(member="Member",reason="Reason")
async def kick(i,member:discord.Member,reason:str="No reason provided"):
    if not await guard(i,"kick"):return
    await member.kick(reason=reason);await i.response.send_message(embed=embed(i.guild,"USER KICKED",f"{em(i.guild,'kick')} {member.mention}\n{reason}","kick"))
@bot.tree.command(name="timeout",description="Timeout member")
@app_commands.describe(member="Member",minutes="Minutes")
async def timeout(i,member:discord.Member,minutes:int):
    if not await guard(i,"timeout"):return
    minutes=max(1,min(minutes,40320));await member.timeout(datetime.timedelta(minutes=minutes));await i.response.send_message(embed=embed(i.guild,"TIMEOUT",f"{em(i.guild,'mute')} {member.mention} • {minutes}m","mute"))
@bot.tree.command(name="purge",description="Delete messages")
@app_commands.describe(amount="1-100")
async def purge(i,amount:int):
    if not await guard(i,"purge"):return
    amount=max(1,min(amount,100));await i.response.defer(ephemeral=True);d=await i.channel.purge(limit=amount);await i.followup.send(embed=embed(i.guild,"MESSAGES CLEARED",f"{em(i.guild,'moderation')} Deleted **{len(d)}**","moderation"),ephemeral=True)
@bot.tree.command(name="lock",description="Lock channel")
async def lock(i):
    if not await guard(i,"lock"):return
    await i.channel.set_permissions(i.guild.default_role,send_messages=False);await i.response.send_message(embed=embed(i.guild,"CHANNEL LOCKED",f"{em(i.guild,'locked')} {i.channel.mention}","locked"))
@bot.tree.command(name="unlock",description="Unlock channel")
async def unlock(i):
    if not await guard(i,"unlock"):return
    await i.channel.set_permissions(i.guild.default_role,send_messages=None);await i.response.send_message(embed=embed(i.guild,"CHANNEL UNLOCKED",f"{em(i.guild,'success')} {i.channel.mention}","success"))

class TicketView(discord.ui.View):
    def __init__(self):super().__init__(timeout=None)
    @discord.ui.button(label="BUY / PURCHASE",style=discord.ButtonStyle.primary,custom_id="lightness:buy")
    async def buy(self,i,b):await i.response.send_message(f"{em(i.guild,'buy','💎')} Purchase request received.",ephemeral=True)
    @discord.ui.button(label="SUPPORT",style=discord.ButtonStyle.secondary,custom_id="lightness:support")
    async def sup(self,i,b):await i.response.send_message(f"{em(i.guild,'support','🛟')} Support request received.",ephemeral=True)
    @discord.ui.button(label="REPORT",style=discord.ButtonStyle.danger,custom_id="lightness:report")
    async def rep(self,i,b):await i.response.send_message(f"{em(i.guild,'report','🚨')} Report request received.",ephemeral=True)
    @discord.ui.button(label="GENERAL HELP",style=discord.ButtonStyle.success,custom_id="lightness:general")
    async def gen(self,i,b):await i.response.send_message(f"{em(i.guild,'help','❓')} General help request received.",ephemeral=True)

@bot.tree.command(name="ticket_panel",description="Post ticket panel")
async def ticket_panel(i):
    if not await guard(i,"ticket_panel"):return
    e=embed(i.guild,"LIGHTNESS SUPPORT CENTER",f"{em(i.guild,'brand')} Choose your service.\n\n{em(i.guild,'buy')} **BUY / PURCHASE**\n{em(i.guild,'support')} **SUPPORT**\n{em(i.guild,'report')} **REPORT**\n{em(i.guild,'help')} **GENERAL HELP**","brand")
    await i.response.send_message(embed=e,view=TicketView())

@bot.tree.command(name="access",description="OWNER: manage user command access")
@app_commands.describe(action="add/remove/list/check/all",user="Member",command="Command name")
@app_commands.choices(action=[app_commands.Choice(name=x,value=x) for x in ["add","remove","list","check","all"]])
async def access(i,action:str,user:discord.Member=None,command:str=None):
    if not owner(i.user.id):await i.response.send_message(embed=embed(i.guild,"ACCESS DENIED","Owner only.","locked"),ephemeral=True);return
    users=data.setdefault("users",{})
    if action=="list":
        text="\n".join(f"<@{uid}> — `{len(cs)}` commands" for uid,cs in users.items()) or "No users."
        return await i.response.send_message(embed=embed(i.guild,"ACCESS LIST",text,"owner"),ephemeral=True)
    if not user:return await i.response.send_message("Select a user.",ephemeral=True)
    key=str(user.id)
    if action=="all":users[key]=COMMANDS.copy();msg="All commands granted."
    elif action=="check":msg=", ".join("/"+x for x in users.get(key,[])) or "No permissions."
    elif action=="add":
        c=(command or "").lower().lstrip("/")
        if c not in COMMANDS:return await i.response.send_message("Invalid command.",ephemeral=True)
        users.setdefault(key,[])
        if c not in users[key]:users[key].append(c)
        msg=f"/{c} granted."
    else:
        c=(command or "").lower().lstrip("/")
        if c=="all":users.pop(key,None);msg="All permissions removed."
        else:users.setdefault(key,[]);users[key]=[x for x in users[key] if x!=c];msg=f"/{c} removed."
    save();await i.response.send_message(embed=embed(i.guild,"ACCESS UPDATED",f"{em(i.guild,'owner')} {user.mention}\n{msg}","owner"),ephemeral=True)

# Permission-protected module commands; safe placeholders until their full workflows are implemented.
MODULES=["ticket_setup","ticket_close","ticket_reopen","ticket_add","ticket_remove","ticket_rename","ticket_claim","ticket_unclaim","ticket_transcript","ticket_lock","ticket_unlock","ticket_delete","report","report_setup","report_list","report_view","report_close","report_claim","report_delete","welcome_setup","welcome_test","welcome_disable","goodbye_setup","goodbye_test","giveaway_start","giveaway_end","giveaway_reroll","giveaway_list"]
def make_module(n):
    async def f(i):
        if await guard(i,n):await i.response.send_message(embed=embed(i.guild,"LIGHTNESS MODULE",f"{em(i.guild,'loading')} `{n}` permission is active. Full workflow can be enabled in the next update.","brand"),ephemeral=True)
    f.__name__=n
    return bot.tree.command(name=n,description=f"LIGHTNESS {n.replace('_',' ')}")(f)
for n in MODULES:make_module(n)

if not TOKEN:raise RuntimeError("DISCORD_TOKEN is missing. Add it in Railway Variables.")
bot.run(TOKEN)
