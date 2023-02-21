from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, details: str = 'item not found'):
        HTTPException.__init__(self, status_code=404, detail=details)
