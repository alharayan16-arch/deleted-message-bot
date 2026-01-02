import discord
from discord.ext import commands
from datetime import datetime

import os
LOG_CHANNEL_ID = 1456557125592547370

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


# 🗑️ DELETED MESSAGE
@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    embed = discord.Embed(
        title="🗑️ MESSAGE DELETED",
        description="A message was deleted in the server",
        color=discord.Color.from_rgb(255, 80, 80),
        timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=message.author.avatar.url if message.author.avatar else None
    )

    embed.add_field(
        name="👤 User",
        value=f"{message.author}\n`{message.author.id}`",
        inline=True
    )

    embed.add_field(
        name="📍 Channel",
        value=message.channel.mention,
        inline=True
    )

    embed.add_field(
        name="💬 Message Content",
        value=message.content if message.content else "*No text (image / embed)*",
        inline=False
    )

    if message.attachments:
        embed.add_field(
            name="🖼️ Attachments",
            value="\n".join(f"[Image]({a.url})" for a in message.attachments),
            inline=False
        )

    embed.set_footer(text="Deleted Message Logger")

    await log_channel.send(embed=embed)


# ✏️ EDITED MESSAGE
@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content == after.content:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)
    if not log_channel:
        return

    embed = discord.Embed(
        title="✏️ MESSAGE EDITED",
        description="A message was edited in the server",
        color=discord.Color.from_rgb(255, 170, 0),
        timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=before.author.avatar.url if before.author.avatar else None
    )

    embed.add_field(
        name="👤 User",
        value=f"{before.author}\n`{before.author.id}`",
        inline=True
    )

    embed.add_field(
        name="📍 Channel",
        value=before.channel.mention,
        inline=True
    )

    embed.add_field(
        name="🟥 Before",
        value=before.content or "*No text*",
        inline=False
    )

    embed.add_field(
        name="🟩 After",
        value=after.content or "*No text*",
        inline=False
    )

    embed.set_footer(text="Edited Message Logger")

    await log_channel.send(embed=embed)


import os
bot.run(os.environ["DISCORD_TOKEN"])



