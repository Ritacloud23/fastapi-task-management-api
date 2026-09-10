from typing import Annotated

from fastapi import Depends, HTTPException, Query
from fastapi.security import APIKeyHeader
from sqlmodel import Session

from database import get_session

# Database dependency
SessionDep = Annotated[
    Session,
    Depends(get_session),
]



API_KEY = "my-secret-key"

api_key_header = APIKeyHeader(
    name="X-API-Key"
)


def require_api_key(
    api_key: str = Depends(api_key_header),
):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
        )

    return api_key


APIKeyDep = Annotated[
    str,
    Depends(require_api_key),
]


# Pagination dependency
class PaginationParams:
    def __init__(
        self,
        offset: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
    ):
        self.offset = offset
        self.limit = limit


PaginationDep = Annotated[
    PaginationParams,
    Depends(),
]