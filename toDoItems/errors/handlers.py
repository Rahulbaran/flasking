from flask import Blueprint, render_template

errors = Blueprint('handlers', __name__)


@errors.app_errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Page not found', heading='Oops!',
    content='Sorry the page you are looking for, is not available'), 404


@errors.app_errorhandler(403)
def not_allowed(e):
    return render_template('error.html', title='Not Allowed', heading='Oops!', 
    content='You are not authorised to access the page'), 403


@errors.app_errorhandler(500)
def server_error(e):
    return render_template('error.html', title='Server Side Error', heading='Sorry!', 
    content='We are experiencing some troubles please try again after some time'), 500


@errors.app_errorhandler(413)
def too_large(e):
    return render_template('error.html', title='Too Large Entity', heading='Too large!',
    content='Uploaded file is too large(must be in size upto 2MB)'), 413


@errors.app_errorhandler(410)
def page_not_found(e):
    return render_template('error.html', title='Page not found', heading='Oops!',
    content='Sorry the page you are looking for, is not available'), 410


@errors.app_errorhandler(503)
def too_large(e):
    return render_template('error.html', title='Service Unavailable', heading='Sorry!',
    content='Right now our service is unavailable, Please try again later'), 503