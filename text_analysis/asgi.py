"""
ASGI config for text_analysis project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
=======
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
>>>>>>> 4ad03e5 (first commit)
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'text_analysis.settings')

application = get_asgi_application()
