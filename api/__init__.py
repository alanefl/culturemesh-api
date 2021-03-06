from flask import Flask
from .decorators import require_apikey
from .credentials import sql
from .extensions import mysql


api = Flask(__name__)
# Add MYSQL Database settings from super safe credentials file off of Version Control.
for setting in sql:
    api.config[setting] = sql[setting]
mysql.init_app(api)


# Register API submodules (aka blueprints)

from api.blueprints.users.controllers import users
from api.blueprints.networks.controllers import networks
from api.blueprints.posts.controllers import posts
from api.blueprints.events.controllers import events
from api.blueprints.locations.controllers import locations
from api.blueprints.languages.controllers import languages
from api.blueprints.accounts.controllers import accounts
from api.blueprints.upload.controllers import upload


api.register_blueprint(users, url_prefix='/user')
api.register_blueprint(networks, url_prefix='/network')
api.register_blueprint(posts, url_prefix='/post')
api.register_blueprint(events, url_prefix='/event')
api.register_blueprint(locations, url_prefix='/location')
api.register_blueprint(languages, url_prefix='/language')
api.register_blueprint(accounts, url_prefix='/account')
api.register_blueprint(upload, url_prefix='/upload')

@api.after_request
def add_custom_http_response_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=86400; includeSubDomains"
    response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-CultureMesh"] = "API"
    return response
