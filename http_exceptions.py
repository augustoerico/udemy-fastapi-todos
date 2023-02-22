from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, details: str = 'item not found'):
        HTTPException.__init__(self, status_code=status.HTTP_404_NOT_FOUND, detail=details)


class UnauthorizedException(HTTPException):
    def __init__(self, details: str = 'Unauthorized'):
        HTTPException.__init__(self, status_code=status.HTTP_401_UNAUTHORIZED, detail=details)
