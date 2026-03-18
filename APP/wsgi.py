"""
WSGI entry point for production servers (gunicorn).
"""

from app.main import create_app

app = create_app()
