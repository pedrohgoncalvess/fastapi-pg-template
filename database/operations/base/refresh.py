from typing import Optional

from sqlalchemy import select, delete

from database.models.base import Refresh
from database.operations import Interface


class RefreshRepository(Interface[Refresh]):
    def __init__(self, db):
        super().__init__(Refresh, db)

    async def find_by_token(self, token: str) -> Optional[Refresh]:
        result = await self.db.execute(
            select(self.model).filter(self.model.token == token)
        )
        return result.scalar_one_or_none()

    async def delete_by_token(self, token: str) -> bool:
        refresh = await self.find_by_token(token)
        if not refresh:
            return False
        await self.db.delete(refresh)
        return True

    async def delete_by_user_id(self, user_id: int) -> None:
        await self.db.execute(
            delete(self.model).where(self.model.user_id == user_id)
        )