# django_json_logging
Various JSON logging extensions for the Django Framework

[![PyPI Version][pypi-image]][pypi-url]

[pypi-image]: https://img.shields.io/pypi/v/django_json_logging
[pypi-url]: https://pypi.org/project/django_json_logging/

# Installation

Using pip

`pip install django_json_logging`

Using pipenv

`pipenv install django_json_logging`

# Quick start
In your project’s `settings.py` add `AccessLogMiddleware` to `MIDDLEWARE` and add `JSONFormatter` to `LOGGING`.

```
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
    'django_json_logging.middleware.AccessLogMiddleware',
]
```
``` 
LOGGING = {
    ...
    'formatters': {"json": {'()': 'django_json_logging.logging.JSONFormatter'}},
    ...
}
```
