import aiosqlite
from config import Config


class Database:
    @staticmethod
    async def initialize():
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS settings(
                    guild_id INTEGER PRIMARY KEY,
                    log_channel INTEGER,
                    welcome_channel INTEGER,
                    goodbye_channel INTEGER,
                    music_channel INTEGER,
                    ticket_category INTEGER,
                    auto_role INTEGER,
                    prefix TEXT DEFAULT '/'
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS levels(
                    guild_id INTEGER,
                    user_id INTEGER,
                    xp INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    messages INTEGER DEFAULT 0,
                    PRIMARY KEY(guild_id, user_id)
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS level_roles(
                    guild_id INTEGER,
                    level INTEGER,
                    role_id INTEGER,
                    PRIMARY KEY(guild_id, level)
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS giveaways(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    channel_id INTEGER,
                    message_id INTEGER,
                    prize TEXT,
                    winners INTEGER,
                    host INTEGER,
                    end_time INTEGER,
                    ended INTEGER DEFAULT 0
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS giveaway_entries(
                    giveaway_id INTEGER,
                    user_id INTEGER,
                    PRIMARY KEY(giveaway_id, user_id)
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS tickets(
                    channel_id INTEGER PRIMARY KEY,
                    guild_id INTEGER,
                    creator_id INTEGER,
                    claimed_by INTEGER,
                    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    closed INTEGER DEFAULT 0
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS warns(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    user_id INTEGER,
                    moderator_id INTEGER,
                    reason TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS modlogs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    moderator INTEGER,
                    target INTEGER,
                    action TEXT,
                    reason TEXT,
                    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS music_settings(
                    guild_id INTEGER PRIMARY KEY,
                    volume INTEGER DEFAULT 50,
                    autoplay INTEGER DEFAULT 0
                )
                """
            )
            await db.commit()

    @staticmethod
    async def get_setting(guild_id, key, default=None):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute(f"SELECT {key} FROM settings WHERE guild_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row[0] if row[0] is not None else default
                return default

    @staticmethod
    async def set_setting(guild_id, key, value):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO settings(guild_id, prefix) VALUES(?, ?) ON CONFLICT(guild_id) DO NOTHING", (guild_id, "/"))
            await db.execute(f"UPDATE settings SET {key} = ? WHERE guild_id = ?", (value, guild_id))
            await db.commit()

    @staticmethod
    async def add_xp(guild_id, user_id, xp):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO levels(guild_id, user_id, xp, level, messages) VALUES(?, ?, 0, 1, 0) ON CONFLICT(guild_id, user_id) DO NOTHING", (guild_id, user_id))
            await db.execute("UPDATE levels SET xp = xp + ?, messages = messages + 1 WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))
            await db.commit()

    @staticmethod
    async def get_level(guild_id, user_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT xp, level, messages FROM levels WHERE guild_id = ? AND user_id = ?", (guild_id, user_id)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {"xp": row[0], "level": row[1], "messages": row[2]}
                return {"xp": 0, "level": 1, "messages": 0}

    @staticmethod
    async def set_level(guild_id, user_id, level, xp, messages):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO levels(guild_id, user_id, xp, level, messages) VALUES(?, ?, ?, ?, ?) ON CONFLICT(guild_id, user_id) DO UPDATE SET xp = excluded.xp, level = excluded.level, messages = excluded.messages", (guild_id, user_id, xp, level, messages))
            await db.commit()

    @staticmethod
    async def add_level_role(guild_id, level, role_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO level_roles(guild_id, level, role_id) VALUES(?, ?, ?) ON CONFLICT(guild_id, level) DO UPDATE SET role_id = excluded.role_id", (guild_id, level, role_id))
            await db.commit()

    @staticmethod
    async def get_level_roles(guild_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT level, role_id FROM level_roles WHERE guild_id = ? ORDER BY level ASC", (guild_id,)) as cursor:
                rows = await cursor.fetchall()
                return rows

    @staticmethod
    async def add_warn(guild_id, user_id, moderator_id, reason):
        async with aiosqlite.connect(Config.DATABASE) as db:
            cursor = await db.execute("INSERT INTO warns(guild_id, user_id, moderator_id, reason) VALUES(?, ?, ?, ?)", (guild_id, user_id, moderator_id, reason))
            await db.commit()
            return cursor.lastrowid

    @staticmethod
    async def get_warns(guild_id, user_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT id, moderator_id, reason, created FROM warns WHERE guild_id = ? AND user_id = ? ORDER BY created DESC", (guild_id, user_id)) as cursor:
                return await cursor.fetchall()

    @staticmethod
    async def log_mod_action(guild_id, moderator, target, action, reason):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO modlogs(guild_id, moderator, target, action, reason) VALUES(?, ?, ?, ?, ?)", (guild_id, moderator, target, action, reason))
            await db.commit()

    @staticmethod
    async def get_modlogs(guild_id, limit=10):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT moderator, target, action, reason, created FROM modlogs WHERE guild_id = ? ORDER BY id DESC LIMIT ?", (guild_id, limit)) as cursor:
                return await cursor.fetchall()

    @staticmethod
    async def create_giveaway(guild_id, channel_id, message_id, prize, winners, host, end_time):
        async with aiosqlite.connect(Config.DATABASE) as db:
            cursor = await db.execute("INSERT INTO giveaways(guild_id, channel_id, message_id, prize, winners, host, end_time, ended) VALUES(?, ?, ?, ?, ?, ?, ?, 0)", (guild_id, channel_id, message_id, prize, winners, host, end_time))
            await db.commit()
            return cursor.lastrowid

    @staticmethod
    async def add_giveaway_entry(giveaway_id, user_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT OR IGNORE INTO giveaway_entries(giveaway_id, user_id) VALUES(?, ?)", (giveaway_id, user_id))
            await db.commit()

    @staticmethod
    async def get_giveaway(giveaway_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT id, guild_id, channel_id, message_id, prize, winners, host, end_time, ended FROM giveaways WHERE id = ?", (giveaway_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row
                return None

    @staticmethod
    async def get_active_giveaways():
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT id, guild_id, channel_id, message_id, prize, winners, host, end_time, ended FROM giveaways WHERE ended = 0") as cursor:
                return await cursor.fetchall()

    @staticmethod
    async def end_giveaway(giveaway_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("UPDATE giveaways SET ended = 1 WHERE id = ?", (giveaway_id,))
            await db.commit()

    @staticmethod
    async def get_giveaway_entries(giveaway_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT user_id FROM giveaway_entries WHERE giveaway_id = ?", (giveaway_id,)) as cursor:
                rows = await cursor.fetchall()
                return [row[0] for row in rows]

    @staticmethod
    async def create_ticket(channel_id, guild_id, creator_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT OR REPLACE INTO tickets(channel_id, guild_id, creator_id, claimed_by, closed) VALUES(?, ?, ?, NULL, 0)", (channel_id, guild_id, creator_id))
            await db.commit()

    @staticmethod
    async def close_ticket(channel_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("UPDATE tickets SET closed = 1 WHERE channel_id = ?", (channel_id,))
            await db.commit()

    @staticmethod
    async def get_ticket(channel_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT channel_id, guild_id, creator_id, claimed_by, closed FROM tickets WHERE channel_id = ?", (channel_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row
                return None

    @staticmethod
    async def set_music_setting(guild_id, volume, autoplay):
        async with aiosqlite.connect(Config.DATABASE) as db:
            await db.execute("INSERT INTO music_settings(guild_id, volume, autoplay) VALUES(?, ?, ?) ON CONFLICT(guild_id) DO UPDATE SET volume = excluded.volume, autoplay = excluded.autoplay", (guild_id, volume, autoplay))
            await db.commit()

    @staticmethod
    async def get_music_setting(guild_id):
        async with aiosqlite.connect(Config.DATABASE) as db:
            async with db.execute("SELECT volume, autoplay FROM music_settings WHERE guild_id = ?", (guild_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return {"volume": row[0], "autoplay": row[1]}
                return {"volume": Config.DEFAULT_VOLUME, "autoplay": 0}
