import sqlite3
from disnake.ui import ActionRow, Select, Button, View
from disnake import SelectOption, ButtonStyle
import disnake
from disnake.ext import commands
import io
import contextlib
import textwrap
import os
import aiohttp
from matplotlib.style import use
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
import adms
import mods
import times


class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()
        
    @commands.slash_command(description='Забанить пользователя на сервере')
    @commands.check(adms.has_ban_members)
    @commands.cooldown(1, 45, commands.BucketType.guild)
    async def ban(self, ctx, user: disnake.Member=None, *, reason='Не указана', time1='0s'):
        await ctx.response.defer()
        if user == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которого хотите забанить**', color=config.error_color))
        if not isinstance(user, disnake.Member):
            #print(type(user))
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if user.id == ctx.author.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя забанить самого себя**', color=config.error_color))
        if ctx.guild.get_member(user.id):
            if ctx.guild.get_member(user.id) == ctx.guild.me:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя забанить бота**', color=config.error_color))
            if ctx.guild.get_member(user.id) == ctx.guild.owner:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя забанить владельца сервера**', color=config.error_color))
            if ctx.guild.get_member(user.id).top_role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с моей ролью**', color=config.error_color))
            if ctx.guild.get_member(user.id).top_role.position >= ctx.author.top_role.position and not ctx.author == ctx.guild.owner:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с вашей ролью**', color=config.error_color))
        if time1 == '0s':
            try:
                await user.send(
                    embed=disnake.Embed(
                        title=':hammer: | Бан',
                        description=f'''>>> **Вы были забанены на сервере `{ctx.guild.name}` ({ctx.guild.id})
Модератор: `{ctx.author}` ({ctx.author.mention})
Причина: `{reason}`**''',
                        color=config.main_color
                    )
                )
            except:
                pass
            await user.ban(reason=reason)
            await ctx.send(
                embed=disnake.Embed(
                    title=':hammer: | Бан',
                    description=f'''>>> **Пользователь `{user}` был забанен
Модератор: `{ctx.author}` ({user.mention})
Причина: `{reason}`**''',
                    color=config.main_color
                )
            )
        else:
            if times.ishs(time1):
                time1 = times.string_to_seconds(time1)
                try: await user.send(
                    embed=disnake.Embed(
                        title=':hammer: | Бан',
                        description=f'''>>> **Вы были забанены на сервере `{ctx.guild.name}` ({ctx.guild.id})
Модератор: `{ctx.author}` ({ctx.author.mention})
Причина: `{reason}`
Срок: `{times.hms(float(time1))}`**''',
                        color=config.main_color
                    )
                )
                except: pass
                await mods.tempban(ctx, user, time1)
                await ctx.send(
                    embed=disnake.Embed(
                        title=':hammer: | Бан',
                        description=f'''>>> **Пользователь `{user}` был забанен
Модератор: `{ctx.author}` ({user.mention})
Причина: `{reason}`**''',
                        color=config.main_color
                    )
                )
            else:
                try:
                    await user.send(
                        embed=disnake.Embed(
                            title=':hammer: | Бан',
                            description=f'''>>> **Вы были забанены на сервере `{ctx.guild.name}` ({ctx.guild.id})
    Модератор: `{ctx.author}` ({ctx.author.mention})
    Причина: `{reason}`**''',
                            color=config.main_color
                        )
                    )
                except:
                    pass
                await user.ban(reason=reason)
                await ctx.send(
                    embed=disnake.Embed(
                        title=':hammer: | Бан',
                        description=f'''>>> **Пользователь `{user}` был забанен
Модератор: `{ctx.author}` ({user.mention})
Причина: `{reason}`**''',
                        color=config.main_color
                    )
                )

    @commands.slash_command(description='Кикнуть участника с сервера')
    @commands.check(adms.has_kick_members)
    @commands.cooldown(1, 45, commands.BucketType.guild)
    async def kick(self, ctx, user: disnake.Member=None, *, reason='Не указана'):
        await ctx.response.defer()
        if user == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которого хотите кикнуть**', color=config.error_color))
        if not isinstance(user, disnake.Member):
            #print(type(user))
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if user.id == ctx.author.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя кикнуть самого себя**', color=config.error_color))
        if ctx.guild.get_member(user.id):
            if ctx.guild.get_member(user.id) == ctx.guild.me:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя кикнуть бота**', color=config.error_color))
            if ctx.guild.get_member(user.id) == ctx.guild.owner:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя кикнуть владельца сервера**', color=config.error_color))
            if ctx.guild.get_member(user.id).top_role.position >= ctx.guild.me.top_role.position:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с моей ролью**', color=config.error_color))
            if ctx.author == ctx.guild.owner:
                try:
                    await user.send(
                        embed=disnake.Embed(
                            title=':hammer: | Кик',
                            description=f'''>>> **Вы были кикнуты с сервера `{ctx.guild.name}` ({ctx.guild.id})
Модератор: `{ctx.author}`
Причина: `{reason}`**''',
                            color=config.main_color
                        )
                    )
                except:
                    pass
                await user.kick(reason=f'{ctx.author}: {reason}')
                await ctx.send(
                    embed=disnake.Embed(
                        title=':hammer: | Кик',
                        description=f'''>>> **Пользователь {user} был кикнут
Модератор: {ctx.author}
Причина: `{reason}`**''',
                        color=config.main_color
                    )
                )
                return
            if ctx.guild.get_member(user.id).top_role.position >= ctx.author.top_role.position:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с вашей ролью**', color=config.error_color))
        try:
            await user.send(
                embed=disnake.Embed(
                    title=':hammer: | Кик',
                    description=f'''>>> **Вы получили кик на сервере `{ctx.guild.name}` ({ctx.guild.id})
Модератор: `{ctx.author}`
Причина: `{reason}`**''',
                    color=config.main_color
                )
            )
        except:
            pass
        await user.kick(reason=reason)
        await ctx.send(
            embed=disnake.Embed(
                title=':hammer: | Кик',
                description=f'''>>> **Пользователь {user} был кикнут
Модератор: {ctx.author}
Причина: `{reason}`**''',
                color=config.main_color
            )
        )

    @commands.slash_command(description='Очистить сообщений в чате')
    @commands.check(adms.has_manage_messages)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def clear(self, ctx, amount: int = 100, user: typing.Optional[disnake.Member] = None):
        await ctx.response.defer()
        m = await ctx.original_message()
        def check(msg):
            return msg.author == user and not msg.id == m.id
        if amount > 1000:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя удалить более `1000` сообщений**', color=config.error_color))
        else:
            embed = disnake.Embed(color=config.main_color)
            embed.title = ":broom: | Очистка сообщений"
            if user is None:
                deleted = len(await ctx.channel.purge(limit=amount, check=lambda msg: msg.id != m.id))
                embed.description = f'>>> **Удалено `{deleted}` сообщений**'
            else:
                deleted = len(await ctx.channel.purge(limit=amount, check=check))
                embed.description = f'>>> **Удалено `{deleted}` сообщений от {user.mention}**'
            await ctx.send(embed=embed)
    
    @commands.slash_command(description='Закрыть канал для сообщений')
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def lock(self, ctx, channel: disnake.TextChannel = None):
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
        await ctx.message.add_reaction('🔒')
        #await ctx.send('🔒')

    @commands.slash_command(description='Открыть канал для сообщений')
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def unlock(self, ctx, channel: disnake.TextChannel = None):
        await ctx.response.defer()
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions=None, speak=None, connect=None)
        #await ctx.send('🔓')
        await ctx.message.add_reaction('🔓')
        """
    @commands.command(description='Закрыть чат.')
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def lock(self, ctx, channel: disnake.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
        await ctx.message.add_reaction('🔒')
    @commands.command(description='Открыть чат.')
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def unlock(self, ctx, channel: disnake.TextChannel = None):
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=None, add_reactions=None)
        await ctx.message.add_reaction('🔓')
    """

    @commands.slash_command(description='Выдать предупреждение пользователю')
    @commands.check(adms.has_moderator)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def warn(self, ctx, user: disnake.Member=None, reason="Причина не указана"):
        await ctx.response.defer()
        if user == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которому хотите выдать предупреждение**', color=config.error_color))
        if not isinstance(user, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if user.id == ctx.author.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя выдать предупреждение себе**', color=config.error_color))
        if user.top_role.position >= ctx.author.top_role.position and not ctx.author == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с вашей ролью**', color=config.error_color))            
        if user == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя выдать предупреждение владельцу сервера.**', color=config.error_color))
        if user.id == self.bot.user.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не можете выдать предупреждение боту.**', color=config.error_color))
        warnnum = len(self.cur.execute("SELECT * FROM warns WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, user.id)).fetchall()) + 1
        if warnnum > 30:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Лимит предупреждений для этого участника (30) превышен**', color=config.error_color))
        embed = disnake.Embed(
            title=':warning: | Предупреждение',
            description=f'>>> **Участнику выдано предупреждение\nУчастник: `{user}` ({user.mention})\nМодератор: `{ctx.author}` ({ctx.author.mention})\n№ предупреждения: `#{warnnum}`\nПричина: `{reason}`**',
            color=config.warning_color
        )
        await ctx.send(embed=embed)
        self.cur.execute("INSERT INTO warns VALUES (?, ?, ?, ?)", (ctx.guild.id, user.id, reason, warnnum))
        self.db.commit()
        embed = disnake.Embed(
            title=':warning: | Предупреждение',
            description=f'>>> **Вы получили предупреждение на сервере `{ctx.guild.name}` ({ctx.guild.id})\nМодератор: `{ctx.author}` ({ctx.author.mention})\n№ предупреждения: `#{warnnum}`\nПричина: `{reason}`**',
            color=config.warning_color
        )
        await user.send(embed=embed)

    @commands.slash_command(description='Снять предупреждение с пользователя')
    @commands.check(adms.has_moderator)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def unwarn(self, ctx, user: disnake.Member=None, number: int=None):
        await ctx.response.defer()
        if user == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, у которого хотите снять предупреждение**', color=config.error_color))
        if number == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не указали № предупреждения, которое хотите снять участнику**', color=config.error_color))
        if not isinstance(user, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if not isinstance(number, int):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **№ предупреждения должен быть числом**', color=config.error_color)) 
        if user.id == ctx.author.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя снять предупреждение у себя**', color=config.error_color))
        if user == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя снять предупреждение владельцу сервера.**', color=config.error_color))
        if self.cur.execute("SELECT * FROM warns WHERE guild_id = {} AND user_id = {} AND warn_number = {}".format(ctx.guild.id, user.id, number)).fetchone() == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Такое предупреждение не найдено**', color=config.error_color))
        self.cur.execute("DELETE FROM warns WHERE guild_id = {} AND user_id = {} AND warn_number = {}".format(ctx.guild.id, user.id, number))
        self.db.commit()
        embed=disnake.Embed(
            title=":warning: | Снято предупреждение",
            description=f">>> **Участник: `{user}` ({user.mention})\nМодератор: `{ctx.author}` ({ctx.author.mention})\nНомер предупреждения: `#{number}`**",
            color=config.warning_color
        )
        await ctx.send(embed=embed)

    @commands.slash_command(description='Просмотреть предупреждения пользователя')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def warnlist(self, ctx, user: disnake.User=None):
        if user == None:
            user = ctx.author
        if not isinstance(user, disnake.Member) and not isinstance(user, disnake.User):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        warns = self.cur.execute("SELECT warn_number, reason FROM warns WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, user.id)).fetchall()
        if warns == []:
            embed=disnake.Embed(
                title=":warning: | Список предупреждений",
                description=f">>> **Список предупреждений участника `{user}` ({user.mention})\nПредупреждения отсутствуют**",
                color=config.warning_color
            )
            return await ctx.send(embed=embed)
        wrns = ""
        for war in warns:
            wrns += f"Предупреждение #{war[0]}\nПричина: `{war[1]}`\n"
        embed=disnake.Embed(
            title=":warning: | Список предупреждений",
            description=f">>> **Список предупреждений участника `{user}` ({user.mention})\n{wrns}**",
            color=config.warning_color
        )
        await ctx.send(embed=embed)

    @commands.slash_command(description='Выдать мут пользователю')
    @commands.check(adms.has_mute_members)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def mute(self, ctx, member: disnake.Member=None, reason='Причина не указана.', time1='0s'):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которого хотите замутить**', color=config.error_color))
        if not isinstance(member, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if member == ctx.author:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя замутить самого себя**', color=config.error_color))
        if member.id == self.bot.user.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя замутить бота**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не можете замутить владельца сервера.**', color=config.error_color))
        if member.id == self.bot.user.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не можете замутить бота.**', color=config.error_color))
        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с моей ролью.**', color=config.error_color))
        if member.top_role >= ctx.author.top_role and not ctx.author == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль данного пользователя выше/на уровне с вашей ролью.**', color=config.error_color))
        if self.cur.execute("SELECT * FROM mutes WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() != None or self.cur.execute("SELECT * FROM timemutes WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() != None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Пользователю уже был выдан мут**', color=config.error_color))
        await ctx.response.defer()
        embed = disnake.Embed(
            title=':stop_button: | Мут',
            description=f'''>>> **Пользователю выдан мут
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Пользователь: `{member}` ({member.mention})**''',
            color=config.error_color
        )
        if time1 == '0s':
            await ctx.edit_original_response(embed=embed)
            await mods.qua(ctx, member)
            embed.description = f'''>>> **Вам был выдан мут на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`**'''
            try:
                await member.send(embed=embed)
            except:
                pass
        else:
            if times.ishs(time1):
                time1 = times.string_to_seconds(time1)
                embed.description=f'''>>> **Пользователю выдан мут
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Пользователь: `{member}` ({member.mention})
Срок: `{times.hms(float(time1))}`**'''
                await ctx.edit_original_response(embed=embed)
                await mods.tempmute(ctx, member, time1)
                embed.description=f'''>>> **Вам был выдан мут на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`
Срок: `{times.hms(float(time1))}`**'''
                try:
                    await member.send(embed=embed)
                except:
                    pass
            else:
                await ctx.edit_original_response(embed=embed)
                await mods.mute(ctx, member)
                embed.description = f'''>>> **Вам был выдан мут на сервере `{ctx.guild.name}`
Администратор: `{ctx.author}` ({ctx.author.mention}
Причина: `{reason}`**'''
                try:
                    await member.send(embed=embed)
                except:
                    pass

    @commands.slash_command(description='Снять мут с пользователя')
    @commands.check(adms.has_mute_members)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def unmute(self, ctx, member: disnake.Member=None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которого хотите убрать из карантина**', color=config.error_color))
        if not isinstance(member, disnake.Member):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if member == ctx.author:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя размутить самого себя**', color=config.error_color))
        if self.cur.execute("SELECT * FROM mutes WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None and self.cur.execute("SELECT * FROM timemutes WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Пользователь не замучен**', color=config.error_color))
        await ctx.send(
            embed=disnake.Embed(
                title=':stop_button: | Мут',
                description=f'>>> **С пользователя `{member}` ({member.mention}) был снят мут**',
                color=config.error_color
            )
        )
        self.cur.execute("DELETE FROM mutes WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))
        self.db.commit()
        self.cur.execute("DELETE FROM timemutes WHERE user_id = {} AND guild_id = {}".format(member.id, ctx.guild.id))
        self.db.commit()
        quarole = self.cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if quarole != None:
            quarole = ctx.guild.get_role(quarole[0])
        try:
            await member.remove_roles(quarole)
        except:
            pass
        
    @commands.slash_command(description='Снять бан с пользователя')
    @commands.check(adms.has_ban_members)
    @commands.cooldown(1, 45, commands.BucketType.guild)
    async def unban(self, ctx, user: disnake.User=None, reason='Не указана'):
        # await ctx.response.defer()
        if user == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули пользователя, которого хотите разбанить**', color=config.error_color))
        if not isinstance(user, disnake.User):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не пользователя**', color=config.error_color))
        if user.id == ctx.author.id:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нельзя разбанить самого себя**', color=config.error_color))
        if ctx.guild.get_member(user.id):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Пользователь есть на сервере**', color=config.error_color))
        await ctx.guild.unban(user, reason=reason)
        await ctx.send(
            embed=disnake.Embed(
                title=':white_check_mark: | Успешно',
                description=f'>>> **Пользователь {user} был разбанен**',
                color=config.success_color
            )
        )
        self.cur.execute("DELETE FROM timebans WHERE user_id = {} AND guild_id = {}".format(user.id, ctx.guild.id))
        self.db.commit()

    @commands.slash_command()
    async def warnlistuser(self, ctx, user: typing.Union[disnake.User, disnake.Member]):
        await self.warnlist(ctx, user)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.cur.execute("SELECT * FROM mutes WHERE guild_id = {} AND user_id = {}".format(member.guild.id, member.id)).fetchone() != None or self.cur.execute("SELECT * FROM mutes WHERE guild_id = {} AND user_id = {}".format(member.guild.id, member.id)).fetchone() != None:
            quarole = self.cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(member.guild.id)).fetchone()
            if quarole != None:
                quarole = member.get_role(quarole[0])
                try:
                    await member.add_roles(quarole)
                except:
                    pass

    
def setup(bot):
    bot.add_cog(Mod(bot))