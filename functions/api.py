import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from app import app as flask_app
from serverless_wsgi import handle_request

def handler(event, context):
    return handle_request(flask_app, event, context)
