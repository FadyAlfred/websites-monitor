from dotenv import load_dotenv

from aiven_monitor.cli import cli
from aiven_monitor.commands import (
    run_database_website_seeding, run_migration, run_monitor_event_consumer, run_monitor_event_producer
)


if __name__ == '__main__':
    load_dotenv()
    cli()
