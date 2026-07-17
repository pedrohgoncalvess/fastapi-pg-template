from typing import Optional

from starlette import status


class DomainError(Exception):
    """Base class for business-rule errors, translated to HTTP by the handler in main.py."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Domain error."
    headers: Optional[dict] = None

    def __init__(self, detail: Optional[str] = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class EmailAlreadyRegistered(DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Email already registered."


class InvalidCredentials(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Email or password incorrect."
    headers = {"WWW-Authenticate": "Bearer"}


class UserNotVerified(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User must be verified."


class InvalidRefreshToken(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid refresh token."


class RefreshTokenExpired(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Refresh token expired."


class OldPasswordRequired(DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "old_password is required to set a new password."


class OldPasswordIncorrect(DomainError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Old password incorrect."


class NothingToUpdate(DomainError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "No fields to update."
