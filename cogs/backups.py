import sqlite3
from disnake.ui import Select, Button, ActionRow
from disnake import AppCommandInter, AppCommandInteraction, SelectOption, ButtonStyle
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
import json
import config


class Backups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

    async def delall(self, ctx):
        for chann in ctx.guild.channels:
            if chann != ctx.channel:
                try:
                    await chann.delete()
                except:
                    pass
                else:
                    pass
        for role in ctx.guild.roles:
            try:
                await role.delete()
            except:
                pass
            else:
                pass 

    def getColor(self, arg):
        return tuple(int(arg.strip('#')[i:i + 2], 16) for i in (0, 2, 4))

    async def saveroles(self, ctx):
        self.cur.execute("DELETE FROM roles WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        yesn = {False: 'NO', True: 'YES'}
        for role in ctx.guild.roles:
            if not role.managed and not role == ctx.guild.default_role:
                self.cur.execute("INSERT INTO roles VALUES (?, ?, ?, ?, ?, ?, ?)", (ctx.guild.id, role.name, role.permissions.value, role.position, yesn[role.hoist], yesn[role.mentionable], str(role.color)))
                self.db.commit()
    
    async def savecategories(self, ctx):
        self.cur.execute("DELETE FROM categories WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        for i in ctx.guild.categories:
            compact = {}
            for role, ovw in i.overwrites.items():
                allow, deny = ovw.pair()
                compact[role.name] = {'a':allow.value, 'd':deny.value}
            self.cur.execute("INSERT INTO categories VALUES (?, ?, ?, ?)", (ctx.guild.id, i.name, json.dumps(compact), i.position))
            self.db.commit()

    async def savetextchannels(self, ctx):
        self.cur.execute("DELETE FROM text_channels WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        yesn = {False: 'NO', True: 'YES'}
        for i in ctx.guild.text_channels:
            compact = {}
            for role, ovw in i.overwrites.items():
                allow, deny = ovw.pair()
                compact[role.name] = {'a':allow.value, 'd':deny.value}
            self.cur.execute("INSERT INTO text_channels VALUES (?, ?, ?, ?, ?, ?, ?)", (ctx.guild.id, i.name, json.dumps(compact), i.position, f'{i.category.name if i.category else "NONE"}', yesn[i.nsfw], i.slowmode_delay, i.topic, i.overwrites))
            self.db.commit()

    async def savevoicechannels(self, ctx):
        self.cur.execute("DELETE FROM voice_channels WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        for i in ctx.guild.voice_channels:
            compact = {}
            for role, ovw in i.overwrites.items():
                allow, deny = ovw.pair()
                compact[role.name] = {'a':allow.value, 'd':deny.value}
            self.cur.execute("INSERT INTO voice_channels VALUES (?, ?, ?, ?, ?)", (ctx.guild.id, i.name, json.dumps(compact), i.position, f'{i.category.name if i.category else "NONE"}'))
            self.db.commit()
        
    async def savestagechannels(self, ctx):
        self.cur.execute("DELETE FROM stage_channels WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        for i in ctx.guild.stage_channels:
            compact = {}
            for role, ovw in i.overwrites.items():
                allow, deny = ovw.pair()
                compact[role.name] = {'a':allow.value, 'd':deny.value}
            self.cur.execute("INSERT INTO stage_channels VALUE (?, ?, ?, ?, ?, ?)")
            self.db.commit()
            
    async def saveforumchannels(self, ctx):
        self.cur.execute("DELETE FROM forum_channels WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        for i in ctx.guild.forum_channels:
            compact = {}
            for role, ovw in i.overwrites.items():
                allow, deny = ovw.pair()
                compact[role.name] = {'a':allow.value, 'd':deny.value}
            self.cur.execute("INSERT INTO forum_channels VALUE (?, ?, ?, ?, ?)")
            self.db.commit()

    async def saveguildname(self, ctx):
        self.cur.execute("DELETE FROM serversNames WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        self.cur.execute("INSERT INTO serversNames VALUES (?, ?)", (ctx.guild.id, ctx.guild.name))
        self.db.commit()
        
    async def saveguildicon(self, ctx):
        self.cur.execute("DELETE FROM serversIcons WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        self.cur.execute("INSERT INTO serversIcons VALUE (?, ?)", (ctx.guild.id, ctx.guild.icon))
        self.db.commit()

    async def getroles(self, ctx):
        return self.cur.execute("SELECT * FROM roles WHERE guild_id = {}".format(ctx.guild.id)).fetchall()

    async def getcategories(self, ctx):
        return self.cur.execute("SELECT * FROM categories WHERE guild_id = {}".format(ctx.guild.id)).fetchall()

    async def gettextchannels(self, ctx):
        return self.cur.execute("SELECT * FROM text_channels WHERE guild_id = {}".format(ctx.guild.id)).fetchall()

    async def getvoicechannels(self, ctx):
        return self.cur.execute("SELECT * FROM voice_channels WHERE guild_id = {}".format(ctx.guild.id)).fetchall()

    async def getguildname(self, ctx):
        return self.cur.execute("SELECT name FROM serversNames WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    
    async def getguildicon(self, ctx):
        return self.cur.execute("SELECT * FROM serversIcons WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
    
    async def getforumchannels(self, ctx):
        return self.cur.execute("SELECT * FROM forum_channels WHERE guild_id = {}".format(ctx.guild.id)).fetchall()
    
    async def getstagechannels(self, ctx):
        return self.cur.execute("SELECT * FROM stage_channels WHERE guild_id = {}".format(ctx.guild.id)).fetchall()

    async def restoreroles(self, ctx):
        for role in await self.getroles(ctx):
            col = self.getColor(role[6])
            yesn = {'YES': True, 'NO': False}
            rollee = await ctx.guild.create_role(
                name=role[1],
                color=disnake.Colour.from_rgb(col[0], col[1], col[2]),
                permissions=disnake.Permissions._from_value(role[2]),
                hoist=yesn[role[4]],
                mentionable=yesn[role[5]]
            )
            await rollee.edit(position=role[3])

    async def restorechannels(self, ctx):
        categories = await self.getcategories(ctx)
        text_channels = await self.gettextchannels(ctx)
        voice_channels = await self.getvoicechannels(ctx)
        yesn = {'YES': True, 'NO': False}
        for c in categories:
            ovws = {}
            raw_ovw = json.loads(c[2])
            for role in ctx.guild.roles:
                try:
                    ovw = disnake.PermissionOverwrite.from_pair(disnake.Permissions(permissions=raw_ovw[role.name]['a']), disnake.Permissions(permissions=raw_ovw[role.name]['d']))
                    ovws[role] = ovw
                except:
                    pass
            await ctx.guild.create_category(
                name=c[1],
                overwrites=ovws,
                position=c[3]
            )
        for c in text_channels:
            ovws = {}
            raw_ovw = json.loads(c[2])
            for role in ctx.guild.roles:
                try:
                    ovw = disnake.PermissionOverwrite.from_pair(disnake.Permissions(permissions=raw_ovw[role.name]['a']), disnake.Permissions(permissions=raw_ovw[role.name]['d']))
                    ovws[role] = ovw
                except:
                    pass
            if c[4] == 'NONE':
                await ctx.guild.create_text_channel(
                    name=c[1],
                    overwrites=ovws,
                    position=c[3],
                    nsfw=yesn[c[5]],
                    slowmode_delay=c[6]
                )
            else:
                await ctx.guild.create_text_channel(
                    name=c[1],
                    overwrites=ovws,
                    position=c[3],
                    category=disnake.utils.get(ctx.guild.categories, name=c[4]),
                    nsfw=yesn[c[5]],
                    slowmode_delay=c[6]
                )
        for c in voice_channels:
            ovws = {}
            raw_ovw = json.loads(c[2])
            for role in ctx.guild.roles:
                try:
                    ovw = disnake.PermissionOverwrite.from_pair(disnake.Permissions(permissions=raw_ovw[role.name]['a']), disnake.Permissions(permissions=raw_ovw[role.name]['d']))
                    ovws[role] = ovw
                except:
                    pass
            if c[4] == 'NONE':
                await ctx.guild.create_voice_channel(
                    name=c[1],
                    overwrites=ovws,
                    position=c[3]
                )
            else:
                await ctx.guild.create_voice_channel(
                    name=c[1],
                    overwrites=ovws,
                    position=c[3],
                    category=disnake.utils.get(ctx.guild.categories, name=c[4])
                )

    async def restoreguildname(self, ctx):
        nam = await self.getguildname(ctx)
        try:
            await ctx.guild.edit(name=nam[0])
        except:pass
        
    async def restoreguildicon(self, ctx):
        ico = await self.getguildicon(ctx)
        try:
            await ctx.guild.edit(icon=ico[0])
        except:
            pass
        
    @commands.slash_command(description='Бэкап сервера')
    async def backup(self, ctx: AppCommandInteraction):
        if not ctx.invoked_subcommand:
            embed = disnake.Embed(
                title=':question: | Помощь',
                color=config.main_color
            )
            embed.add_field(name='Параметры команды whitelist', value=f'''>>> **{ctx.prefix}backup create - `сохранить сервер`
{ctx.prefix}backup load - `загрузить бекап`
{ctx.prefix}backup delete - `удалить бекап`
{ctx.prefix}backup check - `проверить был ли создан бекап сервера`**''')
            await ctx.send(embed=embed)
        pass
    
    @backup.sub_command(description='Создать бэкап сервера')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def create(self, ctx: disnake.AppCommandInteraction):
        mess = await ctx.send(
            embed=disnake.Embed(
                title=':warning: | Предупреждение',
                description='>>> **Данный процесс пересоздаст бэкап сервера, если он был создан ранее\nПродолжить ?**',
                color=config.warning_color
            ),
            components=[
                ActionRow(
                    Button(label='Да', style=ButtonStyle.green, custom_id='yees'),
                    Button(label='Нет', style=ButtonStyle.red, custom_id='noo')
                )
            ]
        )
        m = await ctx.original_message()
        inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
        if inter.component.custom_id == 'yees':
            #try: await inter.respond(type=6)
            #except: pass
            await inter.response.edit_message(embed=disnake.Embed(title=':hourglass: | Ожидание..', description='>>> **Начинаю сохранение сервера**', color=config.main_color), components=[])
            await self.saveguildname(ctx)
            await self.saveroles(ctx)
            await self.savecategories(ctx)
            await self.savetextchannels(ctx)
            await self.savevoicechannels(ctx)
            await ctx.edit_original_response(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Бэкап создан, чтобы загрузить его пропиши `/backup load`**', color=config.success_color))
        else:
            #try: await inter.respond(type=6)
            #except: pass
            await inter.response.edit_message(embed=disnake.Embed(title=':no_entry_sign: | Отмена', description='>>> **Действие отменено**', color=config.main_color), components=[])

    @backup.sub_command(description='Загрузить бэкап сервера')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def load(self, ctx: AppCommandInteraction):
        if await self.getroles(ctx) == [] and await self.getcategories(ctx) == [] and await self.gettextchannels(ctx) == [] and await self.getvoicechannels(ctx) == [] and await self.getguildname(ctx) == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Бэкап ещё не был создан, чтобы создать его пропиши `/backup create`**', color=config.error_color))
        mess = await ctx.send(embed=disnake.Embed(title=':hourglass: | Ожидание..', description='>>> **Начинаю загрузу бекапа сервера, подожди..**', color=config.main_color))
        await self.delall(ctx)
        await self.restoreguildname(ctx)
        await self.restoreroles(ctx)
        await self.restorechannels(ctx)
        await self.restoreguildicon(ctx)
        await ctx.edit_original_response(embed = disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Бэкап загружен**', color=config.success_color))

    @backup.sub_command(description='Удалить бэкап')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def delete(self, ctx):
        if await self.getroles(ctx) == [] and await self.getguildicon(ctx) == [] and await self.getcategories(ctx) == [] and await self.gettextchannels(ctx) == [] and await self.getforumchannels(ctx) == [] and await self.getstagechannels(ctx) == [] and await self.getvoicechannels(ctx) == [] and await self.getguildname(ctx) == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **Бэкап ещё не был создан**', color=config.error_color))
        mess = await ctx.send(
            embed=disnake.Embed(
                title=':warning: | Предупреждение',
                description='>>> **Данный процесс удалит бэкап сервера, если с сервером что-то случится, вы не сможете его восстановить\nПродолжить ?**',
                color=config.warning_color
            ),
            components=[
                ActionRow(
                    Button(label='Да', style=ButtonStyle.green, custom_id='yees'),
                    Button(label='Нет', style=ButtonStyle.red, custom_id='noo')
                )
            ]
        )
        m = await ctx.original_message()
        inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
        if inter.component.custom_id == 'yees':
            #try: await inter.respond(type=6)
            #except: pass
            self.cur.execute("DELETE FROM serversNames WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM voice_channels WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM text_channels WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM categories WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM roles WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM serversIcons WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM stage_channels WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            self.cur.execute("DELETE FROM forum_channels WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            
            await inter.response.edit_message(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Бэкап удалён**', color=config.success_color), components=[])
        else:
            #try: await inter.respond(type=6)
            #except: pass
            await inter.response.edit_message(embed=disnake.Embed(title=':no_entry_sign: | Отмена', description='>>> **Действие отменено**', color=config.main_color), components=[])

    @backup.sub_command(description='Проверить бэкап')
    async def check(self, ctx):
        if await self.getroles(ctx) == [] and await self.getcategories(ctx) == [] and await self.getguildicon(ctx) == [] and await self.getstagechannels(ctx) == [] and await self.getforumchannels(ctx) == [] and await self.gettextchannels(ctx) == [] and await self.getvoicechannels(ctx) == [] and await self.getguildname(ctx) == None:
            embed = disnake.Embed(title=':file_folder: | Бэкап', description=f'>>> **Бэкап ещё не был создан, чтобы создать его пропиши `/backup create`**', color=config.main_color)
        else:
            embed = disnake.Embed(title=':file_folder: | Бэкап', description='>>> **Бэкап сервера уже создан**', color=config.main_color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Backups(bot))