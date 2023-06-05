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
import mods
import adms

class Quarantine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()
    
    
    @commands.slash_command(description='Карантин')
    async def quarantine(self, ctx: disnake.AppCommandInteraction):
        pass
    
    @quarantine.sub_command(description="Добавить пользователя в карантин")
    @commands.check(adms.has_head_admin)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def add(self, ctx: disnake.AppCmdInter, member: disnake.Member=None, reason='Причина не указана.', time1='0s'):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не упомянул пользователя которого хочешь отправить в карантин**', color=config.error_color))
        if not isinstance(member, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты упомянул не пользователя**', color=config.error_color))
        if member == ctx.author:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя отправить в карантин самого себя**', color=config.error_color))
        if member.id == self.bot.user.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя отправить бота в карантин**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не можешь занести владельца сервера в карантин.**', color=config.error_color))            
        if member.id == self.bot.user.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не можешь занести бота в карантин.**', color=config.error_color))
        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне со мной.**', color=config.error_color))
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не можешь закрыть на карантин пользователя, роль которого не ниже твоей.**', color=config.error_color))
        if self.cur.execute("SELECT * FROM quas WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() != None or self.cur.execute("SELECT * FROM timequas WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() != None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Пользователь уже в карантине**', color=config.error_color))
        await ctx.response.defer()
        embed = disnake.Embed(
            title=':biohazard: | Карантин',
            description=f'''>>> **Пользователь занесён в карантин
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Пользователь: `{member}` ({member.mention})**''',
            color=config.warning_color
        )
        if time1 == '0s':
            await ctx.edit_original_response(embed=embed)
            await mods.qua(ctx, member)
            embed.description = f'''>>> **Ты был занесён в карантин на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`**'''
            try: await member.send(embed=embed)
            except: pass
        else:
            if times.ishs(time1):
                time1 = times.string_to_seconds(time1)
                embed.description=f'''>>> **Пользователь занесён в карантин
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Пользователь: `{member}` ({member.mention})
Срок: `{times.hms(float(time1))}`**'''
                await ctx.edit_original_response(embed=embed)
                await mods.tempqua(ctx, member, time1)
                embed.description=f'''>>> **Ты был занесён в карантин на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Срок: `{times.hms(float(time1))}`**'''
                try: await member.send(embed=embed)
                except: pass
            else:
                await ctx.edit_original_response(embed=embed)
                await mods.qua(ctx, member)
                embed.description = f'''>>> **Ты был занесён в карантин на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`**'''
                try: await member.send(embed=embed)
                except: pass

    @quarantine.sub_command(description='Убрать пользователя из карантина')
    @commands.check(adms.has_head_admin)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def remove(self, ctx: disnake.AppCmdInter, member: disnake.Member=None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не упомянул пользователя которого хочешь убрать из карантина**', color=config.error_color))
        if not isinstance(member, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты упомянул не пользователя**', color=config.error_color))
        if member == ctx.author:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя убрать из карантина самого себя**', color=config.error_color))
        if self.cur.execute("SELECT * FROM quas WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None and self.cur.execute("SELECT * FROM timequas WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Пользователь не находится в карантине**', color=config.error_color))
        await ctx.send(
            embed=disnake.Embed(
                title=':biohazard: | Карантин',
                description=f'>>> **Пользователь `{member}` ({member.mention}) удалён из карантина**',
                color=config.warning_color
            )
        )
        self.cur.execute("DELETE FROM quas WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))
        self.db.commit()
        self.cur.execute("DELETE FROM timequas WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))
        self.db.commit()
        quarole = self.cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if quarole != None:
            quarole = ctx.guild.get_role(quarole[0])
        try:
            await member.remove_roles(quarole)
        except: pass

    @quarantine.sub_command(description='Выбрать роль карантина')
    @commands.check(adms.has_head_admin)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def role(self, ctx: disnake.AppCmdInter, role: disnake.Role=None):
        if role == None:
            quarole = self.cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
            if quarole != None:
                if not ctx.guild.get_role(quarole[0]):
                    quarole = '`Роль выбрана, но её нет на сервере`'
                else:
                    quarole = ctx.guild.get_role(quarole[0]).mention
            else:
                quarole = '`Роль ещё не выбрана`'
            #a gidespc код сольёт наверно #я имею ввиду в список животных АХАХАХАХ
            embed = disnake.Embed(
                title=":biohazard: | Карантин",
                description=f">>> **Карантинная роль на данном сервере: {quarole}**",
                color=config.warning_color
            )
            return await ctx.send(embed=embed)
        if not isinstance(role, disnake.Role):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты указал не роль**', color=config.error_color))
        if role.managed:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль принадлежит боту, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже моей, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.author.top_role.position:# ты меня кикал? #нет а значит у меня инет хуёвый
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже твоей**', color=config.error_color))
        embed = disnake.Embed( # crash by forzel and snejok 332 БЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯТЬ ЖДИ ДИАНОН😡👿 НЕ НАДО ЛАДНА ЛАДНАААААА 
            title=":biohazard: | Карантин",
            description=f">>> **Роль {role.mention} помечена как карантинная роль**",
            color=config.warning_color
        )
        await ctx.send(embed=embed)
        await role.edit(permissions=disnake.Permissions._from_value(0))
        #for channel in ctx.guild.text_channels:
        #    await channel.set_permissions(role, view_channel=False)
        #for channel in ctx.guild.voice_channels:
        #    await channel.set_permissions(role, connect=False)
        self.cur.execute("DELETE FROM quaroles WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        self.cur.execute("INSERT INTO quaroles VALUES (?, ?)", (ctx.guild.id, role.id))
        self.db.commit()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.roles != before.roles:
            if self.cur.execute("SELECT * FROM quas WHERE guild_id = {} AND user_id = {}".format(after.guild.id, after.id)).fetchone() != None or self.cur.execute("SELECT * FROM timequas WHERE guild_id = {} AND user_id = {}".format(after.guild.id, after.id)).fetchone() != None:
                quarole = self.cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(after.guild.id)).fetchone()
                for role in after.roles:
                    if quarole != None:
                        rl = after.guild.get_role(quarole[0])
                        if not role in before.roles and not role == rl:
                            try:
                                await after.remove_roles(role)
                            except: pass
                    else:
                        if not role in before.roles:
                            try:
                                await after.remove_roles(role)
                            except: pass
                quarole = self.cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(after.guild.id)).fetchone()
                if quarole != None:
                    rl = after.guild.get_role(quarole[0])
                    if rl: 
                        if not rl in after.roles:
                            try:
                                await after.add_roles(rl)
                            except:
                                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.cur.execute("SELECT * FROM quas WHERE guild_id = {} AND user_id = {}".format(member.guild.id, member.id)).fetchone() != None or self.cur.execute("SELECT * FROM timequas WHERE guild_id = {} AND user_id = {}".format(member.guild.id, member.id)).fetchone() != None:
            quarole = self.cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(member.guild.id)).fetchone()
            if quarole != None:
                quarole = member.get_role(quarole[0])
                try:
                    await member.add_roles(quarole)
                except: pass


def setup(bot):
    bot.add_cog(Quarantine(bot))