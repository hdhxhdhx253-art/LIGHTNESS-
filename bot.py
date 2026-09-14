import os, json, asyncio
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = 1433457392917676138
GUILD_ID = 1544039840767803412
PREFIX = "!"

PERM_FILE = "permissions.json"

EMOJIS = {
    "arrow": "<a:Arrow_White:1549136782971379712>",
    "crown": "<a:BS_crown:1549137817341268058>",
    "butterfly": "<a:CH_Butterfly:1549136722686644336>",
    "loading": "<a:CH_IconLoading:1549136416250921060>",
    "dot": "<a:DOT:1544406593351844012>",
    "fire": "<a:Fire:1549138871537639507>",
    "hashy": "<a:HD_hashy:1544406358152061038>",
    "verify": "<a:INFAMOUS_Verify:1549136346902175754>",
    "kick": "<a:asskick:1549138352618471434>",
    "banned": "<a:banned:1549138249988182147>",
    "bot": "<a:bot:1549139254712606830>",
    "dance": "<a:brat_dence:1549138072694689943>",
    "confuse": "<a:confuse:1549137286925648012>",
    "diamond": "<a:diomond:1549139140803563644>",
    "error": "<a:error:1549136020094717982>",
    "hammer": "<a:hammer_time:1549138507539288126>",
    "help": "<a:help:1549139550134075513>",
    "link": "<:link:1549139611123449997>",
    "home": "<:home:1549139446950269060>",
    "mute": "<a:mute_mute:1549138714624655450>",
    "heart": "<a:rd_heart_bounce:1549139076580511804>",
    "star": "<a:rd_red_star_imp:1549138951413956631>",
    "sparkles": "<a:sparkles:1549138777660850216>",
    "special": "<a:stolen_emoji_blazeki:1549136671260278896>",
    "support": "<a:support:1544406094451974173>",
    "lock": "<:tc_lock:1549137685954953318>",
    "warn": "<a:warnflash:1549136157898575942>",
    "settings": "<:sm_settings:1549139334425219163>",
}

COMMANDS = [
    "ping","help","server","user","avatar","say","announce","embed",
    "ban","unban","kick","timeout","untimeout","warn","warnings","clear",
    "lock","unlock","slowmode","mute",
]

