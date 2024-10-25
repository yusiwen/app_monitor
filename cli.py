from app_monitor import es, settings

import os
import click

def _init():
    return

@click.command()
@click.option('--name', default='', prompt='Name of app', help='Name of app')
def run(name):
    r = es.get_app_by_name(name)
    for hit in r:
        print(hit.name, ": ", hit.version)


if __name__ == '__main__':
    _init()
    run()
