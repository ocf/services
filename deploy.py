#!/usr/bin/env python3
import copy
import getpass
import json
import os.path
from collections import namedtuple

import yaml
from cached_property import cached_property
from ocflib.infra.mesos.marathon import MarathonClient
from ocflib.misc import shell


APPS_PATH = os.path.join(os.path.dirname(__file__), 'apps')


def unbuf_print(*args, **kwargs):
    kwargs.setdefault('flush', True)
    print(*args, **kwargs)


def all_apps():
    return frozenset(
        App(path=dirpath)
        for dirpath, dirnames, filenames in os.walk(APPS_PATH)
        if 'app.yaml' in filenames
    )


class App(namedtuple('App', ('path',))):
    """An app on disk."""

    @property
    def id(self):
        return self.json['id']

    @cached_property
    def json(self):
        with open(os.path.join(self.path, 'app.yaml')) as f:
            return yaml.safe_load(f)


def diff_json(a, b, path=''):
    """Diff two Marathon JSON blobs.

    Returns True if there are any interesting differences anywhere in the tree.
    """
    # Some key/values change all the time and obviously aren't part of our
    # configuration (e.g. how many tasks are currently healthy), so we don't
    # diff them.
    if path in {
            '["deployments"]',
            '["lastTaskFailure"]',
            '["ports"]',
            '["tasks"]',
            '["tasksHealthy"]',
            '["tasksRunning"]',
            '["tasksStaged"]',
            '["tasksUnhealthy"]',
            '["version"]',
            '["versionInfo"]',
    }:
        return False

    if isinstance(a, dict) and isinstance(b, dict):
        found_change = False
        for key in sorted(set(a.keys()) | set(b.keys())):
            found_change |= diff_json(a.get(key), b.get(key), path + '["{}"]'.format(key))
        return found_change
    elif a != b:
        if path == '["container"]["docker"]["image"]':
            a_repo, _ = split_docker(a)
            b_repo, _ = split_docker(b)

            if a_repo == b_repo:
                return False

        # Some things are not interesting (e.g. sometimes we omit a key, but
        # really it's an empty list). Only complain if one is interesting.
        def interesting(thing):
            return thing not in (None, [], {})

        if interesting(a) or interesting(b):
            print('  Difference at {}'.format(path))
            print('    Current value: {}'.format(shell.red(repr(b))))
            print('    Desired value: {}'.format(shell.green(repr(a))))
            return True

    return False


def split_docker(tag):
    if ':' in tag:
        repo, version = tag.split(':')
        return repo, version
    else:
        return tag, 'latest'


def update_app(client, app):
    print(shell.bold('Comparing "{}" on-disk definition to the current status in Marathon:'.format(app.id)))
    deployed = client.app_status(app.id)['app']
    changes = diff_json(app.json, deployed)

    if not changes:
        print(shell.bold(shell.green('There were no differences.')))
    else:
        print(shell.bold(shell.yellow(
            'There were differences. Starting a new deployment.',
        )))

        # update the image tag (this doesn't quite match the on-disk tag)
        on_disk_tag = split_docker(app.json['container']['docker']['image'])
        deployed_tag = split_docker(deployed['container']['docker']['image'])

        new_json = copy.deepcopy(app.json)

        if on_disk_tag[0] == deployed_tag[0]:
            # The repo didn't change, but the version did.
            new_json['container']['docker']['image'] = '{}:{}'.format(*deployed_tag)
        else:
            # The repo changed, so reset to ${repo}:latest.
            new_json['container']['docker']['image'] = '{}:{}'.format(*on_disk_tag)

        client.deploy_app(app.id.lstrip('/'), new_json, report=unbuf_print)

        # make sure there are no longer any differences
        print(shell.bold('Confirming there are now no differences...'))
        new_deployed = client.app_status(app.id)['app']
        if diff_json(app.json, new_deployed):
            print(shell.bold(shell.red(
                'There were still differences in the on-disk and deployed version of "{}", '
                'even after making a new deployment.\n'
                '\n'
                'This most likely means that the app config is missing some default value.\n'
                "This isn't a huge problem, but it *does* mean that every time this repo gets pushed, "
                'we do a no-op push which wastes time :(\n'
                '\n'
                'You should fix this, probably by taking the differences listed above and adding\n'
                "them to the app's config on disk.".format(app.id)
            )))
            raise AssertionError('Deployment failed.')
        else:
            print(shell.bold(shell.green('OK!')))


def main():
    creds_path = os.path.join(os.path.expanduser('~'), '.ocf-marathon')
    if os.path.isfile(creds_path):
        with open(creds_path) as f:
            creds = json.load(f)
        user = creds['user']
        password = creds['password']
    else:
        user = getpass.getuser()
        password = getpass.getpass()

    client = MarathonClient(user, password)

    for app in all_apps():
        update_app(client, app)


if __name__ == '__main__':
    exit(main())
