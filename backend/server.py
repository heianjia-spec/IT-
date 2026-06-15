#!/usr/bin/env python
"""Standalone WSGI server for Django backend."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server

application = get_wsgi_application()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9000
    with make_server('127.0.0.1', port, application) as httpd:
        print(f'Backend running at http://127.0.0.1:{port}/')
        httpd.serve_forever()
