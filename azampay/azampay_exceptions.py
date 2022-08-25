class InvalidCredentials(Exception):
    """
    This exception will be thrown when credentials entered by developer is invalid

    Invalid means the response object came with status code of 423
    """

    error_message: str = """
    Looks like you you're credentials are invalid
    
    Please have a closer look at credentials you specified
    
    And then try again, If it is persist please contact the azampay personel for further assistance   
    """

    def __init__(self, error_message=error_message) -> None:
        super().__init__(error_message)


class BadRequest(Exception):
    """
    BadRequest

    This exception will be raised when you have sent an invalid request to the server side

    And most likely is due to the fact your required JSON data does not match the JSON response you sent
    """

    error_message: str = """
    Ooops, Your request could not be processed 
    
    Mostly likely you're request body is invalid
    
    Please read the docs and fix the body and then try again later.    
    """

    def __init__(self, error_message) -> None:
        super().__init__(error_message)


class InternalServerError(Exception):
    """
    This exception is raised when there was an internal errror on server side
    while processing your request.py

    This will be indicated when response object came with status code of 500
    """

    error_message: str = """
    Oops, Sorry, We are experiencing an issue on the side
    
    We are apologize for any inconvinience we have caused you
    
    Please come back a bilt later while we work had to fix this
    """

    def __init__(self, error_message=error_message) -> None:
        super().__init__(error_message)
