import string, datetime

import pytz

def string_to_seconds(string):
    total_seconds, number_string = 0, ''
    string = string.lower().strip('-').replace('мес', 'е').replace('mo', 'o')
    multi = 1
    units = {
        "s": 1,
        "с": 1,
        "m": 60,
        "м": 60,
        "h": 3600,
        "ч": 3600,
        "d": 86400,
        "д": 86400,
        "w": 604800,
        "н": 604800,
        "o": 2592000,
        "е": 2592000,
        "y": 31536000,
        "г": 31536000,
        "л": 31536000
    }
    for char in string:
        if char.isdigit():
            number_string += char
        else:
            try:
                multi = units[char]
            except KeyError:
                multi = 1
            try:
                total_seconds += int(number_string) * multi
            except:
                pass
            number_string = ''
    if total_seconds < 0:
        total_seconds = 0
    return total_seconds

def word_correct(number: int, p1, p2, p3):
    number = str(number)
    ld = number[-2:]
    cases = {
        "0": "p3",
        "1": "p1",
        "2": "p2",
        "3": "p2",
        "4": "p2",
        "5": "p3",
        "6": "p3",
        "7": "p3",
        "8": "p3",
        "9": "p3"
    }
    if ld[0] == "1" and len(ld) > 1:
        case = "p3"
    else:
        if len(ld) == 1:
            case = cases[ld[0]]
        else:
            case = cases[ld[1]]

    words = {
        "p1": p1,
        "p2": p2,
        "p3": p3
    }
    return words[case]
