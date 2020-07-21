import asyncio

from aiocache import Cache
from databases import Database

import config
from files_app.models import init_db

Settings = config.CONFIG()
cache = Cache()


def setup_database(db_config):
    db = Database(db_config)
    asyncio.get_event_loop().run_until_complete(init_db(db))
    return db


db = setup_database(Settings.get_db_config())
