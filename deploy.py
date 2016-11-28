#!/usr/bin/env python3
import json
import os.path
from collections import namedtuple

from cached_property import cached_property


APPS_PATH = os.path.join(os.path.dirname(__file__), 'apps')


def all_apps():
    return frozenset(
        App(path=dirpath)
        for dirpath, dirnames, filenames in os.walk(APPS_PATH)
        if 'app.json' in filenames
    )


class App(namedtuple('App', ('path',))):

    @cached_property
    def json(self):
        with open(os.path.join(self.path, 'app.json')) as f:
            return json.load(f)


def main():
    pass


if __name__ == '__main__':
    exit(main())
