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

init()

import database
import config


class Anticrash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

    async def checkwl(self, guild, euser, action):
        if euser == guild.owner:
            return True
        if euser == guild.me:
            return True
        if euser.public_flags.verified_bot:
            return True
        if euser in config.default_wl:
            return True
        if self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(guild.id, euser.id, action)).fetchone() != None:
            print(self.cur.execute("SELECT * FROM whitelist WHERE guild_id = {} AND user_id = {} AND action = '{}'".format(guild.id, euser.id, action)).fetchone())
            return True
        return False

    async def checkac(self, guild, action):
        if self.cur.execute("SELECT * FROM anticrash WHERE guild_id = {} AND action = '{}'".format(guild.id, action)).fetchone() != None:
            return True
        return False

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if await self.checkac(channel.guild, 'delete_channels') == True:
            async for entry in channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete):
                if await self.checkwl(channel.guild, entry.user, 'delete_channels') == False:
                    try:
                        await entry.user.ban(reason='Anti Channel Delete')
                    except:
                        pass
                    if isinstance(channel, disnake.TextChannel):
                        if channel.category == None:
                            try:
                                await channel.guild.create_text_channel(
                                    name=channel.name,
                                    topic=channel.topic,
                                    position=channel.position,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    overwrites=channel.overwrites
                                    )
                            except:
                                pass
                        else:
                            try:
                                await channel.guild.create_text_channel(
                                    name=channel.name,
                                    topic=channel.topic,
                                    position=channel.position,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    overwrites=channel.overwrites,
                                    category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                    )
                            except:
                                pass
                    if isinstance(channel, disnake.VoiceChannel):
                        if channel.category == None:
                            try:
                                await channel.guild.create_voice_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    rtc_region=channel.rtc_region,
                                    video_quality_mode=channel.video_quality_mode
                                    )
                            except:
                                pass
                        else:
                            try:
                                await channel.guild.create_voice_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    slowmode_delay=channel.slowmode_delay,
                                    user_limit=channel.user_limit,
                                    bitrate=channel.bitrate,
                                    rtc_region=channel.rtc_region,
                                    video_quality_mode=channel.video_quality_mode,
                                    category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                    )
                            except:
                                pass
                    if isinstance(channel, disnake.CategoryChannel):
                        try:
                            await channel.guild.create_category(
                                name=channel.name,
                                position=channel.position,
                                overwrites=channel.overwrites
                                )
                        except:
                            pass
                    if isinstance(channel, disnake.StageChannel):
                        if channel.category == None:
                            try:
                                await channel.guild.create_stage_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    topic=channel.topic,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    rtc_region=channel.rtc_region,
                                    video_quality_mode=channel.video_quality_mode,
                                    slowmode_delay=channel.slowmode_delay,
                                    requesting_to_speak=channel.requesting_to_speak,
                                    )
                            except:
                                pass
                        else:
                            try:
                                await channel.guild.create_stage_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    topic=channel.topic,
                                    bitrate=channel.bitrate,
                                    user_limit=channel.user_limit,
                                    rtc_region=channel.rtc_region,
                                    video_quality_mode=channel.video_quality_mode,
                                    slowmode_delay=channel.slowmode_delay,
                                    requesting_to_speak=channel.requesting_to_speak,
                                    category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                    )
                            except:
                                pass
                    if isinstance(channel, disnake.ForumChannel):
                        if channel.category == None:
                            try:
                                await channel.guild.create_forum_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    topic=channel.topic,
                                    default_auto_archive_duration=channel.default_auto_archive_duration,
                                    slowmode_delay=channel.slowmode_delay,
                                    default_thread_slowmode_delay=channel.default_thread_slowmode_delay,
                                    default_sort_order=channel.default_sort_order,
                                    default_layout=channel.default_layout,
                                    default_reaction=channel.default_reaction,
                                    available_tags=channel.available_tags,
                                    requires_tag=self.flags.require_tag,
                                    permissions_for=channel.permissions_for
                                    )
                            except:
                                pass
                        else:
                            try:
                                await channel.guild.create_forum_channel(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites,
                                    nsfw=channel.nsfw,
                                    topic=channel.topic,
                                    default_auto_archive_duration=channel.default_auto_archive_duration,
                                    slowmode_delay=channel.slowmode_delay,
                                    default_thread_slowmode_delay=channel.default_thread_slowmode_delay,
                                    default_sort_order=channel.default_sort_order,
                                    default_layout=channel.default_layout,
                                    default_reaction=channel.default_reaction,
                                    available_tags=channel.available_tags,
                                    requires_tag=self.flags.require_tag,
                                    permissions_for=channel.permissions_for,
                                    category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                    )
                            except:
                                pass
                            

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        if await self.checkac(role.guild, 'delete_roles') == True and not role.managed:
            async for entry in role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete):
                if await self.checkwl(role.guild, entry.user, 'delete_roles') == False:
                    try:
                        await entry.user.ban(reason='Anti Role Delete')
                    except:
                        pass
                    try: 
                        rolee2 = await role.guild.create_role(
                            name=role.name,
                            color=role.color,
                            hoist=role.hoist,
                            mentionable=role.mentionable,
                            permissions=role.permissions,
                            icon=role.icon
                            )
                        await rolee2.edit(position=role.position)
                    except:
                        pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        if await self.checkac(after, 'update_server') == True:
            if after.name != before.name:
                async for entry in after.audit_logs(limit=1, action=disnake.AuditLogAction.guild_update):
                    if await self.checkwl(after, entry.user, 'update_server') == False:
                        try:
                            await entry.user.ban(reason='Anti Guild Update | Name Update')
                        except:
                            pass
                        try:
                            await after.edit(name=before.name)
                        except:
                            pass
            if after.icon  != before.icon:
                async for entry in after.audit_logs(limit=1, action=disnake.AuditLogAction.guild_update):
                    if await self.checkwl(after, entry.user, 'update_server') == False:
                        try:
                            await entry.user.ban(reason='Anti Guild Update | Icon Update')
                        except:
                            pass
                        try:
                            await after.edit(icon=before.icon)
                        except:
                            pass
                
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if await self.checkac(channel.guild, 'create_channels') == True:
            async for entry in channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create):
                if await self.checkwl(channel.guild, entry.user, 'create_channels') == False:
                    try:
                        await entry.user.ban(reason='Anti Channel Create')
                    except:
                        pass
                    try:
                        await channel.delete()
                    except:
                        pass
        
    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        if await self.checkac(role.guild, 'create_roles') == True and not role.managed:
            async for entry in role.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_create):
                if await self.checkwl(role.guild, entry.user, 'create_roles') == False:
                    try:
                        await entry.user.ban(reason='Anti Role Create')
                    except:
                        pass
                    try:
                        await role.delete()
                    except:
                        pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild = member.guild
        async for entry in guild.audit_logs(limit=1):
            if entry.action == disnake.AuditLogAction.kick:
                if await self.checkac(guild, 'kick_members') == True:
                    if await self.checkwl(guild, entry.user, 'kick_membes') == False:
                        try:
                            await entry.user.ban(reason='Anti Member Kick')
                        except:
                            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        guild.name = ctx.guild.name
        if await self.checkac(guild, 'ban_members') == True:
            async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.ban):
                if await self.checkwl(guild, entry.user, 'ban_members') == False:
                    try:
                        await entry.user.ban(reason='Anti Member Ban')
                    except:
                        pass
                    try:
                        await member.unban()
                    except:
                        pass
                    inv = await guild.channels[0].create_invite()
                    try:
                        embed = disnake.Embed(
                            title="Анти-краш система",
                            color=disnake.Color.red(),
                            description=f"Вы были забанены на сервере {ctx.guild.name} пользователем <@{entry.user.id}>.\nЯ предотвратил эти действия и разбанил вас."),
                        embed.add_field(
                            name=':link: Ссылка на сервер',
                            value=f'''>>> {inv}''')
                        await ctx.member.send(embed=embed)
                    except:
                        pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if await self.checkac(after.guild, 'update_channels') == True:
            if after.name != before.name:
                async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_update):
                    if await self.checkwl(after.guild, entry.user, 'update_channels') == False:
                        try:
                            await entry.user.ban(reason='Anti Channel Update')
                        except:
                            pass
                        if isinstance(after, disnake.TextChannel):
                            if channel.category == None:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        topic=channel.topic,
                                        position=channel.position,
                                        nsfw=channel.nsfw,
                                        slowmode_delay=channel.slowmode_delay,
                                        overwrites=channel.overwrites,
                                    )
                                except:
                                    pass
                            else:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        topic=channel.topic,
                                        position=channel.position,
                                        nsfw=channel.nsfw,
                                        slowmode_delay=channel.slowmode_delay,
                                        overwrites=channel.overwrites,
                                        category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                        )
                                except:
                                    pass
                        if isinstance(after, disnake.VoiceChannel):
                            if channel.category == None:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        slowmode_delay=channel.slowmode_delay,
                                        user_limit=channel.user_limit,
                                        bitrate=channel.bitrate,
                                        rtc_region=channel.rtc_region,
                                        video_quality_mode=channel.video_quality_mode,
                                        )
                                except:
                                    pass
                            else:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        slowmode_delay=channel.slowmode_delay,
                                        user_limit=channel.user_limit,
                                        bitrate=channel.bitrate,
                                        rtc_region=channel.rtc_region,
                                        video_quality_mode=channel.video_quality_mode,
                                        category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                        )
                                except:
                                    pass
                        if isinstance(after, disnake.CategoryChannel):
                            try:
                                await after.edit(
                                    name=channel.name,
                                    position=channel.position,
                                    overwrites=channel.overwrites
                                    )
                            except:
                                pass
                        if isinstance(after, disnake.StageChannel):
                            if channel.category == None:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        topic=channel.topic,
                                        bitrate=channel.bitrate,
                                        user_limit=channel.user_limit,
                                        rtc_region=channel.rtc_region,
                                        video_quality_mode=channel.video_quality_mode,
                                        slowmode_delay=channel.slowmode_delay,
                                        requesting_to_speak=channel.requesting_to_speak,
                                        )
                                except:
                                    pass
                            else:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        topic=channel.topic,
                                        bitrate=channel.bitrate,
                                        user_limit=channel.user_limit,
                                        rtc_region=channel.rtc_region,
                                        video_quality_mode=channel.video_quality_mode,
                                        slowmode_delay=channel.slowmode_delay,
                                        requesting_to_speak=channel.requesting_to_speak,
                                        category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                        )
                                except:
                                    pass
                        if isinstance(after, disnake.ForumChannel):
                            if channel.category == None:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        topic=channel.topic,
                                        default_auto_archive_duration=channel.default_auto_archive_duration,
                                        slowmode_delay=channel.slowmode_delay,
                                        default_thread_slowmode_delay=channel.default_thread_slowmode_delay,
                                        default_sort_order=channel.default_sort_order,
                                        default_layout=channel.default_layout,
                                        default_reaction=channel.default_reaction,
                                        available_tags=channel.available_tags,
                                        requires_tag=self.flags.require_tag,
                                        )
                                except:
                                    pass
                            else:
                                try:
                                    await after.edit(
                                        name=channel.name,
                                        position=channel.position,
                                        overwrites=channel.overwrites,
                                        nsfw=channel.nsfw,
                                        topic=channel.topic,
                                        default_auto_archive_duration=channel.default_auto_archive_duration,
                                        slowmode_delay=channel.slowmode_delay,
                                        default_thread_slowmode_delay=channel.default_thread_slowmode_delay,
                                        default_sort_order=channel.default_sort_order,
                                        default_layout=channel.default_layout,
                                        default_reaction=channel.default_reaction,
                                        available_tags=channel.available_tags,
                                        requires_tag=self.flags.require_tag,
                                        category=disnake.utils.get(channel.guild.categories, name=channel.category.name)
                                        )
                                except:
                                    pass
                                            
    
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if await self.checkac(after.guild, 'update_roles') == True and not role.managed:
            if after.name != before.name or after.icon != before.icon or after.permissions != before.permissions or after.position != before.position or after.color != before.color or after.hoist != before.hoist or after.mentionable != before.mentionable:
                async for entry in after.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update):
                    if await self.checkwl(after.guild, entry.user, 'update_roles') == False:
                        try:
                            await entry.user.ban(reason='Anti Role Update')
                        except:
                            pass
                        try:
                            await after.edit(
                                name=before.name,
                                color=before.color,
                                position=before.position,
                                hoist=before.hoist,
                                mentionable=before.mentionable,
                                permissions=before.permissions,
                                icon=before.icon
                                )
                        except:
                            pass

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        if await self.checkac(channel.guild, 'create_webhooks') == True:
            async for entry in channel.guild.audit_logs(limit=1, action=disnake.AuditLogAction.webhook_create):
                if await self.checkwl(channel.guild, entry.user, 'create_webhooks') == False:
                    try:
                        await entry.user.ban(reason='Anti Webhook Create')
                    except:
                        pass
                    for webhook in await channel.webhooks():
                        if webhook.id == entry.target.id:
                            try:
                                await webhook.delete()
                            except:
                                pass
                        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id
        if self.cur.execute("SELECT * FROM antibot WHERE guild_id = {}".format(member.guild.id)).fetchone() != None:
            if member.bot and member != member.guild.me:
                if member.public_flags.verified_bot:
                    pass
                else:
                    async for entry in member.guild.audit_logs(limit=1, action=disnake.AuditLogAction.bot_add):
                        if await self.checkwl(member.guild, entry.user, 'add_bots') == False:
                            try:
                                await entry.user.ban(reason='Anti Bot Add')
                            except:
                                pass
                            try:
                                await member.ban(reason='Anti Bot')
                            except:
                                pass
                            
                            
    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.cur.execute("SELECT * FROM hardbot WHERE guild_id = {}".format(member.guild.id)).fetchone() != None:
            if member.bot and member != member.guild.me:
                async for entry in member.guild.audit_logs(limit=1, action=disnake.AuditLogAction.bot_add):
                    if entry.user == guild.owner or entry.user in config.default_wl or guild.me:
                        pass
                    else:
                        try:
                            await entry.user.ban(reason='Anti Hard Bot Add')
                        except:
                            pass
                        try:
                            await member.ban(reason='Anti Hard Bot')
                            await role.delete(role=member.role)
                        except:
                            pass
                            

def setup(bot):
    bot.add_cog(Anticrash(bot))