def load_perms():
    if not os.path.exists(PERM_FILE):
        return {}
    try:
        with open(PERM_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_perms(data):
    with open(PERM_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

perms = load_perms()

def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

def allowed(user_id: int, command: str) -> bool:
    if is_owner(user_id):
        return True
    return command in perms.get(str(user_id), [])

def deny():
    return discord.Embed(
        title=f"{EMOJIS['lock']} LIGHTNESS • ACCESS DENIED",
        description=(
            f"{EMOJIS['error']} **You don't have permission to use this command.**\n\n"
            f"{EMOJIS['crown']} Ask the LIGHTNESS owner for access.\n"
            f"{EMOJIS['link']} discord.gg/FtxqMbBs"
        ),
        color=0xD4AF37,
    )

def check(interaction: discord.Interaction, command: str) -> bool:
    return allowed(interaction.user.id, command)

class Lightness(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(command_prefix=PREFIX, intents=intents)

    async def setup_hook(self):
        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

bot = Lightness()

@bot.event
async def on_ready():
    print(f"LIGHTNESS online as {bot.user} | Guild: {GUILD_ID}")

async def reply(interaction, embed):
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

def simple(title, desc, emoji="sparkles"):
    return discord.Embed(
        title=f"{EMOJIS.get(emoji, '')} {title}",
        description=desc,
        color=0xD4AF37,
    )

@bot.tree.command(name="ping", description="Check LIGHTNESS latency")
async def ping(interaction: discord.Interaction):
    if not check(interaction, "ping"): return await reply(interaction, deny())
    await reply(interaction, simple("LIGHTNESS ONLINE", f"{EMOJIS['verify']} Pong: **{round(bot.latency*1000)}ms**", "bot"))

@bot.tree.command(name="help", description="Show LIGHTNESS commands")
async def help_cmd(interaction: discord.Interaction):
    if not check(interaction, "help"): return await reply(interaction, deny())
    e = simple("LIGHTNESS COMMAND CENTER", f"{EMOJIS['butterfly']} Premium command panel\n{EMOJIS['fire']} Server: discord.gg/FtxqMbBs", "sparkles")
    e.add_field(name="General", value="`/ping` `/server` `/user` `/avatar` `/help`", inline=False)
    e.add_field(name="Management", value="`/ban` `/unban` `/kick` `/timeout` `/untimeout` `/warn` `/warnings` `/clear` `/lock` `/unlock` `/slowmode` `/mute`", inline=False)
    e.add_field(name="Messages", value="`/say` `/announce` `/embed`", inline=False)
    e.add_field(name="Owner", value="`/add` `/remove` `/list` `/check`", inline=False)
    await reply(interaction, e)

@bot.tree.command(name="server", description="Show server information")
async def server(interaction):
    if not check(interaction, "server"): return await reply(interaction, deny())
    g=interaction.guild
    await reply(interaction, simple(f"{g.name}", f"{EMOJIS['home']} Members: **{g.member_count}**\n{EMOJIS['hashy']} ID: `{g.id}`", "home"))

@bot.tree.command(name="user", description="Show a user's information")
@app_commands.describe(member="User to inspect")
async def user(interaction, member: discord.Member=None):
    if not check(interaction, "user"): return await reply(interaction, deny())
    member=member or interaction.user
    await reply(interaction, simple(f"{EMOJIS['bot']} {member.display_name}", f"ID: `{member.id}`\nJoined: <t:{int(member.joined_at.timestamp())}:D>" if member.joined_at else f"ID: `{member.id}`", "bot"))

@bot.tree.command(name="avatar", description="Show a user's avatar")
@app_commands.describe(member="User")
async def avatar(interaction, member: discord.Member=None):
    if not check(interaction, "avatar"): return await reply(interaction, deny())
    member=member or interaction.user
    e=simple(f"{EMOJIS['sparkles']} {member.display_name}'s Avatar", "", "sparkles")
    e.set_image(url=member.display_avatar.url)
    await reply(interaction,e)

@bot.tree.command(name="say", description="Send a message as LIGHTNESS")
@app_commands.describe(message="Message to send")
async def say(interaction, message: str):
    if not check(interaction, "say"): return await reply(interaction, deny())
    await interaction.response.send_message(f"{EMOJIS['arrow']} {message}")

@bot.tree.command(name="announce", description="Send an announcement embed")
@app_commands.describe(title="Announcement title", message="Announcement text")
async def announce(interaction, title: str, message: str):
    if not check(interaction, "announce"): return await reply(interaction, deny())
    e=simple(title, f"{EMOJIS['star']} {message}\n\n{EMOJIS['link']} discord.gg/FtxqMbBs", "star")
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="embed", description="Send a custom embed")
@app_commands.describe(title="Embed title", message="Embed message")
async def embed_cmd(interaction, title: str, message: str):
    if not check(interaction, "embed"): return await reply(interaction, deny())
    await interaction.response.send_message(embed=simple(title,message,"diamond"))

@bot.tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="Member", reason="Reason")
async def ban(interaction, member: discord.Member, reason: str="No reason provided"):
    if not check(interaction,"ban"): return await reply(interaction,deny())
    await member.ban(reason=reason)
    await reply(interaction,simple("USER BANNED",f"{EMOJIS['banned']} {member.mention}\nReason: **{reason}**","banned"))

@bot.tree.command(name="unban", description="Unban by user ID")
@app_commands.describe(user_id="User ID")
async def unban(interaction, user_id: str):
    if not check(interaction,"unban"): return await reply(interaction,deny())
    try: uid=int(user_id)
    except: return await reply(interaction,simple("INVALID ID","Enter a valid Discord user ID.","error"))
    try:
        await interaction.guild.unban(discord.Object(id=uid))
        await reply(interaction,simple("USER UNBANNED",f"{EMOJIS['verify']} `{uid}`","verify"))
    except discord.NotFound:
        await reply(interaction,simple("NOT FOUND",f"{EMOJIS['error']} No matching ban found.","error"))

@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="Member", reason="Reason")
async def kick(interaction, member: discord.Member, reason: str="No reason provided"):
    if not check(interaction,"kick"): return await reply(interaction,deny())
    await member.kick(reason=reason)
    await reply(interaction,simple("USER KICKED",f"{EMOJIS['kick']} {member.mention}\nReason: **{reason}**","kick"))

