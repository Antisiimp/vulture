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
import config

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

    """
    @commands.group(name='prefix', aliases=['p'])
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=disnake.Embed(title=':question: | Помощь', colour=config.main_color)
            embed.add_field(
                name='Параметры команды muterole',
                value = f'''>>> **/prefix set <префикс> - `установить префикс на этом сервере`
/prefix reset - `сбросить префикс на этом сервере`**'''
            )
            await ctx.send(embed=embed)

    @prefix.command(name="reset")
    @commands.cooldown(1, 120)
    @commands.check(adms.has_administrator)
    async def reset_prefix(self, ctx):
        self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        prefix = self.cur.fetchone()
        if prefix is None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не можешь сбросить префикс на сервере, потому-что он не был установлен ранее.**', colour=config.error_color))
        self.cur.execute("DELETE FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере сброшен, теперь мой префикс на этом сервере `{config.default_prefix[0]}`.**', colour=config.success_color))

    @prefix.command(name="set", aliases=['s'])
    @commands.check(adms.has_administrator)
    async def set_prefix(self, ctx, prefix=None):
        if prefix == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Ты не указал префикс, который хочешь поставить на этом сервере.**', colour=config.error_color))
        if prefix in config.default_prefix:
            return await self.reset_prefix(ctx)
        self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        old_prefix = self.cur.fetchone()
        if old_prefix:
            if old_prefix[0] == prefix:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Указанный префикс уже выбран.**', colour=config.error_color))
            self.cur.execute("UPDATE prefixes SET prefix = '{}' WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере изменён на `{prefix}`.**', colour=config.success_color))
        else:
            self.cur.execute("INSERT INTO prefixes VALUES (?, ?)", (prefix, ctx.guild.id))
            self.db.commit()
            await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере установлен.\nТеперь мой префикс на этом сервере: `{prefix}`.**', colour=config.success_color))

    """
    @commands.slash_command(name='whitelist', description='Белый список')
    async def whitelist(self, ctx):
        """
            embed = disnake.Embed(
                title=':question: | Помощь',
                color=config.main_color
            )
            embed.add_field(name='Параметры команды whitelist', value=f'''>>> **/whitelist add `<@участник>` - `Добавить участника в белый список`
/whitelist remove `<@участник>` - `Убрать участника из белого списка`
/whitelist check [@участник] - `Посмотреть белый список/Проверить находится ли участник в белом списке`**''')
            await ctx.send(embed=embed)
        """
        pass

    @whitelist.sub_command(name='add', description='Добавить участника в белый список')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def add_wl(self, ctx, member: disnake.Member = None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули участника, которого хотите добавить в белый список**', color=config.error_color))
        if type(member) != disnake.Member:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянул не участника**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        if member == ctx.guild.me:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        if member.public_flags.verified_bot:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        embed=disnake.Embed(title=':gear: | Добавление Участника в белый список', description='>>> **Вы можете изменять разрешения участника нажимая на кнопки под сообщением**', color=config.main_color)
        def check_perm(action):
            return self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members'),
            'add_bots': check_perm('add_bots')
        }
        icons = {False: "`Запрещено` :no_entry:", True: "`Разрешено` :white_check_mark:"}
        emjs = {False: ":no_entry:", True: ":white_check_mark:"}
        colors = {False: ButtonStyle.red, True: ButtonStyle.green}
        async def remperm(action):
            if check_perm(action):
                self.cur.execute("DELETE FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action))
                self.db.commit()

        async def addperm(action):
            if not check_perm(action):
                self.cur.execute("INSERT INTO whitelist VALUES (?, ?, ?)", (ctx.guild.id, member.id, action))
                self.db.commit()
            
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}
Добавлять ботов: {icons[perms["add_bots"]]}**'''
        def buttons():
            buttons_list = [
                ActionRow(
                    Button(label='Удаление каналов', style=colors[perms['delete_channels']], custom_id='delete_channels', emoji=emjs[perms['delete_channels']]),
                    Button(label='Удаление ролей', style=colors[perms['delete_roles']], custom_id='delete_roles', emoji=emjs[perms['delete_roles']]),
                    Button(label='Создание каналов', style=colors[perms['create_channels']], custom_id='create_channels', emoji=emjs[perms['create_channels']]),
                    Button(label='Создание ролей', style=colors[perms['create_roles']], custom_id='create_roles', emoji=emjs[perms['create_roles']])
                ),
                ActionRow(
                    Button(label='Изменение каналов', style=colors[perms['update_channels']], custom_id='update_channels', emoji=emjs[perms['update_channels']]),
                    Button(label='Изменение ролей', style=colors[perms['update_roles']], custom_id='update_roles', emoji=emjs[perms['update_roles']]),
                    Button(label='Создание вебхуков', style=colors[perms['create_webhooks']], custom_id='create_webhooks', emoji=emjs[perms['create_webhooks']]),
                    Button(label='Изменение сервера', style=colors[perms['update_server']], custom_id='update_server', emoji=emjs[perms['update_server']])
                ),
                ActionRow(
                    Button(label='Бан участников', style=colors[perms['ban_members']], custom_id='ban_members', emoji=emjs[perms['ban_members']]),
                    Button(label='Кик участников', style=colors[perms['kick_members']], custom_id='kick_members', emoji=emjs[perms['kick_members']]),
                    Button(label='Добавлять ботов', style=colors[perms['add_bots']], custom_id='add_bots', emoji=emjs[perms['add_bots']])
                ),
                ActionRow(
                    Button(label='Отмена', style=ButtonStyle.grey, custom_id='cancel', emoji=emjs[False]),
                    Button(label='Готово', style=ButtonStyle.grey, custom_id='ready', emoji=emjs[True]),
                    Button(label='Разрешить все', style=ButtonStyle.grey, custom_id='all_perms', emoji=emjs[True]),
                    Button(label='Запретить все', style=ButtonStyle.grey, custom_id='rem_perms', emoji=emjs[False])
                )
            ]
            return buttons_list
        embed.add_field(name='Разрешения участника', value=check_perms())
        mess = await ctx.send(embed=embed, components=buttons())
        async def editmsg(inter):
            embed.clear_fields()
            embed.add_field(name = "Разрешения участника", value=check_perms())
            await inter.response.edit_message(embed=embed, components=buttons())
        next = 0
        while True:
            m = await ctx.original_message()
            inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
            #print(inter)
            if inter.component.custom_id == 'cancel':
                try: await inter.response.edit_message(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Добавление участника в белый список отменено**', color=config.error_color), components=[])
                except: pass
                #await mess.edit(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Добавление участника в белый список отменено**', color=config.error_color), components=[])
                break
            if inter.component.custom_id in list(perms):
                #try: await inter.respond(type=6)
                #except: pass
                perms[inter.component.custom_id] = not perms[inter.component.custom_id]
                await editmsg(inter)
            elif inter.component.custom_id == 'all_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = True
                await editmsg(inter)
            elif inter.component.custom_id == 'rem_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = False
                await editmsg(inter)
            elif inter.component.custom_id == 'ready':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    if perms[p]:
                        await addperm(p)
                    else:
                        await remperm(p)
                emb = disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Разрешения участника изменены**', color=config.success_color)
                emb.add_field(name='Разрешения участника', value=check_perms())
                await inter.response.edit_message(embed=emb, components=[])
                break

    @whitelist.sub_command(name='remove', description='Убрать участника из белого списка')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def remove_wl(self, ctx, member: disnake.Member = None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули участника, которого хотите убрать из белого списка**', color=config.error_color))
        if type(member) != disnake.Member:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не участника**', color=config.error_color))
        if self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участника нет в белом списке**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        if member == ctx.guild.me:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        if member.public_flags.verified_bot:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        self.cur.execute("DELETE FROM whitelist WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Участник удалён из белого списка**', color=config.success_color))

    @whitelist.sub_command(name='check', description='Посмотреть белый список')
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def check_wl(self, ctx, member: disnake.Member = None):
        if member != None:
            if type(member) != disnake.Member:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не участника**', color=config.error_color))
            if member.public_flags.verified_bot:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У участника есть все разрешения, т.к это верифицированный бот**', color=config.main_color))
            if member == ctx.guild.owner:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У участника еть все разрешения, т.к это владелец сервера**', color=config.main_color))
            if member == ctx.guild.me:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У меня есть все разрешения**', color=config.main_color))
            def check_perm(action):
                return self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action)).fetchone() != None
            perms = {
                'delete_channels': check_perm('delete_channels'),
                'delete_roles': check_perm('delete_roles'),
                'create_channels': check_perm('create_channels'),
                'create_roles': check_perm('create_roles'),
                'update_channels': check_perm('update_channels'),
                'update_roles': check_perm('update_roles'),
                'create_webhooks': check_perm('create_webhooks'),
                'update_server': check_perm('update_server'),
                'ban_members': check_perm('ban_members'),
                'kick_members': check_perm('kick_members'),
                'add_bots': check_perm('add_bots')
            }
            icons = {False: "`Запрещено` :no_entry:", True: "`Разрешено` :white_check_mark:"}
            def check_perms():
                return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}
Добавлять ботов: {icons[perms["add_bots"]]}**'''
            emb = disnake.Embed(title=':page_with_curl: | Белый список', color=config.main_color)
            emb.add_field(name='Разрешения участника', value=check_perms())
            await ctx.send(embed=emb)
        else:
            whitelisted_users = self.cur.execute("SELECT user_id FROM whitelist WHERE guild_id = {}".format(ctx.guild.id)).fetchall()
            wllist = []
            for usr in whitelisted_users:
                if not usr in wllist:
                    wllist.append(usr)
            if wllist == []:
                await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **Белый список обычных пользователей пуст**', color=config.main_color))
            else:
                lissst = ">>> **Участники в белом списке:**\n"
                for userwl in wllist:
                    lissst += f"<@{userwl[0]}>\n"
                await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description=lissst, color=config.main_color))

    @commands.slash_command(description='Анти-краш')
    async def anticrash(self, ctx):
        """
        embed = disnake.Embed(
            title=':question: | Помощь',
            color=config.main_color
        )
        embed.add_field(name='Параметры команды anticrash', value=f'''>>> **/anticrash enable - `Включить анти-краш режим`
/anticrash disable - `Отключить анти-краш режим`
/anticrash check - `Посмотреть запрещённые действия на сервере`**''')
        await ctx.send(embed=embed)
        """
        pass

    @commands.slash_command(description='Выбрать роль мута')
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def muterole(self, ctx: disnake.AppCmdInter, role: disnake.Role=None):
        if role == None:
            quarole = self.cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
            if quarole != None:
                if not ctx.guild.get_role(quarole[0]):
                    quarole = '`Роль выбрана, но её нет на сервере`'
                else:
                    quarole = ctx.guild.get_role(quarole[0]).mention
            else:
                quarole = '`Роль ещё не выбрана`'
            embed = disnake.Embed(
                title=":radio: | Мут",
                description=f">>> **Роль мута на данном сервере: {quarole}**",
                color=config.error_color
            )
            return await ctx.send(embed=embed)
        if not isinstance(role, disnake.Role):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы указали не роль**', color=config.error_color))
        if role.managed:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль принадлежит боту, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже моей, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.author.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже твоей**', color=config.error_color))
        embed = disnake.Embed(
            title=":radio: | Мут",
            description=f">>> **Роль {role.mention} помечена как роль мута**",
            color=config.error_color
        )
        await ctx.send(embed=embed)
        await role.edit(permissions=disnake.Permissions._from_value(0))
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, send_messages=False, add_reactions=False)
        #for channel in ctx.guild.voice_channels:
        #    await channel.set_permissions(role, connect=False)
        self.cur.execute("DELETE FROM muteroles WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        self.cur.execute("INSERT INTO muteroles VALUES (?, ?)", (ctx.guild.id, role.id))
        self.db.commit()

    @anticrash.sub_command(name='enable', description='Изменить запрещённые действия на сервере')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def enable_anticrash(self, ctx):
        embed=disnake.Embed(title=':gear: | Изменение запрещённых действий на сервере', description='>>> **Вы можете изменять запрещённые действия на сервере нажимая на кнопки под сообщением\nПодсказки:\nВключено - действие запрещено\nВыключено - действие разрешено**', color=config.main_color)
        def check_perm(action):
            return self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members')
        }
        icons = {False: "`Выключено` :no_entry:", True: "`Включено` :white_check_mark:"}
        emjs = {False: ":no_entry:", True: ":white_check_mark:"}
        colors = {False: ButtonStyle.red, True: ButtonStyle.green}
        async def remperm(action):
            if check_perm(action):
                self.cur.execute("DELETE FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action))
                self.db.commit()

        async def addperm(action):
            if not check_perm(action):
                self.cur.execute("INSERT INTO anticrash VALUES (?, ?)", (ctx.guild.id, action))
                self.db.commit()
            
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}**'''
        def buttons():
            buttons_list = [
                ActionRow(
                    Button(label='Удаление каналов', style=colors[perms['delete_channels']], custom_id='delete_channels', emoji=emjs[perms['delete_channels']]),
                    Button(label='Удаление ролей', style=colors[perms['delete_roles']], custom_id='delete_roles', emoji=emjs[perms['delete_roles']]),
                    Button(label='Создание каналов', style=colors[perms['create_channels']], custom_id='create_channels', emoji=emjs[perms['create_channels']]),
                    Button(label='Создание ролей', style=colors[perms['create_roles']], custom_id='create_roles', emoji=emjs[perms['create_roles']])
                ),
                ActionRow(
                    Button(label='Изменение каналов', style=colors[perms['update_channels']], custom_id='update_channels', emoji=emjs[perms['update_channels']]),
                    Button(label='Изменение ролей', style=colors[perms['update_roles']], custom_id='update_roles', emoji=emjs[perms['update_roles']]),
                    Button(label='Создание вебхуков', style=colors[perms['create_webhooks']], custom_id='create_webhooks', emoji=emjs[perms['create_webhooks']]),
                    Button(label='Изменение сервера', style=colors[perms['update_server']], custom_id='update_server', emoji=emjs[perms['update_server']])
                ),
                ActionRow(
                    Button(label='Бан участников', style=colors[perms['ban_members']], custom_id='ban_members', emoji=emjs[perms['ban_members']]),
                    Button(label='Кик участников', style=colors[perms['kick_members']], custom_id='kick_members', emoji=emjs[perms['kick_members']])
                ),
                ActionRow(
                    Button(label='Отмена', style=ButtonStyle.grey, custom_id='cancel', emoji=emjs[False]),
                    Button(label='Готово', style=ButtonStyle.grey, custom_id='ready', emoji=emjs[True]),
                    Button(label='Разрешить все', style=ButtonStyle.grey, custom_id='all_perms', emoji=emjs[True]),
                    Button(label='Запретить все', style=ButtonStyle.grey, custom_id='rem_perms', emoji=emjs[False])
                )
            ]
            return buttons_list
        embed.add_field(name='Запрещённые действия на сервере', value=check_perms())
        mess = await ctx.send(embed=embed, components=buttons())
        async def editmsg(inter):
            embed.clear_fields()
            embed.add_field(name = "Запрещённые действия на сервере", value=check_perms())
            await inter.response.edit_message(embed=embed, components=buttons())
        next = 0
        while True:
            m = await ctx.original_message()
            inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
            if inter.component.custom_id == 'cancel':
                #try: await inter.respond(type=6)
                #except: pass
                await inter.response.edit_message(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Изменение запрещённых действий на сервере отменено**', color=config.error_color), components=[])
                break
            if inter.component.custom_id in list(perms):
                #try: await inter.respond(type=6)
                #except: pass
                perms[inter.component.custom_id] = not perms[inter.component.custom_id]
                await editmsg(inter)
            elif inter.component.custom_id == 'all_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = False
                await editmsg(inter)
            elif inter.component.custom_id == 'rem_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = True
                await editmsg(inter)
            elif inter.component.custom_id == 'ready':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    if perms[p]:
                        await addperm(p)
                    else:
                        await remperm(p)
                emb = disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Запрещённые действия на сервере изменены**', color=config.success_color)
                emb.add_field(name='Запрещённые действия на сервере', value=check_perms())
                await inter.response.edit_message(embed=emb, components=[])
                break

    @anticrash.sub_command(name='disable', description='Выключить анти-краш режим')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def disable_anticrash(self, ctx):
        ch = self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-краш режим не включен на данном сервере**', color=config.error_color))
        self.cur.execute("DELETE FROM anticrash WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-краш режим выключён на данном сервере, теперь я не буду защищать этот сервер**', color=config.success_color))

    @anticrash.sub_command(name='check', description='Посмотреть запрещённые действия на сервере')
    async def checkac(self, ctx):
        def check_perm(action):
            return self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members')
        }
        icons = {False: "`Выключено` :no_entry:", True: "`Включено` :white_check_mark:"}
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}**'''
        emb = disnake.Embed(title=':shield:| Анти-краш', color=config.main_color)
        emb.add_field(name='Запрещённые действия на сервере', value=check_perms())
        await ctx.send(embed=emb)

    @commands.slash_command(description='Анти-бот')
    async def antibot(self, ctx):
        """
        embed = disnake.Embed(
            title=':question: | Помощь',
            color=config.main_color
        )
        embed.add_field(name='Параметры команды antibot', value=f'''>>> **/antibot enable - `включить анти-бот режим`
/antibot disable - `отключить анти-бот режим`**''')
        await ctx.send(embed=embed)
        """
        pass

    @antibot.sub_command(name='enable', description='Включить анти-бот')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def enable_antibot(self, ctx):
        ch = self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch != None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-бот режим уже включен на данном сервере**', color=config.error_color))
        self.cur.execute("INSERT INTO antibot VALUES ({})".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-бот режим включён на данном сервере, теперь я буду кикать не верифицированных ботов**', color=config.success_color))    

    @antibot.sub_command(name='disable', description='Выключить анти-бот')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def disable_antibot(self, ctx):
        ch = self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-бот режим не включен на данном сервере**', color=config.error_color))
        self.cur.execute("DELETE FROM antibot WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-бот режим выключён на данном сервере, теперь я не буду кикать не верифицированных ботов**', color=config.success_color))

    @commands.group(name='prefix', aliases=['p'])
    async def prefix(self, ctx):
        embed=disnake.Embed(title=':question: | Помощь', color=config.main_color)
        embed.add_field(
            name='Параметры команды prefix',
            value = f'''>>> **/prefix set <префикс> - `Установить префикс на этом сервере`
    /prefix reset - `Сбросить префикс на этом сервере`**'''
        )
        await ctx.send(embed=embed)

    @prefix.command(name="reset")
    @commands.cooldown(1, 120)
    @commands.check(adms.has_administrator)
    async def reset(self, ctx):
        self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        prefix = self.cur.fetchone()
        if prefix is None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не можете сбросить префикс на сервере, потому что он не был установлен ранее.**', color=config.error_color))
        self.cur.execute("DELETE FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере сброшен, теперь мой префикс на этом сервере - `{config.default_prefix[0]}`.**', color=config.success_color))

    @prefix.command(name="set", aliases=['s'])
    @commands.check(adms.has_administrator)
    async def set(self, ctx, prefix=None):
        if prefix == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не указали префикс, который хотите поставить на этом сервере.**', color=config.error_color))
        if prefix in config.default_prefix:
            return await self.reset_prefix(ctx)
        self.cur.execute("SELECT prefix FROM prefixes WHERE guild_id = {}".format(ctx.guild.id))
        old_prefix = self.cur.fetchone()
        if old_prefix:
            if old_prefix[0] == prefix:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Указанный префикс уже выбран.**', color=config.error_color))
            self.cur.execute("UPDATE prefixes SET prefix = '{}' WHERE guild_id = {}".format(ctx.guild.id))
            self.db.commit()
            await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере изменён на `{prefix}`.**', color=config.success_color))
        else:
            self.cur.execute("INSERT INTO prefixes VALUES (?, ?)", (prefix, ctx.guild.id))
            self.db.commit()
            await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **Префикс на этом сервере установлен.\nТеперь мой префикс на этом сервере: `{prefix}`.**', color=config.success_color))

    @commands.group(name='whitelist')
    async def whitelist(self, ctx):
        embed = disnake.Embed(
            title=':question: | Помощь',
            color=config.main_color
        )
        embed.add_field(name='Параметры команды whitelist', value=f'''>>> **/whitelist add `<@участник>` - `Добавить участника в белый список`
    /whitelist remove `<@участник>` - `Убрать участника из белого списка`
    /whitelist check [@участник] - `Посмотреть белый список/Проверить находится ли участник в белом списке`**''')
        await ctx.send(embed=embed)

    @whitelist.command(name='add')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def add(self, ctx, member: disnake.Member = None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули участника, которого хотите добавить в белый список**', color=config.error_color))
        if type(member) != disnake.Member:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянул не участника**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        if member == ctx.guild.me:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        if member.public_flags.verified_bot:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участник уже в белом списке**', color=config.error_color))
        embed=disnake.Embed(title=':gear: | Добавление Участника в белый список', description='>>> **Вы можете изменять разрешения участника нажимая на кнопки под сообщением**', color=config.main_color)
        def check_perm(action):
            return self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members'),
            'add_bots': check_perm('add_bots')
        }
        icons = {False: "`Запрещено` :no_entry:", True: "`Разрешено` :white_check_mark:"}
        emjs = {False: ":no_entry:", True: ":white_check_mark:"}
        colors = {False: ButtonStyle.red, True: ButtonStyle.green}
        async def remperm(action):
            if check_perm(action):
                self.cur.execute("DELETE FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action))
                self.db.commit()

        async def addperm(action):
            if not check_perm(action):
                self.cur.execute("INSERT INTO whitelist VALUES (?, ?, ?)", (ctx.guild.id, member.id, action))
                self.db.commit()
                
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
    Удаление ролей: {icons[perms["delete_roles"]]}
    Создание каналов: {icons[perms["create_channels"]]}
    Создание ролей: {icons[perms["create_roles"]]}
    Изменение каналов: {icons[perms["update_channels"]]}
    Изменение ролей: {icons[perms["update_roles"]]}
    Создание вебхуков: {icons[perms["create_webhooks"]]}
    Изменение сервера: {icons[perms["update_server"]]}
    Бан участников: {icons[perms["ban_members"]]}
    Кик участников: {icons[perms["kick_members"]]}
    Добавлять ботов: {icons[perms["add_bots"]]}**'''
        def buttons():
            buttons_list = [
                ActionRow(
                    Button(label='Удаление каналов', style=colors[perms['delete_channels']], custom_id='delete_channels', emoji=emjs[perms['delete_channels']]),
                    Button(label='Удаление ролей', style=colors[perms['delete_roles']], custom_id='delete_roles', emoji=emjs[perms['delete_roles']]),
                    Button(label='Создание каналов', style=colors[perms['create_channels']], custom_id='create_channels', emoji=emjs[perms['create_channels']]),
                    Button(label='Создание ролей', style=colors[perms['create_roles']], custom_id='create_roles', emoji=emjs[perms['create_roles']])
                ),
                ActionRow(
                    Button(label='Изменение каналов', style=colors[perms['update_channels']], custom_id='update_channels', emoji=emjs[perms['update_channels']]),
                    Button(label='Изменение ролей', style=colors[perms['update_roles']], custom_id='update_roles', emoji=emjs[perms['update_roles']]),
                    Button(label='Создание вебхуков', style=colors[perms['create_webhooks']], custom_id='create_webhooks', emoji=emjs[perms['create_webhooks']]),
                    Button(label='Изменение сервера', style=colors[perms['update_server']], custom_id='update_server', emoji=emjs[perms['update_server']])
                ),
                ActionRow(
                    Button(label='Бан участников', style=colors[perms['ban_members']], custom_id='ban_members', emoji=emjs[perms['ban_members']]),
                    Button(label='Кик участников', style=colors[perms['kick_members']], custom_id='kick_members', emoji=emjs[perms['kick_members']]),
                    Button(label='Добавлять ботов', style=colors[perms['add_bots']], custom_id='add_bots', emoji=emjs[perms['add_bots']])
                ),
                ActionRow(
                    Button(label='Отмена', style=ButtonStyle.grey, custom_id='cancel', emoji=emjs[False]),
                    Button(label='Готово', style=ButtonStyle.grey, custom_id='ready', emoji=emjs[True]),
                    Button(label='Разрешить все', style=ButtonStyle.grey, custom_id='all_perms', emoji=emjs[True]),
                    Button(label='Запретить все', style=ButtonStyle.grey, custom_id='rem_perms', emoji=emjs[False])
                )
            ]
            return buttons_list
        embed.add_field(name='Разрешения участника', value=check_perms())
        mess = await ctx.send(embed=embed, components=buttons())
        async def editmsg(inter):
            embed.clear_fields()
            embed.add_field(name = "Разрешения участника", value=check_perms())
            await inter.response.edit_message(embed=embed, components=buttons())
        next = 0
        while True:
            m = await ctx.original_message()
            inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
            #print(inter)
            if inter.component.custom_id == 'cancel':
                try:
                    await inter.response.edit_message(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Добавление участника в белый список отменено**', color=config.error_color), components=[])
                except:
                    pass
                #await mess.edit(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Добавление участника в белый список отменено**', color=config.error_color), components=[])
                break
            if inter.component.custom_id in list(perms):
                #try: await inter.respond(type=6)
                #except: pass
                perms[inter.component.custom_id] = not perms[inter.component.custom_id]
                await editmsg(inter)
            elif inter.component.custom_id == 'all_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = True
                await editmsg(inter)
            elif inter.component.custom_id == 'rem_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = False
                await editmsg(inter)
            elif inter.component.custom_id == 'ready':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    if perms[p]:
                        await addperm(p)
                    else:
                        await remperm(p)
                emb = disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Разрешения участника изменены**', color=config.success_color)
                emb.add_field(name='Разрешения участника', value=check_perms())
                await inter.response.edit_message(embed=emb, components=[])
                break

    @whitelist.command(name='remove')
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def remove(self, ctx, member: disnake.Member = None):
        if member == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы не упомянули участника, которого хотите убрать из белого списка**', color=config.error_color))
        if type(member) != disnake.Member:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не участника**', color=config.error_color))
        if self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id)).fetchone() == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Участника нет в белом списке**', color=config.error_color))
        if member == ctx.guild.owner:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        if member == ctx.guild.me:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        if member.public_flags.verified_bot:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Невозможно убрать участника из белого списка**', color=config.error_color))
        self.cur.execute("DELETE FROM whitelist WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Участник удалён из белого списка**', color=config.success_color))

    @whitelist.command(name='check')
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def check(self, ctx, member: disnake.Member = None):
        if member != None:
            if type(member) != disnake.Member:
                return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы упомянули не участника**', color=config.error_color))
            if member.public_flags.verified_bot:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У участника есть все разрешения, т.к это верифицированный бот**', color=config.main_color))
            if member == ctx.guild.owner:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У участника еть все разрешения, т.к это владелец сервера**', color=config.main_color))
            if member == ctx.guild.me:
                return await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **У меня есть все разрешения**', color=config.main_color))
            def check_perm(action):
                return self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(ctx.guild.id, member.id, action)).fetchone() != None
            perms = {
                'delete_channels': check_perm('delete_channels'),
                'delete_roles': check_perm('delete_roles'),
                'create_channels': check_perm('create_channels'),
                'create_roles': check_perm('create_roles'),
                'update_channels': check_perm('update_channels'),
                'update_roles': check_perm('update_roles'),
                'create_webhooks': check_perm('create_webhooks'),
                'update_server': check_perm('update_server'),
                'ban_members': check_perm('ban_members'),
                'kick_members': check_perm('kick_members'),
                'add_bots': check_perm('add_bots')
            }
            icons = {False: "`Запрещено` :no_entry:", True: "`Разрешено` :white_check_mark:"}
            def check_perms():
                return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
    Удаление ролей: {icons[perms["delete_roles"]]}
    Создание каналов: {icons[perms["create_channels"]]}
    Создание ролей: {icons[perms["create_roles"]]}
    Изменение каналов: {icons[perms["update_channels"]]}
    Изменение ролей: {icons[perms["update_roles"]]}
    Создание вебхуков: {icons[perms["create_webhooks"]]}
    Изменение сервера: {icons[perms["update_server"]]}
    Бан участников: {icons[perms["ban_members"]]}
    Кик участников: {icons[perms["kick_members"]]}
    Добавлять ботов: {icons[perms["add_bots"]]}**'''
            emb = disnake.Embed(title=':page_with_curl: | Белый список', color=config.main_color)
            emb.add_field(name='Разрешения участника', value=check_perms())
            await ctx.send(embed=emb)
        else:
            whitelisted_users = self.cur.execute("SELECT user_id FROM whitelist WHERE guild_id = {}".format(ctx.guild.id)).fetchall()
            wllist = []
            for usr in whitelisted_users:
                if not usr in wllist:
                    wllist.append(usr)
            if wllist == []:
                await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description='>>> **Белый список обычных пользователей пуст**', color=config.main_color))
            else:
                lissst = ">>> **Участники в белом списке:**\n"
                for userwl in wllist:
                    lissst += f"<@{userwl[0]}>\n"
                await ctx.send(embed=disnake.Embed(title=':page_with_curl: | Белый список', description=lissst, color=config.main_color))

    @commands.group(invoke_without_command=True, name='anticrash')
    async def anticrash(self, ctx):
        embed = disnake.Embed(
            title=':question: | Помощь',
            color=config.main_color
            )
        embed.add_field(name='Параметры команды anticrash', value=f'''>>> **/anticrash enable - `Включить анти-краш режим`
    /anticrash disable - `Отключить анти-краш режим`
    /anticrash check - `Посмотреть запрещённые действия на сервере`**''')
        await ctx.send(embed=embed)

    @commands.command(aliases=['mr', 'rmute'])
    @commands.check(adms.has_administrator)
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def muterole(self, ctx, role: disnake.Role=None):
        if role == None:
            quarole = self.cur.execute("SELECT role_id FROM muteroles WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
            if quarole != None:
                if not ctx.guild.get_role(quarole[0]):
                    quarole = '`Роль выбрана, но её нет на сервере`'
                else:
                    quarole = ctx.guild.get_role(quarole[0]).mention
            else:
                quarole = '`Роль ещё не выбрана`'
                embed = disnake.Embed(
                    title=":radio: | Мут",
                    description=f">>> **Роль мута на данном сервере: {quarole}**",
                    color=config.error_color
                )
                return await ctx.send(embed=embed)
        if not isinstance(role, disnake.Role):
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Вы указали не роль**', color=config.error_color))
        if role.managed:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль принадлежит боту, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.guild.me.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже моей, я не смогу её выдать**', color=config.error_color))
        if role.position >= ctx.author.top_role.position:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Роль не ниже твоей**', color=config.error_color))
        embed = disnake.Embed(
            title=":radio: | Мут",
            description=f">>> **Роль {role.mention} помечена как роль мута**",
            color=config.error_color
        )
        await ctx.send(embed=embed)
        await role.edit(permissions=disnake.Permissions._from_value(0))
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, send_messages=False, add_reactions=False)
        for channel in ctx.guild.voice_channels:
            await channel.set_permissions(role, connect=False, speak=False, send_messages=False, add_reactions=False)
        for channel in ctx.guild.stage_channels:
            await channel.set_permissions(role, send_messages=False, speak=False, connect=False)
        self.cur.execute("DELETE FROM muteroles WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        self.cur.execute("INSERT INTO muteroles VALUES (?, ?)", (ctx.guild.id, role.id))
        self.db.commit()

    @anticrash.command(name='enable')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def enable(self, ctx):
        embed=disnake.Embed(title=':gear: | Изменение запрещённых действий на сервере', description='>>> **Вы можете изменять запрещённые действия на сервере нажимая на кнопки под сообщением\nПодсказки:\nВключено - действие запрещено\nВыключено - действие разрешено**', color=config.main_color)
        def check_perm(action):
            return self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members')
        }
        icons = {False: "`Выключено` :x:", True: "`Включено` :white_check_mark:"}
        emjs = {False: ":x:", True: ":white_check_mark:"}
        colors = {False: ButtonStyle.red, True: ButtonStyle.green}
        async def remperm(action):
            if check_perm(action):
                self.cur.execute("DELETE FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action))
                self.db.commit()

        async def addperm(action):
            if not check_perm(action):
                self.cur.execute("INSERT INTO anticrash VALUES (?, ?)", (ctx.guild.id, action))
                self.db.commit()
            
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}**'''
        def buttons():
            buttons_list = [
                ActionRow(
                    Button(label='Удаление каналов', style=colors[perms['delete_channels']], custom_id='delete_channels', emoji=emjs[perms['delete_channels']]),
                    Button(label='Удаление ролей', style=colors[perms['delete_roles']], custom_id='delete_roles', emoji=emjs[perms['delete_roles']]),
                    Button(label='Создание каналов', style=colors[perms['create_channels']], custom_id='create_channels', emoji=emjs[perms['create_channels']]),
                    Button(label='Создание ролей', style=colors[perms['create_roles']], custom_id='create_roles', emoji=emjs[perms['create_roles']])
                ),
                ActionRow(
                    Button(label='Изменение каналов', style=colors[perms['update_channels']], custom_id='update_channels', emoji=emjs[perms['update_channels']]),
                    Button(label='Изменение ролей', style=colors[perms['update_roles']], custom_id='update_roles', emoji=emjs[perms['update_roles']]),
                    Button(label='Создание вебхуков', style=colors[perms['create_webhooks']], custom_id='create_webhooks', emoji=emjs[perms['create_webhooks']]),
                    Button(label='Изменение сервера', style=colors[perms['update_server']], custom_id='update_server', emoji=emjs[perms['update_server']])
                ),
                ActionRow(
                    Button(label='Бан участников', style=colors[perms['ban_members']], custom_id='ban_members', emoji=emjs[perms['ban_members']]),
                    Button(label='Кик участников', style=colors[perms['kick_members']], custom_id='kick_members', emoji=emjs[perms['kick_members']])
                ),
                ActionRow(
                    Button(label='Отмена', style=ButtonStyle.grey, custom_id='cancel', emoji=emjs[False]),
                    Button(label='Готово', style=ButtonStyle.grey, custom_id='ready', emoji=emjs[True]),
                    Button(label='Разрешить все', style=ButtonStyle.grey, custom_id='all_perms', emoji=emjs[True]),
                    Button(label='Запретить все', style=ButtonStyle.grey, custom_id='rem_perms', emoji=emjs[False])
                )
            ]
            return buttons_list
        embed.add_field(name='Запрещённые действия на сервере', value=check_perms())
        mess = await ctx.send(embed=embed, components=buttons())
        async def editmsg(inter):
            embed.clear_fields()
            embed.add_field(name = "Запрещённые действия на сервере", value=check_perms())
            await inter.response.edit_message(embed=embed, components=buttons())
        next = 0
        while True:
            m = await ctx.original_message()
            inter = await self.bot.wait_for('button_click', check=lambda i: i.author == ctx.author and i.message.id == m.id)
            if inter.component.custom_id == 'cancel':
                #try: await inter.respond(type=6)
                #except: pass
                await inter.response.edit_message(embed=disnake.Embed(title=':x: | Отмена', description='>>> **Изменение запрещённых действий на сервере отменено**', color=config.error_color), components=[])
                break
            if inter.component.custom_id in list(perms):
                #try: await inter.respond(type=6)
                #except: pass
                perms[inter.component.custom_id] = not perms[inter.component.custom_id]
                await editmsg(inter)
            elif inter.component.custom_id == 'all_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = False
                await editmsg(inter)
            elif inter.component.custom_id == 'rem_perms':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    perms[p] = True
                await editmsg(inter)
            elif inter.component.custom_id == 'ready':
                #try: await inter.respond(type=6)
                #except: pass
                for p in list(perms):
                    if perms[p]:
                        await addperm(p)
                    else:
                        await remperm(p)
                emb = disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Запрещённые действия на сервере изменены**', color=config.success_color)
                emb.add_field(name='Запрещённые действия на сервере', value=check_perms())
                await inter.response.edit_message(embed=emb, components=[])
                break

    @anticrash.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def disable(self, ctx):
        ch = self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-краш режим не включен на данном сервере**', color=config.error_color))
        self.cur.execute("DELETE FROM anticrash WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-краш режим выключён на данном сервере, теперь я не буду защищать этот сервер**', color=config.success_color))

    @anticrash.command(name='check')
    async def check(self, ctx):
        def check_perm(action):
            return self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {} AND action = '{}'".format(ctx.guild.id, action)).fetchone() != None
        perms = {
            'delete_channels': check_perm('delete_channels'),
            'delete_roles': check_perm('delete_roles'),
            'create_channels': check_perm('create_channels'),
            'create_roles': check_perm('create_roles'),
            'update_channels': check_perm('update_channels'),
            'update_roles': check_perm('update_roles'),
            'create_webhooks': check_perm('create_webhooks'),
            'update_server': check_perm('update_server'),
            'ban_members': check_perm('ban_members'),
            'kick_members': check_perm('kick_members')
        }
        icons = {False: "`Выключено` :no_entry:", True: "`Включено` :white_check_mark:"}
        def check_perms():
            return f'''>>> **Удаление каналов: {icons[perms["delete_channels"]]}
Удаление ролей: {icons[perms["delete_roles"]]}
Создание каналов: {icons[perms["create_channels"]]}
Создание ролей: {icons[perms["create_roles"]]}
Изменение каналов: {icons[perms["update_channels"]]}
Изменение ролей: {icons[perms["update_roles"]]}
Создание вебхуков: {icons[perms["create_webhooks"]]}
Изменение сервера: {icons[perms["update_server"]]}
Бан участников: {icons[perms["ban_members"]]}
Кик участников: {icons[perms["kick_members"]]}**'''
        emb = disnake.Embed(title=':shield:| Анти-краш', color=config.main_color)
        emb.add_field(name='Запрещённые действия на сервере', value=check_perms())
        await ctx.send(embed=emb)

    @commands.group()
    async def antibot(self, ctx):
        embed = disnake.Embed(
            title=':question: | Помощь',
            color=config.main_color
        )
        embed.add_field(name='Параметры команды antibot', value=f'''>>> **/antibot enable - `включить анти-бот режим`
/antibot disable - `отключить анти-бот режим`**''')
        await ctx.send(embed=embed)

    @antibot.command(name='enable')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def enable_antibot(self, ctx):
        ch = self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch != None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-бот режим уже включен на данном сервере**', color=config.error_color))
        self.cur.execute("INSERT INTO antibot VALUES ({})".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-бот режим включён на данном сервере, теперь я буду кикать не верифицированных ботов**', color=config.success_color))    

    @antibot.command(name='disable')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.check(adms.only_owner)
    async def disable(self, ctx):
        ch = self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(ctx.guild.id)).fetchone()
        if ch == None:
            return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description='>>> **Анти-бот режим не включен на данном сервере**', color=config.error_color))
        self.cur.execute("DELETE FROM antibot WHERE guild_id = {}".format(ctx.guild.id))
        self.db.commit()
        await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description='>>> **Анти-бот режим выключён на данном сервере, теперь я не буду кикать не верифицированных ботов**', color=config.success_color))


def setup(bot):
    bot.add_cog(Settings(bot))