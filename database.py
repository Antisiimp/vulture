import sqlite3

db = sqlite3.connect('data.db')
cur = db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS prefixes (
    prefix TEXT,
    guild_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS whitelist (
    guild_id INTEGER,
    user_id INTEGER,
    action TEXT
)""")
db.commit()
         
cur.execute("""CREATE TABLE IF NOT EXISTS logs (
    guild_id INTEGER,
    channel_id INTEGER,
    webhook_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS languages (
    guild_id INTEGER,
    language INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS webhook (
    guild_id INTEGER,
    channel_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS antibot (
    guild_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS hardbot (
    guild_id INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS anticrash (
    guild_id INTEGER,
    action TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS blacklist (
    user_id INTEGER,
    reason TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS text_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    position INTEGER,
    category TEXT,
    nsfw TEXT,
    slowmode INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS forum_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    position INTEGER,
    category TEXT,
    nsfw TEXT,
    slowmode INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS passwords (
    guild_id INTEGER,
    code INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS stage_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    position INTEGER
    category TEXT,
    nsfw TEXT,
    slowmode INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS voice_channels (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    postion INTEGER,
    category TEXT
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS categories (
    guild_id INTEGER,
    name TEXT,
    perms TEXT,
    postion INTEGER
)""")
db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS roles (
    guild_id INTEGER,
    name TEXT,
    perms INTEGER,
    position INTEGER,
    hoist TEXT,
    mentionable TEXT,
    color TEXT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS serversNames (
    guild_id INTEGER,
    name TEXT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS serverIcons (
    guild_id INTEGER,
    icon INTEGER
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS warns (
    guild_id INTEGER,
    user_id INTEGER,
    reason TEXT,
    warn_number INTEGER
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS timebans (
    guild_id INTEGER,
    user_id INTEGER,
    time BIGINT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS timemutes (
    guild_id INTEGER,
    user_id INTEGER,
    time BIGINT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS mutes (
    guild_id INTEGER,
    user_id INTEGER
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS timequas (
    guild_id INTEGER,
    user_id INTEGER, 
    time BIGINT
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS quas (
    guild_id INTEGER,
    user_id INTEGER
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS muteroles (
    guild_id INTEGER,
    role_id INTEGER
)""")

db.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS quaroles (
    guild_id INTEGER,
    role_id INTEGER
)""")

db.commit()