@bot.tree.command(name="timeout", description="Timeout a member")
@app_commands.describe(member="Member", minutes="Minutes", reason="Reason")
async def timeout(interaction, member: discord.Member, minutes: int, reason: str="No reason provided"):
    if not check(interaction,"timeout"): return await reply(interaction,deny())
    minutes=max(1,min(minutes,40320))
    await member.timeout(discord.utils.utcnow()+__import__("datetime").timedelta(minutes=minutes),reason=reason)
    await reply(interaction,simple("TIMEOUT APPLIED",f"{EMOJIS['mute']} {member.mention} • **{minutes}m**","mute"))

@bot.tree.command(name="untimeout", description="Remove a timeout")
@app_commands.describe(member="Member")
async def untimeout(interaction, member: discord.Member):
    if not check(interaction,"untimeout"): return await reply(interaction,deny())
    await member.timeout(None)
    await reply(interaction,simple("TIMEOUT REMOVED",f"{EMOJIS['verify']} {member.mention}","verify"))

@bot.tree.command(name="warn", description="Warn a member")
@app_commands.describe(member="Member", reason="Reason")
async def warn(interaction, member: discord.Member, reason: str="No reason provided"):
    if not check(interaction,"warn"): return await reply(interaction,deny())
    data=load_perms()
    key=f"warnings:{member.id}"
    data[key]=data.get(key,[])+[reason]
    save_perms(data)
    await reply(interaction,simple("WARNING",f"{EMOJIS['warn']} {member.mention}\nReason: **{reason}**","warn"))

@bot.tree.command(name="warnings", description="View a member's warnings")
@app_commands.describe(member="Member")
async def warnings(interaction, member: discord.Member):
    if not check(interaction,"warnings"): return await reply(interaction,deny())
    data=load_perms(); ws=data.get(f"warnings:{member.id}",[])
    text="\n".join(f"**{i}.** {x}" for i,x in enumerate(ws,1)) or "No warnings."
    await reply(interaction,simple(f"WARNINGS • {member.display_name}",text,"warn"))

@bot.tree.command(name="clear", description="Delete recent messages")
@app_commands.describe(amount="1-100 messages")
async def clear(interaction, amount: int):
    if not check(interaction,"clear"): return await reply(interaction,deny())
    amount=max(1,min(amount,100))
    await interaction.response.defer(ephemeral=True)
    deleted=await interaction.channel.purge(limit=amount)
    await interaction.followup.send(embed=simple("MESSAGES CLEARED",f"{EMOJIS['hammer']} Deleted **{len(deleted)}** messages.","hammer"),ephemeral=True)

@bot.tree.command(name="lock", description="Lock the current channel")
async def lock(interaction):
    if not check(interaction,"lock"): return await reply(interaction,deny())
    ow=interaction.guild.default_role
    await interaction.channel.set_permissions(ow,send_messages=False)
    await interaction.response.send_message(embed=simple("CHANNEL LOCKED",f"{EMOJIS['lock']} {interaction.channel.mention} is locked.","lock"))

@bot.tree.command(name="unlock", description="Unlock the current channel")
async def unlock(interaction):
    if not check(interaction,"unlock"): return await reply(interaction,deny())
    ow=interaction.guild.default_role
    await interaction.channel.set_permissions(ow,send_messages=None)
    await interaction.response.send_message(embed=simple("CHANNEL UNLOCKED",f"{EMOJIS['verify']} {interaction.channel.mention} is unlocked.","verify"))

