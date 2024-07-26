# constants.py
from enum import Enum


class Constants:
    """
    Application Constants.
    """

    ACTION_RESULT = "result"
    ACTION_STATUS = "execution_status"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    RESPONSE_TYPE_TEXT = "text"
    RESPONSE_TYPE_CONTENT = "content"
    LOGOUT_SUCCESSFUL = "Logout successful"
    MESSAGE = "message"
    STATUS_CODE = "status_code"
    AUTH_SUCCESSFUL = "Authentication successful"
    AUTH_ERROR = "Error in authentication"
    RESPONSE = "response"
    CREDENTIALS_VALID = "Credentials valid and can perform API calls"


class ErrorMessage:
    """
    Connector Error Messages.
    """

    SERVER_ERROR = "A server side error, check configuration and try again or Contact CSOL administrator for further details."
    LOGOUT = "Logout from authenticated session success"
    NO_DATA_RETURNED = "No content returned"
    INVALID_METHOD = "Invalid method requested !"
    ERROR_IN_GET = "Error occurred in get action"
    AUTH_FAILED = "Authentication failed"
    CONNECTION_FAILED_ERROR = "Connection could not be made to the server"
    JSON_RESPONSE_NOT_FOUND = 'JSON response was not found'


class HttpMethods(Enum):
    """
    HTTP methods
    """
    GET = "GET"
    PUT = "PUT"
    POST = "POST"
    DELETE = "DELETE"
    PATCH = "PATCH"
