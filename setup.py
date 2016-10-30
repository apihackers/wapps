#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
from __future__ import unicode_literals

import re
import sys

from os.path import join, dirname

from setuptools import setup, find_packages


ROOT = dirname(__file__)

RE_REQUIREMENT = re.compile(r'^\s*-r\s*(?P<filename>.*)$')

PYPI_RST_FILTERS = (
    # Replace code-blocks
    (r'\.\.\s? code-block::\s*(\w|\+)+', '::'),
    # Remove all badges
    (r'\.\. image:: .*', ''),
    (r'\s+:target: .*', ''),
    (r'\s+:alt: .*', ''),
    # Replace Python crossreferences by simple monospace
    (r':(?:class|func|meth|mod|attr|obj|exc|data|const):`~(?:\w+\.)*(\w+)`', r'``\1``'),
    (r':(?:class|func|meth|mod|attr|obj|exc|data|const):`([^`]+)`', r'``\1``'),
    # replace doc references
    (r':doc:`(.+) <(.*)>`', r'`\1 <http://wapps.readthedocs.org/en/stable\2.html>`_'),
    # replace issues references
    (r':issue:`(.+)`', r'`#\1 <https://github.com/apihackers/wapps/issues/\1>`_'),
    # Drop unrecognized currentmodule
    (r'\.\. currentmodule:: .*', ''),
)


def pip(filename):
    """Parse pip reqs file and transform it to setuptools requirements."""
    requirements = []
    if not filename.endswith('.pip'):
        filename = '{0}.pip'.format(filename)
    for line in open(join(ROOT, 'requirements', filename)):
        line = line.strip()
        if not line or '://' in line:
            continue
        match = RE_REQUIREMENT.match(line)
        if match:
            requirements.extend(pip(match.group('filename')))
        else:
            requirements.append(line)
    return requirements


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
     - all badges
    '''
    content = open(filename).read()
    for regex, replacement in PYPI_RST_FILTERS:
        content = re.sub(regex, replacement, content)
    return content


long_description = '\n'.join((
    rst('README.md'),
    # rst('CHANGELOG.rst'),
    ''
))


exec(compile(open('wapps/__about__.py').read(), 'wapps/__about__.py', 'exec'))

# insta

# tests_require = ['nose', 'rednose', 'blinker', 'tzlocal']
# install_requires = ['Flask>=0.8', 'six>=1.3.0', 'jsonschema', 'pytz', 'aniso8601>=0.82']
# doc_require = ['sphinx', 'alabaster', 'sphinx_issues']
# dev_requires = ['flake8', 'minibench', 'tox', 'invoke'] + tests_require + doc_require
# test_require = []

setup(
    name='wapps',
    version=__version__,
    description=__description__,
    long_description=long_description,
    # url='https://github.com/apihackers/wapps',
    author='API Hackers',
    author_email='wapps@apihackers.com',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=pip('install'),
    tests_require=[],
    extras_require={
        'test': [],
        'doc': [],
        # 'dev': pip('develop'),
    },
    license='MIT',
    zip_safe=False,
    keywords='wagtail',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: System :: Software Distribution',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
)
