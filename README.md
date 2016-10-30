# WApps

[![Build Status](https://ci.noirbizarre.info/api/badges/apihackers/wapps/status.svg)](https://ci.noirbizarre.info/apihackers/wapps)

A very optionated set of Wagtail reusable applications and helpers
meant to speedup website development.

# Requirements

Wapps is designed to work with Python 3, Django-jinja, Django-babel and latest Django and Wagtail versions.

## Installation

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
