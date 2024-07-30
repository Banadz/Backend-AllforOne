"""
ASGI config for fullBack project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from fastapi import FastAPI
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from fastapi.responses import HTMLResponse
import uvicorn

# Importez ici votre application FastAPI
from fullBack.fastapi_app import app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fullBack.settings')

# Exposez votre application FastAPI comme point d'entrée ASGI
application = app
