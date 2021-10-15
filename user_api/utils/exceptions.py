class ResourceNotFound(Exception):
    """Raised when a resource does not exist"""


class InvalidOrExpiredToken(Exception):
    """Raised on authorization error"""


class InvalidCredentials(Exception):
    """Raised on authentication error"""
