# LIGHTNESS OP Security Edition

Railway-ready Discord bot.

## Setup
- Upload these files to GitHub.
- Railway → Variables → `DISCORD_TOKEN`.
- Do NOT put the real token in GitHub.
- Owner ID: `1433457392917676138`
- Guild ID: `1544039840767803412`

## Security
Includes a permission-gated security layer with:
- Anti-nuke monitoring for repeated channel/role create/delete actions
- Emergency `/lockdown` and `/unlockdown`
- `/security_setup` status
- Owner whitelist
- Defensive timeout/kick response when thresholds are crossed

Important: no Discord bot can guarantee that nobody can ever bypass security. Give LIGHTNESS the minimum required permissions, keep its role above roles it must manage, protect the owner account, and enable Discord's native security features/2FA where appropriate.

## Emoji system
Your supplied emoji IDs are centralized in `bot.py` and resolved by ID, so message code does not need emoji tags repeated everywhere.
