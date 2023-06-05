import disnake
import config


async def errmess(ctx, text):
    return await ctx.send(embed=disnake.Embed(title=':no_entry: | Ошибка..', description=f'>>> **{text}**', color=config.error_color))


async def succmess(ctx, text):
    return await ctx.send(embed=disnake.Embed(title=':white_check_mark: | Успешно', description=f'>>> **{text}**', color=config.success_color))
