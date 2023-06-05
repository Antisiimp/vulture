from email import message
import sqlite3
from disnake.ui import ActionRow, Select, Button, View
from disnake import AppCommandInteraction, SelectOption, ButtonStyle
import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import io
import contextlib
import textwrap
import os
import aiohttp
import requests
import random
import pyshorteners
import asyncio
import time
import datetime
from datetime import datetime as dt
import typing
from colorama import Fore, init

init()

import database
import times
import config
import adms

class Say(disnake.ui.Modal):
	def __init__(self, bot):
		self.bot = bot  
		components = [
			disnake.ui.TextInput(
				label="Текст для сообщения",
				placeholder="Введи текст.",
				custom_id="messagetext",
				style=TextInputStyle.short,
				max_length=300,
			)
		]
		super().__init__(
			title="Сказать от имени бота",
			custom_id="create_say",
			components=components,
		)

	# Обработка ответа, после отправки модального окна
	async def callback(self, inter: disnake.ModalInteraction):		
		k = inter.text_values['messagetext'].format(
			**{
				"disnake": disnake,
				"commands": commands,
				"bot": self.bot,
				"client": self.bot,
				"db": database.db,
				"cur": database.cur,
				"sqlite3": sqlite3,
				"ctx": inter,
				"inter": inter,
				"channel": inter.channel,
				"author": inter.author,
				"guild": inter.guild,
				"message": inter.message,
				"config": config,
				"database": database
			}
		) 
		await inter.response.send_message("Текст скоро отправится.", ephemeral=True)
		await inter.channel.send(k)

