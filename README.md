# WApps

[![CircleCI](https://img.shields.io/circleci/project/github/apihackers/wapps.svg)](https://circleci.com/gh/apihackers/workflows/wapps)
[![Coverage Status](https://coveralls.io/repos/github/apihackers/wapps/badge.svg?branch=master)](https://coveralls.io/github/apihackers/wapps?branch=master)
[![Last version](https://img.shields.io/pypi/v/wapps.svg)](https://pypi.python.org/pypi/wapps)
[![License](https://img.shields.io/pypi/l/wapps.svg)](https://pypi.python.org/pypi/wapps)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/wapps.svg)](https://pypi.python.org/pypi/wapps)

A very optionated set of Wagtail reusable applications and helpers
meant to speedup website development. There is not any universality intent.

## stack

It assumes the following stacks:

### Server-side stack:

- Python 3
- Latest Wagtail and Django versions
- Django-Jinja for template rendering
- Django-Babel for localization
- Django-Appconf for default settings

### Frontend Stack

- Vue 2 for front components
- Webpack 2 as front build toolchain
- SCSS as style language
- Bootstrap and Font-awesome as base frameworks

## Requirements

Wapps is designed to work with Python 3, Django-jinja, Django-babel and latest Django and Wagtail versions.

Wapps also provides JS/Vue2 helpers and scss mixins and classes

## Installation

### Python installation

Install it with pip:

```shell
$ pip install wapps
```

then add the required bases apps to your settings (ie. `settings.py`):

```python
INSTALLED_APPS = [
    '...',
    'wapps',
    'memoize'
]
```

### Node modules installation

Install it with `npm` or `yarn`

```shell
$ npm install wapps@<wapps-version>
```
