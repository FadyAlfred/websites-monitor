from logging import Logger
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock

from psycopg.connection import Connection

from aiven_monitor.migration.db_migrator import DBMigrator


class TestDBMigrator(TestCase):
    def setUp(self):
        self._fake_db_connection = MagicMock(spec=Connection)
        self._fake_logger = MagicMock(spec=Logger)

        self.db_migrator = DBMigrator(self._fake_db_connection, self._fake_logger)

        self._mock_manager = Mock()
        self._mock_manager.attach_mock(self._fake_db_connection, 'fake_db_connection')
        self._mock_manager.attach_mock(self._fake_logger, 'fake_logger')

    def test_migrate(self):
        self.db_migrator.migrate()

        expected_calls = [
            call.fake_logger.info('Migrate the database schema'),
            call.fake_db_connection.cursor(),
            call.fake_db_connection.cursor().execute(open('aiven_monitor/migration/queries/db_schema.sql', 'r').read()),
            call.fake_db_connection.close()
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)

    def test_seed_websites(self):
        self.db_migrator.seed_websites()

        expected_calls = [
            call.fake_logger.info('Seed the database with websites'),
            call.fake_db_connection.cursor(),
            call.fake_db_connection.cursor().execute(
                open('aiven_monitor/migration/queries/websites_seed.sql', 'r').read()
            ),
            call.fake_db_connection.commit(),
            call.fake_db_connection.close()
        ]

        self.assertEqual(self._mock_manager.mock_calls, expected_calls)
