# LIGHTNESS — Railway Setup

## 1. Upload to GitHub
Upload all files from this folder to a new GitHub repository.

## 2. Create Railway service
Create a new Railway project and deploy the GitHub repository.

## 3. Add variable
Railway → Service → Variables:

DISCORD_TOKEN = YOUR_DISCORD_BOT_TOKEN

Do NOT put the token inside GitHub.

## 4. Start command
Railway can use the included Procfile. If needed, set:
python bot.py

## 5. Discord bot permissions
Invite the bot to your server with the permissions required by the moderation commands:
View Channels, Send Messages, Embed Links, Read Message History, Manage Messages, Moderate Members, Kick Members, Ban Members, Manage Channels.

Use the minimum permissions you actually need.

## 6. Owner access
Owner ID is hard-coded as:
1433457392917676138

Guild ID:
1544039840767803412

## Permission commands
/add user command: give one command
/add user all: give all normal commands
/remove user command: remove one command
/remove user all: remove all commands
/list: list permitted users
/check user: show a user's permissions

Only the owner ID can use these four permission-management commands.

The bot stores permissions in permissions.json. For a production setup, commit/persist this file or use Railway's persistent volume if you want permissions to survive redeploys. Keep the bot token private.
