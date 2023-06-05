import disnake
from disnake.ext import commands

async def owner_only(ctx):
    if not ctx.author == ctx.guild.owner:
        return await ctx.send(embed=disnake.Embed(title='❌ | Ошибка..', description='>>> **Вы не владелец сервера**', color=config.error_color))
    return True

class MissingPerms(commands.CheckFailure):
    pass

class NotOwner(commands.CheckFailure):
    pass

class NotDeveloper(commands.CheckFailure):
    pass

class Err(commands.CheckFailure):
    pass

async def only_owner(ctx):
    if ctx.author == ctx.guild.owner:
        return True
    else:
        raise NotOwner()

async def has_ban_members(ctx):
    if ctx.author.guild_permissions.ban_members or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Банить участников')

async def has_kick_members(ctx):
    if ctx.author.guild_permissions.kick_members or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Выгонять участников')

async def has_mute_members(ctx: disnake.AppCmdInter):
    if ctx.author.guild_permissions.mute_members or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Мутить участников')

async def has_administrator(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Администратор')

async def has_developer(ctx):
    if ctx.author.id in config.developers:
        return True
    else:
        raise NotDeveloper()

async def check_admin(ctx):
    roles = [r for r in ctx.guild.roles if not r.managed]
    if ctx.author == ctx.guild.owner: return True
    if ctx.author.top_role.position > len(roles) - 5 and ctx.author.guild_permissions.administrator: return True
    return False

async def has_head_admin(ctx):
    if await check_admin(ctx) == True:
        return True
    else:
        raise MissingPerms('Главный администратор')

async def has_manage_messages(ctx):
    if ctx.author.guild_permissions.manage_messages or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Управлять сообщениями')
async def has_manage_channels(ctx):
    if ctx.author.guild_permissions.manage_channels or ctx.author == ctx.guild.owner:
        return True
    else:
        raise MissingPerms('Управлять каналами')
async def has_moderator(ctx: disnake.AppCmdInter):
    if ctx.author.guild_permissions.kick_members and ctx.author.guild_permissions.view_audit_log:
        return True
    else:
        raise MissingPerms('Модератор')

async def hack_by_snejok():
    raise Err('litex dev')