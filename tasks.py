# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import os
import sys

from invoke import task, call

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))

PROJECTS = [
    'wappsdemo',
    'wapps',
    'wapps.blog',
    'wapps.gallery',
    'wapps.forms',
]

LANGUAGES = ['fr']

I18N_DOMAIN = 'django'

CLEAN_PATTERNS = [
    'build', 'dist', '**/*.pyc', '**/__pycache__', '.tox', '**/*.mo', 'reports'
]


def color(code):
    '''A simple ANSI color wrapper factory'''
    return lambda t: '\033[{0}{1}\033[0;m'.format(code, t)


green = color('1;32m')
red = color('1;31m')
blue = color('1;30m')
cyan = color('1;36m')
purple = color('1;35m')
white = color('1;39m')


def header(text):
    '''Display an header'''
    print(' '.join((blue('>>'), cyan(text))))
    sys.stdout.flush()


def info(text, *args, **kwargs):
    '''Display informations'''
    text = text.format(*args, **kwargs)
    print(' '.join((purple('>>>'), text)))
    sys.stdout.flush()


def success(text):
    '''Display a success message'''
    print(' '.join((green('>>'), white(text))))
    sys.stdout.flush()


def error(text):
    '''Display an error message'''
    print(red('✘ {0}'.format(text)))
    sys.stdout.flush()


def exit(text=None, code=-1):
    if text:
        error(text)
    sys.exit(-1)


@task
def clean(ctx):
    '''Cleanup all build artifacts'''
    header(clean.__doc__)
    with ctx.cd(ROOT):
        for pattern in CLEAN_PATTERNS:
            info(pattern)
            ctx.run('rm -rf {0}'.format(' '.join(CLEAN_PATTERNS)))


@task
def demo(ctx):
    '''Run the demo'''
    header(demo.__doc__)
    with ctx.cd(ROOT):
        ctx.run('./manage.py migrate', pty=True)
        ctx.run('./manage.py runserver', pty=True)


@task
def test(ctx, report=False):
    '''Run tests suite'''
    header(test.__doc__)
    cmd = 'pytest -v'
    if report:
        cmd = ' '.join((cmd, '--junitxml=reports/python/tests.xml'))
    with ctx.cd(ROOT):
        ctx.run(cmd, pty=True)


@task
def cover(ctx, report=False):
    '''Run tests suite with coverage'''
    header(cover.__doc__)
    cmd = [
        'pytest',
        '--cov-config coverage.rc',
        '--cov-report term',
        '--cov-report html:reports/coverage',
        '--cov-report xml:reports/coverage.xml',
        '--cov=wapps',
    ]
    if report:
        cmd += [
            '--cov-report html:reports/python/coverage',
            '--cov-report xml:reports/python/coverage.xml',
            '--junitxml=reports/python/tests.xml'
        ]
    with ctx.cd(ROOT):
        ctx.run(' '.join(cmd), pty=True)


@task
def qa(ctx):
    '''Run a quality report'''
    header(qa.__doc__)
    with ctx.cd(ROOT):
        info('Python Static Analysis')
        flake8_results = ctx.run('flake8 wapps', pty=True, warn=True)
        if flake8_results.failed:
            error('There is some lints to fix')
        else:
            success('No lint to fix')
        info('Ensure PyPI can render README and CHANGELOG')
        readme_results = ctx.run('python setup.py check -r -s', pty=True, warn=True, hide=True)
        if readme_results.failed:
            print(readme_results.stdout)
            error('README and/or CHANGELOG is not renderable by PyPI')
        else:
            success('README and CHANGELOG are renderable by PyPI')
    if flake8_results.failed or readme_results.failed:
        exit('Quality check failed', flake8_results.return_code or readme_results.return_code)
    success('Quality check OK')


@task
def migration(ctx, app='wapps', name=None, empty=False):
    '''Create a new migration'''
    header('Create a new django migration')
    cmd = ['./manage.py', 'makemigrations', app]
    if name:
        cmd += ['-n', name]
    if empty:
        cmd += ['--empty']
    with ctx.cd(ROOT):
        ctx.run(' '.join(cmd), pty=True)


@task
def update(ctx):
    '''Update dependancies'''
    header(update.__doc__)
    with ctx.cd(ROOT):
        ctx.run('pip install -r requirements/develop.pip')
        ctx.run('npm install')


@task
def i18n(ctx):
    '''Extract translatable strings'''
    header(i18n.__doc__)
    for project in PROJECTS:
        root = project.replace('.', '/')
        with ctx.cd(root):
            ctx.run('pybabel extract -F babel.cfg -o locale/{0}.pot .'.format(I18N_DOMAIN))
            for lang in LANGUAGES:
                translation = os.path.join(root, 'locale', lang, 'LC_MESSAGES', '{0}.po'.format(I18N_DOMAIN))
                if not os.path.exists(translation):
                    ctx.run('pybabel init -D {domain} -i locale/django.pot -d locale -l {lang}'.format(
                        lang=lang, domain=I18N_DOMAIN
                    ))
                ctx.run('pybabel update -D {0} -i locale/{0}.pot -d locale'.format(I18N_DOMAIN))
            ctx.run('rm locale/{0}.pot'.format(I18N_DOMAIN))


@task
def i18nc(ctx):
    '''Compile translations'''
    header(i18nc.__doc__)
    for project in PROJECTS:
        root = project.replace('.', '/')
        with ctx.cd(root):
            ctx.run('pybabel compile -D {0} -d locale --statistics'.format(I18N_DOMAIN))


@task(i18nc)
def dist(ctx, buildno=None):
    '''Package for distribution'''
    header(dist.__doc__)
    cmd = ['python3 setup.py']
    if buildno:
        cmd.append('egg_info -b {0}'.format(buildno))
    cmd.append('bdist_wheel')
    with ctx.cd(ROOT):
        ctx.run(' '.join(cmd), pty=True)
    success('Distribution is available in dist directory')


@task(clean, qa, call(cover, report=True), dist, default=True)
def all(ctx):
    '''Run tests, reports and packaging'''
    pass


@task
def dronecrypt(ctx):
    '''Encrypt drone secrets'''
    header(dronecrypt.__doc__)
    with ctx.cd(ROOT):
        ctx.run('drone secure --repo apihackers/wapps --in drone.secrets.yml')
