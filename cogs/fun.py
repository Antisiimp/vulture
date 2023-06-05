import sqlite3
import disnake
from disnake.ext import commands
import json
import io
import contextlib
import textwrap
import os
import aiohttp
import pyshorteners
import requests
from googletrans import Translator
from disnake import SelectOption, ButtonStyle
import random
import asyncio
import time
import datetime
from datetime import datetime as dt
import typing
from colorama import Fore, init
from memory_profiler import memory_usage
import httpx
init()

import msgs
import database
import config

requests = httpx.AsyncClient()
translator = Translator()
class AnimalsButton(disnake.ui.View):
	@disnake.ui.button(label="Лиса", style=disnake.ButtonStyle.grey, emoji="🦊")
	async def fox(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото лисы',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/fox')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Собака", style=disnake.ButtonStyle.grey, emoji="🐶")
	async def dog(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото собаки',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/dog')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Кот", style=disnake.ButtonStyle.grey, emoji="🐱")
	async def cat(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото кота',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/cat')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Панда", style=disnake.ButtonStyle.grey, emoji="🐼")
	async def pandas(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото панды',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/panda')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Птица", style=disnake.ButtonStyle.grey, emoji="🐦")
	async def bird(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото птицы',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/bird')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Енот", style=disnake.ButtonStyle.grey, emoji="🦝")
	async def raccon(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото енота',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/raccoon')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	@disnake.ui.button(label="Кенгуру", style=disnake.ButtonStyle.grey, emoji="🦘")
	async def kangaroo(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
		embed = disnake.Embed( title = f'Фото кенгуру',color=config.main_color)
		response = await requests.get(f'https://some-random-api.ml/img/kangaroo')
		json_data = json.loads(response.text) 
		embed.set_image(url = json_data['link'])
		await interaction.response.edit_message(embed = embed)

	# @disnake.ui.button(label="Коза", style=disnake.ButtonStyle.grey, emoji="🐐")
	# async def lox(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
	# 	embed = disnake.Embed( title = f'Фото козы',color=config.main_color)
	# 	embed.set_image(url = 'https://cdn.discordapp.com/avatars/913825600790200330/a_0bb0078c1a795f27039ef6b96d960c6d.png?size=1024')
	# 	await interaction.response.edit_message(embed = embed)
		#добавь сюда GidesPC куда #
class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.slash_command(description='Задать вопрос магическому шару')
	@commands.cooldown(1, 5, commands.BucketType.guild)
	async def ball(self, ctx, вопрос):
		await ctx.response.defer()
		answers = ['Бесспорно :thumbsup:',
'Предрешено :thumbsup:',
'Никаких сомнений :thumbsup:',
'Определённо да :ok_hand:',
'Можешь быть уверен в этом :ok_hand:',
'Мне кажется — «да» :ok_hand:',
'Вероятнее всего :ok_hand:',
'Хорошие перспективы :ok_hand:',
'Знаки говорят — «да» :white_check_mark:',
'Да :ok_hand:',
'Пока не ясно, попробуй снова :eyes:',
'Спроси позже :eyes:',
'Лучше не рассказывать :eyes:',
'Сейчас нельзя предсказать :thinking:',
'Сконцентрируйся и спроси опять :eyes:',
'Даже не думай :x:',
'Мой ответ — «нет» :no_entry:',
'По моим данным — «нет» :no_entry_sign:',
'Перспективы не очень хорошие :no_entry:',
'Весьма сомнительно :x:']
		await ctx.send(random.choice(answers))
		
	@commands.slash_command(description='Подбросить монетку')
	async def coin(self, ctx):
		await ctx.response.defer()
		randomIntOR = random.randint(0, 1)
		if randomIntOR == 0:
			randomIntORoutput = "орёл"
		else:
			randomIntORoutput = "решка"
		await ctx.send(f"Посмотрим... О, тебе выпал {randomIntORoutput}!")
		
	@commands.slash_command(name='simple')
	async def simple(self, ctx):
		pass

	@commands.Cog.listener()
	async def on_button_click(self, ctx):
		if ctx.component.custom_id == "simpledimple":
			embed = disnake.Embed(title=f'Симпл-димпл', description=f"""
:black_large_square::black_large_square::black_large_square:
:black_large_square:||:yellow_square:||:black_large_square:
:black_large_square::black_large_square::black_large_square:
:black_large_square:||:blue_square:||:black_large_square:
:black_large_square::black_large_square::black_large_square:""",
			color=config.main_color)
			buttons = disnake.ui.View()
			buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id="simpledimple",label='Ещё!'))
			await ctx.send(embed=embed, view=buttons, ephemeral=True)
		if ctx.component.custom_id == "popit":
			cpage = disnake.Embed(
			title = 'Поп-ит',
			description = f'''
||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||
||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||
||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||
||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||''', 
			color=config.main_color
		)
		buttons = disnake.ui.View()
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id="popit",label='Ещё!'))
		await ctx.send(embed=cpage, view=buttons, ephemeral=True)
	@simple.sub_command(name='dimple', description='Симпл димпл')
	async def dimple(self, ctx):
				await ctx.response.defer()
				embed = disnake.Embed(title=f'Симпл-димпл', description=f"""
:black_large_square::black_large_square::black_large_square:
:black_large_square:||:yellow_square:||:black_large_square:
:black_large_square::black_large_square::black_large_square:
:black_large_square:||:blue_square:||:black_large_square:
:black_large_square::black_large_square::black_large_square:""",
				color=config.main_color)
				buttons = disnake.ui.View()
				buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id="simpledimple",label='Ещё!'))
				await ctx.send(embed=embed, view=buttons)

	@commands.slash_command(name='popit', description='Анти-стресс поп-ит')
	async def popit(self, ctx):
		await ctx.response.defer()
		cpage = disnake.Embed(
			title = 'Поп-ит',
			description = f'''
||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||||:red_square:||
||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||||:yellow_square:||
||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||||:green_square:||
||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||||:blue_square:||
||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||||:purple_square:||''', 
			color=config.main_color
		)
		buttons = disnake.ui.View()
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id="popit",label='Ещё!'))
		await ctx.send(embed=cpage, view=buttons)

	@commands.slash_command(description='Сыграть в казино')
	async def casino(ctx):
		await ctx.response.defer()
		winlist = ["⬜⬜⬜\n⬜⬜⬜\n⬜⬜⬜","🟧🟧🟧\n🟧🟧🟧\n🟧🟧🟧","🟦🟦🟦\n🟦🟦🟦\n🟦🟦🟦","🟥🟥🟥\n🟥🟥🟥\n🟥🟥🟥","🟪🟪🟪\n","🟩🟩🟩\n🟩🟩🟩\n🟩🟩🟩","🟨🟨🟨\n🟨🟨🟨\n🟨🟨🟨"]
		loselist = ["🟩🟪🟦\n🟥🟧🟨\n🟦🟪🟧","🟨🟧🟪\n🟧🟩⬛\n🟧🟦🟨","⬜⬜🟥\n⬜🟧⬜\n🟥⬜🟦","🟦🟧⬜\n🟥🟩🟨\n🟦🟨🟪","🟩⬜🟩\n🟨🟩🟧\n🟨🟧🟩","🟩🟪🟩\n🟪🟧🟥\n🟫🟩🟥","🟨🟥🟪\n🟪🟩🟧\n🟫🟪🟨","⬜🟦🟥\n🟥🟪🟩\n🟦🟥🟫","🟦🟧🟨\n🟧🟩🟨\n🟥🟨🟨","🟩⬜🟪\n🟪🟫🟦\n⬜⬛🟧","🟨🟦⬜\n⬜⬛🟧\n🟪🟥🟧"]
		winorlose = ["yes","no","no","no","no"]
		rndwin = random.choice(winlist)
		rndlose = random.choice(loselist)
		wol = random.choice(winorlose)
		if wol == "yes":
			embed = disnake.Embed(title='Ты выиграл', description=rndwin, color=config.success_color)
			await ctx.send(embed=embed)
		elif wol == "no":
			embed = disnake.Embed(title='Ты проиграл', description=rndlose, color=config.error_color)
			await ctx.send(embed=embed)

	@commands.slash_command(description='Задать вопрос Бену')
	async def ben(self, ctx, *, вопрос):
				await ctx.response.defer()
				OTVET = ["No", "Yes", "Hohoho", "Ugh"]
				OTVETA = random.choice(OTVET)
				embedben = disnake.Embed(title="Бен",description=f"На вопрос `{вопрос}` Бен ответил: \n **{OTVETA}**", color=config.main_color)
				if OTVETA == "Ugh":
					embedben.set_image(url="https://c.tenor.com/fr6i8VzKJuEAAAAd/talking-ben-ugh.gif")
					await ctx.send(embed=embedben)
				elif OTVETA == "Hohoho":
					embedben.set_image(url="https://c.tenor.com/agrQMQjQTzgAAAAd/talking-ben-laugh.gif")
					await ctx.send(embed=embedben)
				elif OTVETA == "Yes":
					embedben.set_image(url="https://c.tenor.com/6St4vNHkyrcAAAAd/yes.gif")
					await ctx.send(embed=embedben)
				elif OTVETA == "No":
					embedben.set_image(url="https://c.tenor.com/x2u_MyapWvcAAAAd/no.gif")
					await ctx.send(embed=embedben)

	@commands.slash_command(description='Сделать ссылку короткой')
	async def shorturl(ctx, url):
			# await ctx.response.defer()
			s = pyshorteners.Shortener()
			shorten = s.tinyurl.short(url)
			await ctx.send(embed=disnake.Embed(title=":link: | Твоя ссылка",description=shorten,color=config.main_color),ephemeral=True)   

	@commands.slash_command(description='Картинки животных')
	async def animals(self, ctx):
		await ctx.response.defer()
		await ctx.response.send_message(embed = disnake.Embed(title = 'Животные', description='Выбери кнопку, для просмотров животных', color=config.main_color), view=AnimalsButton())

	@commands.slash_command(description='Рандомные мемы')
	async def meme(self, inter):
		await inter.response.defer()
		response = requests.get('https://some-random-api.ml/meme')
		json_data = json.loads(response.text)
		embed = disnake.Embed(color=config.main_color, title = 'Мемы', description = json_data['caption'])
		embed.set_image(url = json_data['image'])
		await inter.send(embed = embed)
     
	"""@commands.Cog.listener()
	async def on_button_click(ctx, button):
	ennmaes = ["fox", "dog", "cat", "panda"]
	runmaes = ["Лисы", "Собаки", "Коты", "Панды"]
	for i in range (0, 4):
		if button.custom_id == ennmaes[i]:
			embed = discord.Embed(title = f'Фото {runmaes[i]}', color = discord.Color.red())
			embed.set_footer(text=f'По запросу {ctx.author}')
			response = requests.get(f'https://some-random-api.ml/img/{ennmaes[i]}')
			json_data = json.loads(response.text) 
			embed.set_image(url = json_data['link']) 
			await ctx.message.edit(embed = embed, view=None)"""
                
    #@commands.command()
	"""async def animals(ctx):
         ennmaes = ["fox", "dog", "cat", "panda"]
	        runmaes = ["Лиса", "Собака", "Кот", "Панда"]	
	        em = ["🦊", "🐶", "🐱", "🐼"]
	       buttons = disnake.ui.View()
	        for i in range(0, 4):
	            buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.blurple, custom_id=ennmaes[i],label=runmaes[i], emoji=em[i]))
	         await ctx.response.send_message( embed = disnake.Embed( title = 'Животные', description='Выберите кнопку, для просмотров животных', color=config.main_color), view=buttons)
	@commands.message_command(name="Перевести на русский язык") #не забыай про self, это обязательно, ну я впервые в когах #параметр self ваще любая функция должна принимать, если ты в классе работаешь а погял
	async def translate_to_russian(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
		#print(message)
		#print(f"{message.content}")
		await inter.response.defer()
		try:
			translatedText = translator.translate(message.content, dest="ru")
			await msgs.succmess(inter, f"Сообщение [*{message.content}*]({message.jump_url}) преведено на русский язык\nПеревод: `{translatedText.text}`")
		except:
			await inter.send(embed=disnake.Embed(title='<:1828774:1025858045873487922> | Ошибка..', description='>>> **Не удалось перевести сообщение**', color=config.error_color))

	@commands.message_command(name="Перевести на английский язык")
	async def translate_to_english(self, inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
		#print(message)
		#print(f"{message.content}")
		await inter.response.defer()
		try:
			translatedText = translator.translate(message.content, dest="en")
			await msgs.succmess(inter, f"Сообщение [*{message.content}*]({message.jump_url}) преведено на английский язык\nПеревод: `{translatedText.text}`")
		except:
			await inter.send(embed=disnake.Embed(title='<:1828774:1025858045873487922> | Ошибка..', description='>>> **Не удалось перевести сообщение**', color=config.error_color))"""


def setup(bot):
	bot.add_cog(Fun(bot))