import os
from logging import getLogger, Logger
from os.path import dirname, join

import psycopg
from psycopg.connection import Connection


class DBMigrator:
    def __init__(self, db_connection: Connection, logger: Logger):
        self.db_connection = db_connection
        self.logger = logger

    def migrate(self):
        self.logger.info('Migrate the database schema')
        self.db_connection.cursor().execute(open(f'{join(dirname(__file__))}/queries/db_schema.sql', 'r').read())

        self.db_connection.close()

    def seed_websites(self):
        self.logger.info('Seed the database with websites')
        self.db_connection.cursor().execute(open(f'{join(dirname(__file__))}/queries/websites_seed.sql', 'r').read())
        self.db_connection.commit()

        self.db_connection.close()

    @classmethod
    def create(cls):
        return cls(
            psycopg.connect(
                user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT'), dbname=os.getenv('DB_NAME')
            ),
            getLogger(__name__)
        )
