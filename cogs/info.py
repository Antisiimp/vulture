import sqlite3
import disnake
from disnake.ext import commands
import io
import contextlib
import textwrap
import os
import aiohttp
import pyshorteners
import requests
import random
import asyncio
import time
import datetime
from datetime import datetime as dt
import typing
from colorama import Fore, init
from memory_profiler import memory_usage

init()

import database
import config

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

    async def checkac(self, guild):
        #if self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {}".format(guild.id)).fetchone() != None:
        #    return True
        #return False
        return len(self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {}".format(guild.id)).fetchall())

    async def checkab(self, guild):
        if self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(guild.id)).fetchone() != None:
            return True
        return False

    @commands.slash_command(description="Инфо о эмодзи.")
    async def emojiinfo(self, ctx, emoji:disnake.Emoji):
        embed = disnake.Embed(title=":information_source: | Эмодзи", color=config.main_color)
        embed.add_field(name="Название", value=emoji.name)
        embed.add_field(name="ID", value=emoji.id)
        if emoji.animated == False:anim = "Нет :x:"
        else:anim="Да :white_check_mark:"
        embed.add_field(name="Анимированное ?", value=anim)
        embed.add_field(name="Создано", value=f"<t:{round(emoji.created_at.timestamp())}:f>")
        try:embed.add_field(name="Автор", value=emoji.user if emoji.user else ":question: Не определён")
        except:embed.add_field(name="Автор", value=":question: Не определён")
        embed.add_field(name="URL", value=f"[Скачать]({emoji.url})")
        await ctx.send(embed=embed)
    
    @commands.slash_command(description='Информация о сервере')
    async def serverinfo(self, ctx):
        link = await ctx.guild.channels[0].create_invite()
        rgs = {
            'brazil':':flag_br: Бразилия',
            'europe':':flag_eu: Европа',
            'hongkong':':flag_hk: Гонконг',
            'india':':flag_in: Индия',
            'japan':':flag_jp: Япония',
            'russia':':flag_ru: Россия',
            'singapore':':flag_sg: Сингапур',
            'southafrica':':flag_za: ЮАР',
            'sydney':':flag_au: Сидней',
            'us-central':':flag_us: Центральная Америка',
            'us-east':':flag_us: Восточное побережье США',
            'us-south':':flag_us: Америка (Юг)',
            'us-west':':flag_us: Западное побережье США',
            'deprecated':'Убран'
        }
        vlevels = {
            'none':'Отсутствует',
            'low':'Низкий',
            'medium':'Средний',
            'high':'Высокий',
            'extreme':'Самый высокий',
            'highest': 'Наивысший'
        }
        embed = disnake.Embed(
            title=':information_source: | Инфо о сервере',
            color=config.main_color
        )
        embed.add_field(
            name='Основная информация',
            value=f""">>> **├ :information_source: × Название сервера: `{ctx.guild.name}`
├ :link: × Ссылка приглашения: [клик](https://discord.gg/{link.code})
├ :link: × Создано приглашений: `{len(await ctx.guild.invites())}`
├ :id: × ID Сервера: `{ctx.guild.id}`
├ :asterisk: × ID шарда: `{ctx.guild.shard_id}`
├ :heavy_check_mark: × Уровень верификации: `{vlevels[str(ctx.guild.verification_level)]}`
├ :triangular_flag_on_post: × Регион: `{rgs.get(str(ctx.guild.region)) if rgs.get(str(ctx.guild.region)) else str(ctx.guild.region)}`
├ :crown: × Владелец сервера: `{ctx.guild.owner if ctx.guild.owner else "Не определён"}`
└ :hourglass: × Дата и время создания сервера: `{ctx.guild.created_at.day}.{ctx.guild.created_at.month}.{ctx.guild.created_at.year}, {ctx.guild.created_at.hour}:{ctx.guild.created_at.minute}`**"""
        )
        embed.add_field(
            name='Каналы',
            value=f'''>>> **├ :books: × Всего: `{len(ctx.guild.channels)}`
├ :speech_balloon: × Текстовых: `{len(ctx.guild.text_channels)}`
├ :microphone2: × Голосовых: `{len(ctx.guild.voice_channels)}`
├ :open_file_folder: × Категорий: `{len(ctx.guild.categories)}`
├ :dividers: × Форумов: `{len(ctx.guild.forum_channels)}`
└ :radio: × Трибун: `{len(ctx.guild.stage_channels)}`**'''
        )
        embed.add_field(
            name='Роли',
            value=f'''>>> **├ :books: × Всего: `{len(ctx.guild.roles)}`
├ :tools: × С правами администратора: `{len([r for r in ctx.guild.roles if r.permissions.administrator])}`
├ :lock: × С правами модератора: `{len([r for r in ctx.guild.roles if r.permissions.kick_members])}`
└ :space_invader: × Интеграций: `{len([r for r in ctx.guild.roles if r.managed])}`**'''
        )
        embed.add_field(
            name='Участники',
            value=f'''>>> **├ :busts_in_silhouette: × Всего: `{ctx.guild.member_count}`
├ :busts_in_silhouette: × Людей: `{len([m for m in ctx.guild.members if not m.bot])}`
├ :tools: × С правами администратора: `{len([m for m in ctx.guild.members if m.guild_permissions.administrator])}`
├ :construction: × С правами `банить участников`: `{len([m for m in ctx.guild.members if m.guild_permissions.ban_members])}`
├ :construction: × С правами `кикать участников`: `{len([m for m in ctx.guild.members if m.guild_permissions.kick_members])}`
└ :space_invader: × Ботов: `{len([m for m in ctx.guild.members if m.bot])}`**'''
        )
        embed.add_field(
            name='Настройки',
            value=f'''>>> **├ :shield: × Анти-краш: `{await self.checkac(ctx.guild)}` запрещённых действий
├ :tools: × Статус анти-краш: {"`Включен` :white_check_mark:" if await self.checkac(ctx.guild) else "`Выключен` :x:"}
└ :space_invader: × Статус анти-бот: {"`Включен` :white_check_mark:" if await self.checkab(ctx.guild) else "`Выключен` :x:"}**'''
        )
        await ctx.send(embed=embed)

    @commands.slash_command(description='Информация о боте')
    async def info(self, ctx):
        await ctx.response.defer()
        sysinf = f'''>>> **├ :ping_pong: × Пинг бота: `{self.bot.latency * 1000:.0f} ms`
├ :asterisk: × Шардов: `{len(self.bot.shards)}`
└ :minidisc: × Потрачено памяти: `{round(memory_usage()[0], 2)} мб`**'''
        statsinf = f'''>>> **├ :gear: × Всего серверов: `{len(self.bot.guilds)}`
├ :chains: × Сервера от 30+ участников: `{len([g for g in self.bot.guilds if len(g.members) >= 30])}`
├ :first_place: × Сервера от 100+ участников: `{len([g for g in self.bot.guilds if len(g.members) >= 100])}`
├ :trophy: × Сервера от 1000+ участников: `{len([g for g in self.bot.guilds if len(g.members) >= 1000])}`
└ :busts_in_silhouette: × Пользователей: `{len([m for g in self.bot.guilds for m in g.members])}`**'''
        otherinf = f'''>>> **├ :snake: × Язык программирования `Python`
├ :label: × Библиотека: `disnake 2.6.0`
├ :open_file_folder: × База данных: `sqlite3`
├ :gear: × Версия бота: `{config.version}`
├ :calendar: × Дата создания бота: `{self.bot.user.created_at.day}.{self.bot.user.created_at.month}.{self.bot.user.created_at.year}`
└ :computer: × Разработчики бота: `se4lite#1392`**'''
        links2 = f'''**:link: [Добавить бота](https://discord.com/api/oauth2/authorize?client_id=1090683815963398194&permissions=8&scope=bot%20applications.commands)
└:link: [Сервер поддержки](https://discord.gg/{config.support_server})**'''
        thanks = '''**Never#0228 - за помощь в разработке бота**'''
        embed=disnake.Embed(title=':information_source: | Информация о боте', color=config.main_color)
        embed.add_field(name='Основная информация', value=sysinf, inline=True)
        embed.add_field(name='Статистика бота', value=statsinf, inline=True)
        embed.add_field(name='Прочее', value=otherinf)
        embed.add_field(name='Благодарности', value=thanks)
        embed.add_field(name='Полезные ссылки', value=links2, inline=True)
        await ctx.send(embed=embed)

    @commands.slash_command(description='Пинг бота')
    async def ping(self, ctx):
        embed = disnake.Embed(title=":ping_pong: | Пинг бота", description=f'>>> **Средняя задержка: `{int(self.bot.latency * 1000)} ms`**', color=config.main_color)
        shardsinf = '>>> '
        for shard in self.bot.shards:
            shardsinf += f'**Шард {shard}: `{int(self.bot.get_shard(shard).latency) * 1000} ms`**\n'
        embed.add_field(inline=False, name="По шардам", value=shardsinf)
        embed.set_footer(text=f'ID вашего шарда: {ctx.guild.shard_id}')
        await ctx.send(embed=embed)

    @commands.slash_command(description='Оперативная память')
    async def ram(self, ctx):
        embed = disnake.Embed(title=":cd: | Ram", description=f">>> **:floppy_disk: × Потрачено памяти: `{round(memory_usage()[0], 2)} MB`**", colour=config.main_color)
        await ctx.send(embed=embed)

    @commands.slash_command(description='Информация о пользователе')
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def user(self, ctx, user: disnake.User = None):
        months = {
            1: "января",
            2: "февраля",
            3: "марта",
            4: "апреля",
            5: "мая",
            6: "июня",
            7: "июля",
            8: "августа",
            9: "сентября",
            10: "октября",
            11: "ноября",
            12: "декабря"
        }
        if user is None:
            user = ctx.author
        embed = disnake.Embed(color=config.main_color)
        if user.bot:
            embed.title = f":space_invader: | Информация о боте **{user}**"
        else:
            embed.title = f":bust_in_silhouette: | Информация о пользователе **{user}**"
        #print(user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f'ID: {user.id}')
        if ctx.guild.get_member(user.id):
            user = ctx.guild.get_member(user.id)
            embed.add_field(inline=False, name="Роли", value=f'Всего: **{len(user.roles)}**\nНаивысшая роль: {user.top_role.mention}')
            if user == ctx.guild.owner:
                embed.add_field(inline=True, name="Владелец сервера?", value='Да :white_check_mark:')
            else:
                embed.add_field(inline=True, name="Владелец сервера?", value='Нет :x:')
                if user.guild_permissions.administrator:
                    embed.add_field(inline=True, name="Администратор?", value='Да :white_check_mark:')
                else:
                    embed.add_field(inline=True, name="Администратор?", value='Нет :x:')
            ja = user.joined_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            embed.add_field(inline=False, name="Дата присоединения к серверу", value=f'<t:{int(ja.timestamp())}> (<t:{int(ja.timestamp())}:R>)')
        ca = user.created_at
        embed.add_field(inline=False, name="Дата создания аккаунта", value=f'<t:{int(ca.timestamp())}> (<t:{int(ca.timestamp())}:R>)')
        await ctx.send(embed=embed)

    @commands.slash_command(description="Аватар пользователя")  # optional
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        emb = disnake.Embed(title=f"Аватарка пользователя {user}", color=config.main_color)
        emb.set_image(url=user.display_avatar.url)
        await inter.response.send_message(embed=emb)


    @commands.user_command(name="Информация о пользователе")  # optional
    async def infouser(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        embed = disnake.Embed(color=config.main_color)
        if user.bot:
            embed.title = f":space_invader: | Информация о боте **{user}**"
        else:
            embed.title = f":bust_in_silhouette: | Информация о пользователе **{user}**"
        embed.set_thumbnail(url=user.avatar)
        embed.set_footer(text=f'ID: {user.id}')
        if inter.guild.get_member(user.id):
            user = inter.guild.get_member(user.id)
            embed.add_field(inline=False, name="Роли", value=f'Всего: **{len(user.roles)}**\nНаивысшая роль: {user.top_role.mention}')
            if user == inter.guild.owner:
                embed.add_field(inline=True, name="Владелец сервера?", value='Да :white_check_mark:')
            else:
                embed.add_field(inline=True, name="Владелец сервера?", value='Нет :x:')
                if user.guild_permissions.administrator:
                    embed.add_field(inline=True, name="Администратор?", value='Да :white_check_mark:')
                else:
                    embed.add_field(inline=True, name="Администратор?", value='Нет :x:')
            ja = user.joined_at.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            embed.add_field(inline=False, name="Дата присоединения к серверу", value=f'<t:{int(ja.timestamp())}> (<t:{int(ja.timestamp())}:R>)')
        ca = user.created_at
        embed.add_field(inline=False, name="Дата создания аккаунта", value=f'<t:{int(ca.timestamp())}> (<t:{int(ca.timestamp())}:R>)')
        await inter.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))