class Util(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = sqlite3.connect('data.db')
		self.cur = self.db.cursor()

	async def del_channel(self, ctx, chann):
		try:
			await chann.delete()
		except:
			pass
		else:
			pass

	async def del_role(self, ctx, rolee):
		try:
			await rolee.delete()
		except:
			pass
		else:
			pass

	async def del_roles(self, ctx):
		#for role in ctx.guild.roles:
		#	asyncio.create_task(del_role(ctx, rolee=role))
		await asyncio.gather(*[self.del_role(ctx, role) for role in ctx.guild.roles])         
			
	@commands.slash_command(name='setup', description='Частичное восстановление сервера')
	@commands.cooldown(1, 60, commands.BucketType.default)
	@commands.check(adms.only_owner)
	async def setup(self, ctx):
		if ctx.guild.default_role.permissions.administrator:
			await ctx.guild.default_role.edit(permissions=disnake.Permissions(administrator=False, send_messages=True, view_channel=True, read_message_history=True))
		await ctx.guild.edit(name=f'Server {ctx.guild.owner.name if ctx.guild.owner else ctx.author.name} {random.choice(["Team", "Community", "Squad", "Group"])} (Тех работы)')
		message = await ctx.send(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Идёт восстановление сервера, подожди....**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		await asyncio.sleep(3)
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `1`\nУдаление каналов**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		await asyncio.gather(*[self.del_channel(ctx, c) for c in ctx.guild.channels if c != ctx.channel])
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `1` завершён, приступаю к `2` этапу\nУдаление ролей**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		await self.del_roles(ctx)
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `2` завершён, приступаю к `3` этапу\nСоздание категорий**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		category1 = await ctx.guild.create_category(name='main')
		await category1.set_permissions(ctx.guild.default_role, send_messages=False)
		category2 = await ctx.guild.create_category(name='general')
		category3 = await ctx.guild.create_category(name='voices')
		category4 = await ctx.guild.create_category(name='games')
		category5 = await ctx.guild.create_category(name='nsfw')
		category6 = await ctx.guild.create_category(name='admins only')
		category7 = await ctx.guild.create_category(name='owners only')
		await category7.set_permissions(ctx.guild.default_role, view_channel=False)
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `3` завершён, приступаю к `4` этапу\nСоздание ролей**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		owner = await ctx.guild.create_role(name='Owner', permissions=disnake.Permissions(administrator=True), hoist=True, mentionable=False)
		await ctx.author.add_roles(owner)
		botr = await ctx.guild.create_role(name='Bot', permissions=disnake.Permissions(administrator=True), hoist=True, mentionable=False)
		await ctx.guild.create_role(name='Co-Owner', permissions=disnake.Permissions(administrator=True), hoist=True, mentionable=False)
		await ctx.guild.create_role(name='Curator', permissions=disnake.Permissions(ban_members=True, kick_members=True, manage_roles=True, manage_nicknames=True, mute_members=True, manage_messages=True), hoist=True, mentionable=False)
		await ctx.guild.create_role(name='Administrator', permissions=disnake.Permissions(kick_members=True, manage_nicknames=True, mute_members=True), hoist=True, mentionable=False)
		await ctx.guild.create_role(name='Moderator', permissions=disnake.Permissions(manage_nicknames=True, mute_members=True), hoist=True, mentionable=False)
		mr = await ctx.guild.create_role(name='Member', hoist=True, mentionable=False, permissions=disnake.Permissions(send_messages=True, view_channel=True, read_message_history=True))
		await category6.set_permissions(ctx.guild.default_role, view_channel=False)
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `4` завершён, приступаю к `5` этапу\nСоздание каналов**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		for r in ['Curator', 'Administrator', 'Moderator']:
			await category6.set_permissions(disnake.utils.get(ctx.guild.roles, name=r), view_channel=True)
		for c in ['rules', 'news', 'info', 'updates', 'boosts', 'giveaways']:
			await ctx.guild.create_text_channel(name=c, sync_permissions=True, category=category1)
		for c in ['chat', 'toxic-chat', 'spam', 'bot-chat', 'offtop', 'rp-chat']:
			await ctx.guild.create_text_channel(name=c, sync_permissions=True, category=category2)
		await ctx.guild.create_text_channel(name='no-micro', category=category3)
		for c in ['Chat', 'Toxic Voice']:
			await ctx.guild.create_voice_channel(name=c, sync_permissions=True, category=category3)
		for c in ['minecraft', 'roblox', 'gta', 'cs-go', 'fortnite', 'pubg']:
			await ctx.guild.create_text_channel(name=c, sync_permissions=True, category=category4)
		for c in ['hentai', 'real-life', 'nsfw-chat', 'games', 'gays', 'other']:
			await ctx.guild.create_text_channel(name=c, sync_permissions=True, category=category5, nsfw=True)
		for c in ['admins-chat', 'admins-news', 'admins-info', 'logs']:
			await ctx.guild.create_text_channel(name=c, sync_permissions=True, category=category6)
		await ctx.guild.create_voice_channel(name='Admins Voice', sync_permissions=True, category=category6)
		await ctx.guild.create_text_channel(name='owners-chat', category=category7, sync_permissions=True)
		await ctx.guild.create_voice_channel(name='Owners Voice', category=category7)
		await message.edit(embed=disnake.Embed(title=':hourglass: | Ожидание...', description='>>> **Этап `5` завершён, приступаю к последнему этапу\nВыдача всем роли участника**', colour=disnake.Colour.from_rgb(0, 104, 214)))
		for m in ctx.guild.members:
			await m.add_roles(mr)
			if m.bot:
				await m.add_roles(botr)
		await message.edit(embed=disnake.Embed(title=':heavy_check_mark: | Успешно', description='>>> **Сервер восстановлен\nДа, хоть он и не такой как был до краша, но хоть как-то восстановлен**', colour=disnake.Colour.from_rgb(0, 104, 214)))

	@commands.slash_command(name='delspamchannels', description='Удалить спам каналы')
	@commands.check(adms.has_head_admin)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def delspamchannels(self, ctx: AppCommandInteraction, name=None):
		if name == None:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не указал имя каналов**', color=config.error_color))
		channels = [c for c in ctx.guild.channels if c.name == name and not c == ctx.channel]
		if channels == []:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нету каналов с таким названием**', color=config.error_color))
		deleted = 0
		count_channels = len(channels)
		mess = await ctx.send(embed = disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Начинаю удаление каналов с названием `{name}`**', color=config.main_color))
		await asyncio.sleep(3)     
		for channel in channels:
			try:
				await channel.delete()
			except:
				pass
			else:
				deleted += 1
				#await mess.edit(embed = disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Удалил `{deleted}` из `{count_channels}` спам каналов**', color=config.main_color))
		await ctx.edit_original_response(embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'>>> **Удалил `{deleted}` из `{count_channels}` спам каналов**', color=config.success_color))
				
	@commands.slash_command(description='Удалить спам роли')
	@commands.check(adms.has_head_admin)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def delspamroles(self, ctx: AppCommandInteraction, name=None):
		if name == None:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не указал имя ролей**', color=config.error_color))
		roles = [c for c in ctx.guild.roles if c.name == name]
		if roles == []:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Нету ролей с таким названием**', color=config.error_color))
		deleted = 0
		count_roles = len(roles)
		mess = await ctx.send(embed = disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Начинаю удаление ролей с названием `{name}`**', color=config.main_color))
		await asyncio.sleep(3)
		for role in roles:
			try:
				await role.delete()
			except:
				pass
			else:
				deleted += 1
				#await mess.edit(embed = disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Удалил `{deleted}` из `{count_roles}` спам ролей**', color=config.main_color))
		await ctx.edit_original_response(disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'>>> **Удалил `{deleted}` из `{count_roles}` спам ролей**', color=config.success_color))

	@commands.slash_command(description='Разбанить всех')
	@commands.check(adms.has_head_admin)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def unbanall(self, ctx: disnake.AppCommandInteraction):
		menu = [
			ActionRow(
				Button(label='Да', style=ButtonStyle.green, custom_id='yees'),
				Button(label='Нет', style=ButtonStyle.red, custom_id='noo')
			)
		]
		embed = disnake.Embed(
			title=':warning:| Предупреждение',
			description=f'>>> **Данный процесс может занять много времени, и разбанит __абсолютно всех__ пользователей\nПродолжить ?**',
			color=config.warning_color
		)
		mess = await ctx.send(embed=embed, components=menu)
		m = await ctx.original_message()
		inter = await self.bot.wait_for('button_click', check=lambda i: i.channel == ctx.channel and i.author == ctx.author and i.message.id == m.id)
		if inter.component.custom_id == 'yees':
			await inter.response.edit_message(embed=disnake.Embed(title=':hourglass: | Ожидание..', description='>>> **Начинаю разбан всех пользователей**', color=config.main_color), components=[])
			#await inter.respond(type=6)
			await asyncio.sleep(3)
			unbanned = 0
			bans = await ctx.guild.bans().flatten()
			banned = len(bans)
			for ban in bans:
				try:
					await ctx.guild.unban(ban.user)
				except:
					pass
				else:
					unbanned += 1
			#if unbanned == banned:
			await ctx.edit_original_response(embed=disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'>>> **Разбанено `{unbanned}` из `{banned}` забаненных пользователей**', color=config.success_color))
		else:
			await inter.response.edit_message(embed=disnake.Embed(title=':no_entry_sign: | Отмена', description='>>> **Действие отменено**', color=config.main_color), components=[])
			#await inter.respond(type=6)

	@commands.slash_command(description='Выдать роль всем')
	@commands.check(adms.has_head_admin)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def giveroleall(self, ctx: AppCommandInteraction, role: disnake.Role=None):
		if role == None:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты не указал роль**', color=config.error_color))
		if not isinstance(role, disnake.Role):
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты указал не роль**', color=config.error_color))
		if role.managed:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль является интеграцией**', color=config.error_color))
		if role.permissions.administrator:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Нельзя выдать эту роль, т.к она имеет права администратора**', color=config.error_color))
		if role.position >= ctx.author.top_role.position:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль выше/на уровне с тобой**', color=config.error_color))
		if role.position >= ctx.guild.me.top_role.position:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль выше/на уровне со мной**', color=config.error_color))
		mess = await ctx.send(embed=disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Начинаю выдачу всем роли {role.mention}**', color=config.main_color))
		givd = 0
		for member in ctx.guild.members:
			try:
				await member.add_roles(role)
			except:
				pass
			else:
				givd += 1
		await ctx.edit_original_response(embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'>>> **Выдал роль `{givd}` участникам**', color=config.success_color))
	
	@commands.slash_command(description='Забрать роль у всех')
	@commands.check(adms.has_head_admin)
	@commands.cooldown(1, 60, commands.BucketType.guild)
	async def removeroleall(self, ctx: AppCommandInteraction, role: disnake.Role=None):
		if role == None:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты не указал роль**', color=config.error_color))
		if not isinstance(role, disnake.Role):
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Ты указал не роль**', color=config.error_color))
		if role.managed:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль является интеграцией**', color=config.error_color))
		if role.position >= ctx.author.top_role.position:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль выше/на уровне с тобой**', color=config.error_color))
		if role.position >= ctx.guild.me.top_role.position:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Эта роль выше/на уровне со мной**', color=config.error_color))
		mess = await ctx.send(embed=disnake.Embed(title=':hourglass: | Ожидание..', description=f'>>> **Забираю у всех роль {role.mention}**', color=config.main_color))
		givd = 0
		for member in role.members:
			try:
				await member.remove_roles(role)
			except:
				pass
			else:
				givd += 1
		await ctx.edit_original_response(embed = disnake.Embed(title=':heavy_check_mark: | Успешно', description=f'>>> **Забрал роль у `{givd}` участников**', color=config.success_color))

	@commands.slash_command()
	@commands.check(adms.has_administrator)
	async def say(self, inter: disnake.AppCmdInter):
		"""Сказать от имени бота."""
		await inter.response.send_modal(modal=Say(self.bot))

	@commands.slash_command(description='Поставить задержку на канал')
	@commands.check(adms.has_administrator)
	@commands.cooldown(1, 15, commands.BucketType.guild)
	async def slowmode(self, ctx, slowmode='9h'):
		await ctx.response.defer()
		st = times.string_to_seconds(slowmode)
		if st >= 32400:
			return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Нельзя поставить задержку больше 9 часов**', color=config.error_color))
		await ctx.channel.edit(slowmode_delay=st) #мб через times сделаем давай а я пока эмбед сделаю
		await ctx.send(embed=disnake.Embed(title=":white_check_mark: | Успешно", description=f">>> **Задержка на сообщения в канале изменена на `{times.hms(float(st))}`**", color=config.success_color))


def setup(bot):
	bot.add_cog(Util(bot))