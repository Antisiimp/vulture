#тут мб будет хуйня с войсами

import sqlite3
from disnake.ui import ActionRow, Select, Button, View
from disnake import AppCmdInter, SelectOption, ButtonStyle
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
import adms
import mods
import times

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = sqlite3.connect('data.db')
        self.cur = self.db.cursor()

def setup(bot):
    bot.add_cog(Voice(bot))