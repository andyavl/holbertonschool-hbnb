from flask_jwt_extended import get_jwt

def is_admin():
    """Returns True if the current JWT has admin privileges."""
    return get_jwt().get('is_admin', False)
