# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import sys

from invoke import run as irun, task

from os.path import join, abspath, dirname

ROOT = abspath(join(dirname(__file__)))

PROJECTS = [
    'wappsdemo',
    'wapps',
    'wapps.blog',
    'wapps.gallery',
]

LANGUAGES = ['fr']

I18N_DOMAIN = 'django'


CLEAN_PATTERNS = [
    'build', 'dist', 'htmlcover', '**/*.pyc', '**/__pycache__',
    '*.egg-info', '.tox', 'coverage.xml', '**/*.mo',
]


def color(code):
    '''A simple ANSI color wrapper factory'''
    return lambda t: '\033[{0}{1}\033[0;m'.format(code, t)


green = color('1;32m')
red = color('1;31m')
cyan = color('1;36m')
purple = color('1;35m')


def header(text):
    '''Display an header'''
    print(green('>> {0}'.format(text)))
    sys.stdout.flush()


def info(text):
    '''Display informations'''
    print(cyan('>>> {0}'.format(text)))
    sys.stdout.flush()


def subinfo(text):
    print(purple('>>>> {0}'.format(text)))
    sys.stdout.flush()


def error(text):
    print(red(' '.join((KO, text))))
    sys.stdout.flush()


def exit(text):
    error(text)
    sys.exit(-1)


def run(cmd, *args, **kwargs):
    '''Run a command ensuring cwd is project root'''
    return irun('cd {0} && {1}'.format(ROOT, cmd), *args, **kwargs)


@task
def clean(ctx):
    '''Cleanup all build artifacts'''
    header(clean.__doc__)
    for pattern in CLEAN_PATTERNS:
        info(pattern)
    run('rm -rf {0}'.format(' '.join(CLEAN_PATTERNS)))


@task
def demo(ctx):
    '''Run the demo'''
    header(demo.__doc__)
    run('./manage.py migrate')
    run('./manage.py runserver')


@task
def test(ctx):
    '''Run tests suite'''
    header(test.__doc__)
    run('py.test tests/', pty=True)


@task
def cover(ctx):
    '''Run tests suite with coverage'''
    header(cover.__doc__)
    options = [
        '--cov-config coverage.rc',
        '--cov-report term:skip-covered',
        '--cov-report html:htmlcov',
        '--cov-report xml:coverage.xml',
        '--cov=wapps',
    ]
    run('py.test {0} tests/'.format(' '.join(options)), pty=True)


@task
def qa(ctx):
    '''Run a quality report'''
    header(qa.__doc__)
    run('flake8 wapps')


@task
def update(ctx):
    '''Update dependancies'''
    header(update.__doc__)
    run('pip install -r requirements/develop.pip')
    # run('npm install')


@task
def i18n(ctx):
    '''Extract translatable strings'''
    header(i18n.__doc__)
    for project in PROJECTS:
        root = project.replace('.', '/')
        run('cd {root} && pybabel extract -F babel.cfg -o locale/{domain}.pot .'.format(
            root=root, domain=I18N_DOMAIN
        ))
        for lang in LANGUAGES:
            translation = os.path.join(root, 'locale', lang, 'LC_MESSAGES', '{0}.po'.format(I18N_DOMAIN))
            if not os.path.exists(translation):
                run('pybabel init -D {domain} -i {root}/locale/django.pot -d {root}/locale -l {lang}'.format(
                    root=root, lang=lang, domain=I18N_DOMAIN
                ))
            run('pybabel update -D {domain} -i {root}/locale/{domain}.pot -d {root}/locale'.format(
                root=root, domain=I18N_DOMAIN
            ))
        run('rm {root}/locale/{domain}.pot'.format(root=root, domain=I18N_DOMAIN))


@task
def i18nc(ctx):
    '''Compile translations'''
    header(i18nc.__doc__)
    for project in PROJECTS:
        root = project.replace('.', '/')
        run('pybabel compile -D {domain} -d {root}/locale --statistics'.format(root=root, domain=I18N_DOMAIN))


@task(clean, i18nc)
def dist(ctx, buildno=None):
    '''Package for distribution'''
    header(dist.__doc__)
    cmd = ['python setup.py']
    if buildno:
        cmd.append('egg_info -b {0}'.format(buildno))
    cmd.append('bdist_wheel')
    run(' '.join(cmd), pty=True)


@task(qa, test, dist, default=True)
def all(ctx):
    '''Run tests, reports and packaging'''
    pass


@task
def dronecrypt(ctx):
    '''Encrypt drone secrets'''
    header(dronecrypt.__doc__)
    run('drone secure --repo apihackers/sphene-wedding --in drone.secrets.yml')
