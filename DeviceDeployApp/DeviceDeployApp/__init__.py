"""
The flask application package.
"""

from flask import Flask, render_template

app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Make a random secret key from Django Documentation
# https://docs.djangoproject.com/en/dev/ref/settings/

app.secret_key = 'this should be a secret key'

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Could not find what you were looking for', 404
@app.errorhandler(500)
def not_found(error):
    return 'Error 500: Nothing shows up', 500

from DeviceDeployApp.views import *
