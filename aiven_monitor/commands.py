from aiven_monitor.cli import cli
from aiven_monitor.migration.db_migrator import DBMigrator
from aiven_monitor.monitor.monitor_consumer import MonitorConsumer
from aiven_monitor.monitor.monitor_producer import MonitorProducer


@cli.command('run-monitor-event-consumer')
def run_monitor_event_consumer() -> None:
    monitor_consumer = MonitorConsumer.create()
    monitor_consumer.run_consumer()


@cli.command('run-monitor-event-producer')
def run_monitor_event_producer() -> None:
    monitor_producer = MonitorProducer.create()
    monitor_producer.run_producer()


@cli.command('run-migration')
def run_migration() -> None:
    db_migrator = DBMigrator.create()
    db_migrator.migrate()


@cli.command('run-database-website-seeding')
def run_database_website_seeding() -> None:
    db_migrator = DBMigrator.create()
    db_migrator.seed_websites()
