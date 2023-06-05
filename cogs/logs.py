import sqlite3
import disnake
from disnake.ext import commands
import io
import contextlib
import textwrap
import os
import aiohttp
import requests
import random
import asyncio
import time
import datetime
from datetime import datetime as dt
import typing
from colorama import Fore, init

init()

import database
import config


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()
        
        
    @commands.slash_command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.check(messages.check_perms)
    async def logs(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = disnake.Embed(color=config.main_color)
            embed.title = "📝 | Канал логов"
            embed.add_field(name="Команды", inline=False, value=f"""
`{ctx.prefix}log set` – Установить канал для логов
`{ctx.prefix}log remove` – Удалить канал для логов
            """)
            try:
                channel = self.cur.execute("SELECT channel_id FROM logs WHERE guild_id = {}".format(ctx.guild.id))
            except AttributeError:
                channel = None
            except KeyError:
                channel = None

            if channel:
                embed = disnake.Embed(
                    title="Канал логов",
                    description=f"Текущий канал логов: {channel_id.mention}",
                    color=config.main_color()
                )
                await ctx.send(embed=embed)

    @logs.sub_command(name='set')
    async def __set(self, ctx, channel1: disnake.TextChannel):
        try:
            channel = self.cur.execute("SELECT channel_id FROM logs WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
        except KeyError:
            channel = None

        if channel:
            if channel1.id == channel:
                return await messages.err(ctx, "Новый канал для логов не может совпадать со старым.")

        webhook = await channel1.create_webhook(name="Vulture Logs")
        await webhook.send("📁 | Этот канал указан в качестве канала для логов. Пожалуйста, не удаляйте этот вебхук. Спасибо!")
        self.cur.execute("INSERT INTO webhook VALUES (?, ?, ?)", (ctx.guild.id, channel1.id, webhook.id))
        self.db.commit()
        embed = disnake.Embed(
            title="✅ | Готово", 
            description=f"Канал {channel1.mention} указан как канал для логов.", 
            color=config.main_color()
        )
        await ctx.send(embed=embed)

    @logs.sub_command(name='remove')
    async def __remove(self, ctx):
        try:
            channel = self.cur.execute("SELECT channel_id FROM logs WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        except KeyError:
            channel = None

        if not channel:
            return await messages.err(ctx, "Канал логов не был указан ранее")
        else:
            self.cur.execute("DELETE channel_id FROM logs WHERE guild_id = {}".format(ctx.guild.id))
            embed = disnake.Embed(
                title="✅ | Готово", 
                description=f"Канал логов {channel.mention} был удалён.", 
                color=config.main_color()
                )
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Logs(bot))