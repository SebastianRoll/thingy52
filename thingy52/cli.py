# -*- coding: utf-8 -*-

"""Console script for gcloud_cli."""

import click
import atexit

from . import __version__
from . import thingy52
from thingy52 import delegates
from thingy52.audio import RecordingDelegate

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

@main.command()
@click.argument('feature')
@click.option('--enable', default=True)
@click.pass_context
def sound(ctx, feature, enable):
    """
    Enable/Disable motion characteristics.
    """
    address = ctx.obj.get("address")
    print(address)

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    t.setDelegate(delegates.ThingyCharDelegate(t.handles))
    t.sound.toggle_notifications(characteristic=feature, enable=enable)
    while True:
        t.waitForNotifications(1.0)
        print("Waiting...")

@main.command()
@click.pass_context
def record(ctx):
    """
    Enable/Disable motion characteristics.
    """
    address = ctx.obj.get("address")

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    rec = RecordingDelegate(t.handles)
    t.setDelegate(rec)
    atexit.register(rec.finish)
    t.sound.toggle_notifications(characteristic="microphone", enable=True)
    for i in range(100):
        t.waitForNotifications(1.0)



@main.command()
@click.pass_context
def demo_led(ctx):
    """
    Enable/Disable motion characteristics.
    """
    address = ctx.obj.get("address")

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    d = delegates.Demo1Delegate(t, t.handles)
    t.setDelegate(d)
    t.ui.toggle_notifications(characteristic="button", enable=True)
    while True:
        t.waitForNotifications(1.0)



if __name__ == "__main__":
    main()
