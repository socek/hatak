import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hatak.db import Base


class TestDatabase(object):

    def __init__(self, settings):
        self.settings = settings

    def recreate_database(self):
        if self.settings['db:url'].startswith('sqlite'):
            self.recreate_sqlite_database()
            return
        url = self.settings['db:testurl']
        engine = create_engine(url)

        connection = engine.connect()
        connection.execute("commit")
        connection.execute(
            "drop database if exists %(db:db)s" % (self.settings))
        connection.execute("commit")
        connection.execute("create database %(db:db)s" % (self.settings))
        connection.close()

    def recreate_sqlite_database(self):
        try:
            os.unlink(self.settings['sqlite_db'])
        except FileNotFoundError:
            pass

    def get_engine_and_session(self):
        url = self.settings['db:url']
        engine = create_engine(url)
        session = sessionmaker(bind=engine)()
        return engine, session

    def create_all(self, engine):
        Base.metadata.create_all(engine)
