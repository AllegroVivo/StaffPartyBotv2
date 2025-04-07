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
    def venue_hours(self, hours_id: int) -> None:

        self._delete_record(Models.VenueScheduleModel, hours_id)

################################################################################
    def requirement(self, req_id: int) -> None:

        self._delete_record(Models.RequirementModel, req_id)

################################################################################
    def bg_check_venue(self, venue_id: int) -> None:

        self._delete_record(Models.BGCheckVenueModel, venue_id)

################################################################################
    def venue(self, venue_id: int) -> None:

        self._delete_record(Models.VenueModel, venue_id)

################################################################################
    def additional_image(self, image_id: int) -> None:

        self._delete_record(Models.ProfileAdditionalImageModel, image_id)

################################################################################
    def profile(self, profile_id: int) -> None:

        self._delete_record(Models.StaffProfileModel, profile_id)

################################################################################
    def profile_availability(self, avail_id: int) -> None:

        self._delete_record(Models.ProfileAvailabilityModel, avail_id)

################################################################################
    def temporary_job(self, job_id: int) -> None:

        self._delete_record(Models.TemporaryJobPostingModel, job_id)

################################################################################
    def permanent_job(self, job_id: int) -> None:

        self._delete_record(Models.PermanentJobPostingModel, job_id)

################################################################################
    def dj_profile_availability(self, avail_id: int) -> None:

        self._delete_record(Models.DJProfileAvailabilityModel, avail_id)

################################################################################
