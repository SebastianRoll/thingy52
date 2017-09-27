# -*- coding: utf-8 -*-

"""Console script for gcloud_cli."""

import atexit

import click

from thingy52 import delegates
from thingy52.services import Color
from . import __version__
from . import thingy52

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
def speaker_stream(ctx):
    """
    """
    address = ctx.obj.get("address")

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)

    t.sound.activate_speaker_stream(speaker_mode=2, mic_mode=1)
    while True:
        print("k")
        t.sound.stream_speaker()


@main.command()
@click.pass_context
def speaker_frequency(ctx):
    """
    """
    address = ctx.obj.get("address")

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    t.sound.activate_speaker_stream(1, 1)
    t.sound.stream_frequency(frequency=10500, duration=500, volume=50)


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


@main.command()
@click.pass_context
def demo_led2(ctx):
    """
    Enable/Disable motion characteristics.
    """
    address = ctx.obj.get("address")

    t = thingy52.Thingy52(address)
    atexit.register(t.disconnect)
    t.setDelegate(delegates.ThingyCharDelegate(t.handles))
    t.ui.rgb_breathe(color=Color.CYAN)
    t.sound.play_sample()
    while True:
        t.waitForNotifications(1.0)
        print("Waiting...")



if __name__ == "__main__":
    main()
