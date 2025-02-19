from __future__ import annotations

from typing import TYPE_CHECKING, Type

from . import Models

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseDeleter",)

################################################################################
class DatabaseDeleter:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def _delete_record(self, model_class: Type, _id: int) -> None:

        with self._parent._get_db() as db:
            try:
                # Query and delete all matching records
                query = db.query(model_class).filter(model_class.id == _id)  # type: ignore
                deleted_count = query.delete(synchronize_session=False)

                if deleted_count == 0:
                    raise ValueError(f"{model_class.__name__} with ID {_id} not found")

                db.commit()
            except Exception as e:
                db.rollback()
                raise e

################################################################################
