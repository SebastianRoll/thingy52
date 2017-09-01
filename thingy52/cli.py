# -*- coding: utf-8 -*-

"""Console script for gcloud_cli."""

import click
import atexit

from . import __version__
from . import thingy52
from thingy52 import delegates

CONTEXT_SETTINGS = dict(
    obj={},
)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option('--debug/--no-debug', default=False)
@click.argument('address')
@click.pass_context
def main(ctx, debug, address):
    """Console script for gcloud_cli."""
    ctx.obj['address'] = address


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
@click.pass_context
def list_services(ctx):
    """
    List services.
    """
    address = ctx.obj.get("address")
    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)


@main.command()
@click.pass_context
def list_characteristics(ctx):
    """
    List characteristics.
    """
    address = ctx.obj.get("address")
    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)


@main.command()
@click.argument('feature')
@click.option('--enable', default=True)
@click.pass_context
def motion(ctx, feature, enable):
    """
    Enable/Disable motion characteristics.
    """
    address = ctx.obj.get("address")
    print(address)

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    t.setDelegate(delegates.ThingyCharDelegate(t.handles))
    t.motion.toggle_notifications(characteristic=feature, enable=enable)
    while True:
        t.waitForNotifications(1.0)
        print("Waiting...")


if __name__ == "__main__":
    main()
