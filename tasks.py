# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from invoke import run as irun, task

from os.path import join, abspath, dirname

ROOT = abspath(join(dirname(__file__)))


def run(cmd, *args, **kwargs):
    '''Run a command ensuring cwd is project root'''
    return irun('cd {0} && {1}'.format(ROOT, cmd), *args, **kwargs)


@task
def clean(ctx, docs=False, bytecode=False, extra=''):
    '''Cleanup all build artifacts'''
    patterns = ['build', 'dist', 'cover', 'docs/_build', '**/*.pyc', '*.egg-info', '.tox']
    for pattern in patterns:
        print('Removing {0}'.format(pattern))
        run('rm -rf {0}'.format(pattern))


@task
def demo(ctx):
    '''Run the demo'''
    run('python examples/todo.py')


@task
def test(ctx):
    '''Run tests suite'''
    run('nosetests --force-color', pty=True)


@task
def cover(ctx):
    '''Run tests suite with coverage'''
    run('nosetests --force-color --with-coverage --cover-html', pty=True)


@task
def tox(ctx):
    '''Run tests against Python versions'''
    run('tox', pty=True)


@task
def qa(ctx):
    '''Run a quality report'''
    run('flake8 wapps')


@task
def doc(ctx):
    '''Build the documentation'''
    run('cd doc && make html', pty=True)


@task
def update(ctx):
    '''Update dependancies'''
    run('pip install -r requirements/develop.pip')
    run('npm install')


@task
def assets(ctx):
    '''Fetch web assets'''
    run('npm run build')


@task
def dist(ctx):
    '''Package for distribution'''
    run('python setup.py sdist bdist_wheel', pty=True)


@task(tox, doc, qa, assets, dist, default=True)
def all(ctx):
    '''Run tests, reports and packaging'''
    pass
