# -*- coding: utf-8 -*-

"""Console script for gcloud_cli."""

import click
import atexit

from . import __version__
from . import thingy52

CONTEXT_SETTINGS = dict(
    obj={},
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, debug):
    """Console script for gcloud_cli."""
    pass


@main.command()
def version():
    """Display the current version."""
    click.echo(__version__)


@click.command()
@click.pass_context
def list_services(ctx):
    """Console script for gcloud_cli."""
    pass


@main.command()
@click.argument('address')
def list(address):
    """
    List topics.
    """
    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)


@main.command()
@click.argument('address')
def listen(address):
    """
    List topics.
    """
    thingy52.listen_to_thingy(address)


if __name__ == "__main__":
    main()