@bot.tree.command(name="slowmode", description="Set channel slowmode")
@app_commands.describe(seconds="0-21600 seconds")
async def slowmode(interaction, seconds: int):
    if not check(interaction,"slowmode"): return await reply(interaction,deny())
    seconds=max(0,min(seconds,21600))
    await interaction.channel.edit(slowmode_delay=seconds)
    await reply(interaction,simple("SLOWMODE UPDATED",f"{EMOJIS['settings']} **{seconds}s**","settings"))

@bot.tree.command(name="mute", description="Mute a member using timeout")
@app_commands.describe(member="Member", minutes="Minutes")
async def mute(interaction, member: discord.Member, minutes: int=10):
    if not check(interaction,"mute"): return await reply(interaction,deny())
    minutes=max(1,min(minutes,40320))
    await member.timeout(discord.utils.utcnow()+__import__("datetime").timedelta(minutes=minutes))
    await reply(interaction,simple("USER MUTED",f"{EMOJIS['mute']} {member.mention} • **{minutes}m**","mute"))

# Owner-only permission management
def owner_only(interaction):
    return is_owner(interaction.user.id)

@bot.tree.command(name="add", description="OWNER: Give a user command permissions")
@app_commands.describe(user="User", command="Command name, or 'all'")
async def add(interaction, user: discord.Member, command: str):
    if not owner_only(interaction): return await reply(interaction,deny())
    command=command.lower().lstrip("/")
    if command=="all": perms[str(user.id)]=COMMANDS.copy()
    elif command in COMMANDS:
        perms.setdefault(str(user.id),[])
        if command not in perms[str(user.id)]: perms[str(user.id)].append(command)
    else: return await reply(interaction,simple("INVALID COMMAND",f"Use one of: `{', '.join(COMMANDS)}` or `all`","error"))
    save_perms(perms)
    await reply(interaction,simple("ACCESS GRANTED",f"{EMOJIS['crown']} {user.mention}\nPermission: **{command}**","crown"))

@bot.tree.command(name="remove", description="OWNER: Remove a user's command permission")
@app_commands.describe(user="User", command="Command name, or 'all'")
async def remove(interaction, user: discord.Member, command: str):
    if not owner_only(interaction): return await reply(interaction,deny())
    command=command.lower().lstrip("/")
    if str(user.id) not in perms: return await reply(interaction,simple("NO ACCESS","User has no stored permissions.","error"))
    if command=="all": perms.pop(str(user.id),None)
    elif command in perms[str(user.id)]:
        perms[str(user.id)].remove(command)
    else: return await reply(interaction,simple("NOT FOUND","That permission is not assigned.","error"))
    save_perms(perms)
    await reply(interaction,simple("ACCESS REMOVED",f"{EMOJIS['lock']} {user.mention}\nPermission: **{command}**","lock"))

@bot.tree.command(name="list", description="OWNER: List users with permissions")
async def list_users(interaction):
    if not owner_only(interaction): return await reply(interaction,deny())
    lines=[]
    for uid, cs in perms.items():
        if uid.startswith("warnings:"): continue
        member=interaction.guild.get_member(int(uid))
        lines.append(f"{member.mention if member else uid} — `{len(cs)} commands`")
    await reply(interaction,simple("LIGHTNESS ACCESS LIST","\n".join(lines) or "No users have custom access.","crown"))

@bot.tree.command(name="check", description="OWNER: Check a user's permissions")
@app_commands.describe(user="User")
async def check_user(interaction, user: discord.Member):
    if not owner_only(interaction): return await reply(interaction,deny())
    cs=perms.get(str(user.id),[])
    await reply(interaction,simple(f"ACCESS • {user.display_name}",f"{EMOJIS['verify']} {', '.join('/'+x for x in cs) if cs else 'No permissions assigned.'}","settings"))

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is missing. Add it as a Railway environment variable.")

bot.run(TOKEN)
