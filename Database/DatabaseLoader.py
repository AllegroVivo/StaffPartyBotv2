from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict, Any
from sqlalchemy.orm import selectinload

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseLoader",)

################################################################################
class DatabaseLoader:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def check_guild(self, guild_id: int) -> bool:

        with self._parent._get_db() as db:
            try:
                guild = db.query(GuildIDModel).filter(GuildIDModel.id == guild_id).first()
            except Exception as e:
                print(e)
                return False

            return guild is not None

################################################################################
    def load_guilds(self) -> List[Dict[str, Any]]:

        with self._parent._get_db() as db:
            try:
                guilds = db.query(GuildIDModel).options(

                ).all()
            except Exception as e:
                print(e)
                return MasterResponseSchema(root=[]).model_dump()

            guild_datas = []
            for guild in guilds:
                guild_datas.append(
                    TopLevelGuildSchema(
                        id=guild.guild_id,
                        data=GuildDataSchema(

                        )
                    )
                )

            return MasterResponseSchema(root=guild_datas).model_dump()

################################################################################
