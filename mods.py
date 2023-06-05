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
import times

init()

import database
import config
import adms

db = sqlite3.connect('data.db')
cur = db.cursor()

async def tempqua(ctx, user: disnake.Member, time1: int):
    quarole = cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    if quarole != None:
        if not ctx.guild.get_role(quarole[0]):
            quarole = await ctx.guild.create_role(name='Chaos-Qua')
            cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, quarole.id))
            db.commit()
        else:
            quarole = ctx.guild.get_role(quarole[0])
    else:
        quarole = await ctx.guild.create_role(name='Chaos-Qua')
        cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, quarole.id))
        db.commit()
    for role in user.roles:
        try:
            await user.remove_roles(role)
        except: pass
    await user.add_roles(quarole)
    cur.execute("INSERT INTO timequas VALUES (?, ?, ?)", (ctx.guild.id, user.id, int(time.time()) + time1))
    db.commit()

async def qua(ctx, user: disnake.Member):
    quarole = cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    if quarole != None:
        if not ctx.guild.get_role(quarole[0]):
            quarole = await ctx.guild.create_role(name='Chaos-Qua')
            cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, quarole.id))
            db.commit()
        else:
            quarole = ctx.guild.get_role(quarole[0])
    else:
        quarole = await ctx.guild.create_role(name='Chaos-Qua')
        cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, quarole.id))
        db.commit()
    for role in user.roles:
        try:
            await user.remove_roles(role)
        except: pass
    await user.add_roles(quarole)
    cur.execute("INSERT INTO quas VALUES (?, ?)", (ctx.guild.id, user.id))
    db.commit()

async def tempmute(ctx, user: disnake.Member, time1: int):
    muterole = cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    if muterole != None:
        if not ctx.guild.get_role(muterole[0]):
            muterole = await ctx.guild.create_role(name='Chaos-Muted')
            cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, muterole.id))
            db.commit()
        else:
            muterole = ctx.guild.get_role(muterole[0])
    else:
        muterole = await ctx.guild.create_role(name='Chaos-Muted')
        cur.execute("INSERT INTO muteroles VALUES (?, ?)", (ctx.guild.id, muterole.id))
        db.commit()
        for c in ctx.guild.text_channels:
            try:
                await c.set_permissions(muterole, send_messages=False, add_reactions=False)
            except: pass
    await user.add_roles(muterole)
    cur.execute("INSERT INTO timemutes VALUES (?, ?, ?)", (ctx.guild.id, user.id, int(time.time()) + time1))
    db.commit()

async def mute(ctx, user: disnake.Member):
    muterole = cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    if muterole != None:
        if not ctx.guild.get_role(muterole[0]):
            muterole = await ctx.guild.create_role(name='Chaos-Muted')
            cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, muterole.id))
            db.commit()
        else:
            muterole = ctx.guild.get_role(muterole[0])
    else:
        muterole = await ctx.guild.create_role(name='Chaos-Muted')
        cur.execute("INSERT INTO muteroles VALUES (?, ?)", (ctx.guild.id, muterole.id))
        db.commit()
        for c in ctx.guild.text_channels:
            try:
                await c.set_permissions(muterole, send_messages=False, add_reactions=False)
            except: pass
    await user.add_roles(muterole)
    cur.execute("INSERT INTO mutes VALUES (?, ?)", (ctx.guild.id, user.id))
    db.commit()

async def tempban(ctx, user: disnake.Member, time1: int):
    try:
        await user.ban()
    except:
        pass #await ctx.send(embed=disnake.Embed(title='<:1828774:1025858045873487922> | Ошибка..', description='>>> **Не удалось забанить участника.**', color=config.error_color))
    cur.execute("INSERT INTO timebans VALUES (?, ?, ?)", (ctx.guild.id, user.id, int(time.time()) + time1))
    db.commit()