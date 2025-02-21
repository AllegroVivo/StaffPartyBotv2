from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Type, List

from . import Models

if TYPE_CHECKING:
    from Classes import *
    from Database import Database
################################################################################

__all__ = ("DatabaseUpdater",)

################################################################################
class DatabaseUpdater:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def _update_record(
        self,
        model_class: Type,
        data: Dict[str, Any],
        **identifiers: Any
    ) -> None:

        with self._parent._get_db() as db:
            query = db.query(model_class).filter_by(**identifiers)
            existing = query.first()

            if existing is None:
                raise ValueError(f"{model_class.__name__} not found with identifiers {identifiers}")

            try:
                for key, value in data.items():
                    setattr(existing, key, value)
                db.commit()
            except Exception as e:
                db.rollback()
                raise e

################################################################################
    def venue(self, v: Venue) -> None:

        self._update_record(Models.VenueModel, v.to_dict(), id=v.id)

################################################################################
    def venue_hours(self, vh: VenueHours) -> None:

        self._update_record(Models.VenueScheduleModel, vh.to_dict(), id=vh.id)

################################################################################
    def top_level(self, top_level_obj: Any) -> None:

        self._update_record(Models.TopLevelDataModel, top_level_obj.to_dict(), id=1)

################################################################################
