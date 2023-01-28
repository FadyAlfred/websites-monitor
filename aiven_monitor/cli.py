import logging

import click
import click_log

main_logger = logging.getLogger('main')
main_logger.setLevel('INFO')
click_log.basic_config(main_logger)


@click.group()
@click.option('--loglevel', envvar='LOGLEVEL', default='ERROR')
@click_log.simple_verbosity_option(main_logger)
def cli(loglevel):
    logging.basicConfig(level=loglevel)