def hms(sec: float):
    w = int(sec // 604800)
    d = int((sec % 604800) // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)
    
    if d > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_d = f'{d} {word_correct( d, "день", "дня", "дней" )} '
        else:
            display_d = f'{d} {word_correct( d, "day", "days", "days")} '
    else:
        display_d = ''

    if h > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_h = f'{h} {word_correct( h, "час", "часа", "часов" )} '
        else:
            display_h = f'{h} {word_correct( h, "hour", "hours", "hours")} '
    else:
        display_h = ''

    if m > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_m = f'{m} {word_correct( m, "минута", "минуты", "минут" )} '
        else:
            display_m = f'{m} {word_correct( m, "minute", "minutes", "minutes")} '
    else:
        display_m = ''

    if s > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_s = f'{s} {word_correct(s, "секунда", "секунды", "секунд" )}'
        else:
            display_s = f'{s} {word_correct(s, "second", "seconds", "seconds")}'
    else:
        display_s = ''

    if sec < 1:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{ms} {word_correct( ms, "миллисекунда", "миллисекунды", "миллисекунд" )}'.strip()
        else:
            return f'{ms} {word_correct( ms, "millisecond", "milliseconds", "milliseconds")}'.strip()
    elif sec < 60:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{s} {word_correct( s, "секунда", "секунды", "секунд" )}'.strip()
        else:
            return f'{s} {word_correct( s, "second", "seconds", "seconds")}'.strip()
    elif sec < 3600:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{m} {word_correct( m, "минута", "минуты", "минут" )} {display_s}'.strip()
        else:
            return f'{m} {word_correct( m, "minute", "minutes", "minutes")} {display_s}'.strip()
    elif sec < 86400:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{h} {word_correct( h, "час", "часа", "часов" )} {display_m}{display_s}'.strip()
        else:
            return f'{h} {word_correct( h, "hour", "hours", "hours")} {display_m}{display_s}'.strip()
    elif sec < 604800:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{display_d}{display_h}{display_m}{display_s}'.strip()
        else:
            return f'{display_d}{display_h}{display_m}{display_s}'.strip()
    else:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{w} {word_correct( w, "неделя", "недели", "недель" )} {display_d}{display_h}{display_m}{display_s}'.strip()
        else:
            return f'{w} {word_correct( w, "week", "weeks", "weeks")} {display_d}{display_h}{display_m}{display_s}'.strip()

def hms2(sec: float):
    w = int(sec // 604800)
    d = int((sec % 604800) // 86400)
    h = int((sec % 86400) // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(sec % 1 * 1000)
    
    if d > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_d = f'{d} {word_correct( d, "день", "дня", "дней" )} '
        else:
            display_d = f'{d} {word_correct( d, "day", "days", "days")} '
    else:
        display_d = ''

    if h > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_h = f'{h} {word_correct( h, "час", "часа", "часов" )} '
        else:
            display_h = f'{h} {word_correct( h, "hour", "hours", "hours")} '
    else:
        display_h = ''

    if m > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_m = f'{m} {word_correct( m, "минуту", "минуты", "минут" )} '
        else:
            display_m = f'{m} {word_correct( m, "minute", "minutes", "minutes")} '
    else:
        display_m = ''

    if s > 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            display_s = f'{s} {word_correct(s, "секунду", "секунды", "секунд" )}'
        else:
            display_s = f'{s} {word_correct(s, "second", "seconds", "seconds")}'
    else:
        display_s = ''

    if sec < 1:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{ms} {word_correct( ms, "миллисекунду", "миллисекунды", "миллисекунд" )}'
        else:
            return f'{ms} {word_correct( ms, "millisecond", "milliseconds", "milliseconds" )}'
    elif sec < 60:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{s} {word_correct( s, "секунду", "секунды", "секунд" )}'
        else:
            return f'{s} {word_correct( s, "second", "seconds", "seconds")}'
    elif sec < 3600:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{m} {word_correct( m, "минуту", "минуты", "минут" )} {display_s}'
        else:
            return f'{m} {word_correct( m, "minute", "minutes", "minutes" )} {display_s}'
    elif sec < 86400:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{h} {word_correct( h, "час", "часа", "часов" )} {display_m}{display_s}'
        else:
            return f'{h} {word_correct( h, "hour", "hours", "hours" )} {display_m}{display_s}'
    elif sec < 604800:
            return f'{display_d}{display_h}{display_m}{display_s}'.strip()
    else:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f'{w} {word_correct( w, "неделю", "недели", "недель" )} {display_d}{display_h}{display_m}{display_s}'.strip()
        else:
            return f'{w} {word_correct( w, "week", "weeks", "weeks")} {display_d}{display_h}{display_m}{display_s}'.strip()
        
def oneof(string, list):
    found = False
    for l in list:
        if l in string.lower():
            found = True
            break
    return found, l

def ishs(string1):
    string1 = string1.lower()
    return oneof(string1, list('smhdwyсмчднгл'))[0] and oneof(string1, [str(n) for n in string.digits])[0]

def ago(dt):
    days = (datetime.datetime.now(pytz.timezone("Europe/Moscow")) - dt).days
    if days >= 365:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = f'{days//365} {word_correct(days//365, "год", "года", "лет")} назад'
        else:
            d = f'{days//365} {word_correct(days//365, "year", "years", "years")} ago'
    elif days >= 30:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = f'{days//30} {word_correct(days//30, "месяц", "месяца", "месяцев")} назад'
        else:
            d = f'{days//30} {word_correct(days//30, "month", "months", "months")} ago'
    elif days >= 7:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = f'{days//7} {word_correct(days//7, "неделю", "недели", "недель")} назад'
        else:
            d = f'{days//7} {word_correct(days//7, "week", "weeks", "weeks")} ago'
    elif days > 1:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = f'{days} {word_correct(days, "день", "дня", "дней")} назад'
        else:
            d = f'{days} {word_correct(days, "day", "days", "days")} ago'
    elif days == 1:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = 'вчера'
        else:
            d = 'yesterday'
    elif days == 0:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            d = 'сегодня'
        else:
            d = 'today'
    return d

def eround(number: float, decimal: int = 0):
    if str(round(number, decimal)).endswith(".0"):
        return int(number)
    return round(number, decimal)

def unit(number: int):
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{eround(number / 1000, 1)} тыс"
    elif number < 1000000000:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f"{eround(number / 1000000, 1)} млн"
        else:
            return f"{eround(number / 1000000, 1)} mln"
    elif number < 1000000000000:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f"{eround(number / 1000000000, 1)} млрд"
        else:
            return f"{eround(number / 1000000000, 1)} mlrd"
    else:
        if self.cur.execute("SELECT * FROM languages WHERE guild_id = {}".format(ctx.guild.id)).fetchone() == False:
            return f"{eround(number / 1000000000000, 1)} трлн"
        else:
            return f"{eround(number / 1000000000000, 1)} trln"