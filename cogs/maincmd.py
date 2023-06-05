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
import requests
import random
import asyncio
import time
import datetime
from datetime import datetime as dt
import typing
from colorama import Fore, init
import adms

init()

import database
import times
import config


class MainCMD(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = sqlite3.connect('data.db')
		self.cur =self.db.cursor()

	async def get_prefix(self, guild):
		prefix = self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(guild.id)).fetchone()
		if prefix is None:
			return config.default_prefix[0]
		else:
			return prefix[0]

	@commands.slash_command(description='Справка о командах бота')
	async def help(self, ctx):
		embed = disnake.Embed(
			title=':question: | Помощь',
			description='>>> **Выбери опцию в меню под сообщением\nПодсказки:\n<> - Обязательный аргумент\n[] - Необязательный аргумент**',
			color=config.main_color
		)
		menu = [
			Select(
				placeholder='Выберите опцию...',
				options=[
					SelectOption(label='Настройки', emoji='<:gear:1025858080803651665>', description='Помощь по настройкам бота', value='settss_g'),
					SelectOption(label='Информация', emoji='<:471713:1025862037768765500>', description='Команды информации', value='infoo_g'),
					SelectOption(label='Модерация', emoji='<:5632549:1025858065595117648>', description='Помощь по командам модерации', value='moodd_g'),
					SelectOption(label='Фан', emoji='<:121202:1026122136559030324>', description='Помощь по фан командам', value='funn_g'),
					SelectOption(label='Утилиты', emoji='<:2963823:1026124476913561710>', description='Помощь по утилитам', value='utill_g')
				]
			)
		]
		return await ctx.send(embed=embed, components=menu)

	@commands.Cog.listener()
	async def on_dropdown(self, inter):
		#print(type(inter))
		if inter.message.author == inter.guild.me:
			embed = disnake.Embed(
				title=':question: | Помощь',
				color=config.main_color
			)
			p = await self.get_prefix(inter.guild)
			if inter.values[0] == 'settss_g':
				embed.add_field(
					name='Настройки',
					value=f'''>>> **/whitelist - `Белый список`
/antibot - `Включить/Выключить анти-бот`
/anticrash - `Включить/Выключить анти-краш`
/muterole [роль] - `Пометить роль мута`**'''
				)
			if inter.values[0] == 'infoo_g':
				embed.add_field(
					name=':information_source: | Информация',
					value=f'''>>> **/info - `Информация о боте`
/ping - `Пинг бота`
/ram - `Потраченая память`
/user `<@пользователь>` - `Информация о пользователе`
/serverinfo - `Информация о сервере`
/emojiinfo <эмодзи> - `Информация о эмодзи`**'''
				)
			if inter.values[0] == 'moodd_g':
				embed.add_field(
					name=':shield: | Модерация',
					value=f'''>>> **/kick `<@участник>` [причина] - `Кикнуть участника`
/ban `<@участник>` [причина] - `Забанить участника`
/lock - `Закрыть чат`
/unlock - `Открыть чат`
/clear [кол-во] - `Очистить чат`
/quarantine - `Управление карантином`
/mute `<@участник>` [причина] [время] - `Замутить участника`
/unmute `<@участник>` - `Размутить участника`
/slowmode <задержка> - `Поставить задержку на канал`**'''
				)
			if inter.values[0] == 'funn_g':
				embed.add_field(
					name='Фан команды',
					value=f'''>>> **/ball `<вопрос>` - `Задать вопрос магическому шару`
/ben `<вопрос>`- `Задать вопрос бену`
/say - `Сказать от имени бота`
/coin - `Подбросить монетку`
/popit - `Поп-ит`
/simple dimple - `Симпл димпл`
/animals - `Показывает картинки с изображением животных`
/shorturl <ссылка> - `Сделать ссылку короткой`**'''
				)
			if inter.values[0] == 'utill_g':
				embed.add_field(
					name='Утилиты',
					value=f'''>>> **/delspamchannels - `Удалить спам каналы`
/delspamroles - `Удалить спам роли`
/delspamwebhooks - `Удалить спам вебхуки`
/unbanall - `Разбанить всех`
/giveroleall `<@роль>` - `Выдать роль всем участникам`
/removeroleall `<@роль>` - `Забрать роль у всех участников`
/backup - `Бэкап сервера`**''')
			await inter.response.edit_message(embed=embed)
			#try: await inter.respond(type=6)
			#except: pass
			#добавляй есл чё новые команды в хелп

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.guild:
			if self.bot.user.mention in message.content:
				self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(message.guild.id))
				prefix = self.cur.fetchone()
				if prefix is None:
					prefix = config.default_prefix[0]
				else:
					prefix = prefix[0].lower()
				embed = disnake.Embed(title=':question: | Помощь', description=f'>>> **Привет, {message.author.mention}!\nМой префикс на этом сервере: `/`, используйте `/help` чтобы посмотреть список моих команд.**', colour=config.main_color)
				await message.reply(embed=embed)

	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропишите /help**', color=config.error_color))
			#await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Бот перешёл на слеш-команды, пропиши `/.` и потом листай команды бота.**', color=config.error_color))
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Команда на перезарядке, подожди {times.hms(error.retry_after)}**', color=config.error_color))
		elif isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Не верные аргументы команды, пропиши `/.help` чтобы ознакомиться с командами бота**', color=config.error_color))
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

	@commands.Cog.listener()
	async def on_slash_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Введённая команда не найдена.\nЧтобы ознакомиться со списком команд пропииши /help**', color=config.error_color))
		elif isinstance(error, commands.CommandOnCooldown):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Команда на перезарядке, подожди {times.hms(error.retry_after)}**', color=config.error_color))
		elif isinstance(error, commands.BadArgument) or isinstance(error, commands.BadUnionArgument):
			await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Не верные аргументы команды, пропиши `/help` чтобы ознакомиться с командами бота**', color=config.error_color))
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

def setup(bot):
	bot.add_cog(MainCMD(bot))