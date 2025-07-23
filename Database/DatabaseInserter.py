from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Any, Dict

from discord import Guild

from .Models import *
from .Schemas import *

if TYPE_CHECKING:
    from Database import Database
################################################################################

__all__ = ("DatabaseInserter", )

################################################################################
class DatabaseInserter:

    __slots__ = (
        "_parent",
    )

################################################################################
    def __init__(self, parent: Database):

        self._parent = parent

################################################################################
    def guild(self, guild: Guild) -> None:

        with self._parent._get_db() as db:
            gid = guild.id
            query = db.query(GuildIDModel).filter(GuildIDModel.id == gid)
            existing = query.first()

            if existing is not None:
                raise ValueError(f"Guild {gid} already exists in the database.")

            try:
                new_guild = GuildIDModel(id=gid)
                db.add(new_guild)
                db.commit()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating guild: {str(e)}")

################################################################################
    def venue(self, xiv_id: str, name: str) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            query = db.query(VenueModel).filter(VenueModel.xiv_id == xiv_id)
            existing = query.first()

            if existing is not None:
                raise ValueError(f"Venue with XIV ID '{xiv_id}' already exists in the database.")

            try:
                new_venue = VenueModel(xiv_id=xiv_id, name=name)
                db.add(new_venue)
                db.commit()
                db.refresh(new_venue)
                return VenueSchema.model_validate(new_venue).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating venue: {str(e)}")

################################################################################
    def venue_schedule(self, venue_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_schedule = VenueScheduleModel(venue_id=venue_id)
                db.add(new_schedule)
                db.commit()
                db.refresh(new_schedule)
                return VenueScheduleSchema.model_validate(new_schedule).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating venue schedule: {str(e)}")

################################################################################
    def bg_check(self, user_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_bg = BGCheckModel(user_id=user_id)
                db.add(new_bg)
                db.commit()
                db.refresh(new_bg)
                return BGCheckSchema.model_validate(new_bg).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating background check: {str(e)}")

################################################################################
    def bg_check_venue(self, parent_id: int, name: str, data_center: int, world: int, jobs: List[str]) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_bg_venue = BGCheckVenueModel(
                    bg_check_id=parent_id,
                    name=name,
                    data_center=data_center,
                    world=world,
                    jobs=jobs
                )
                db.add(new_bg_venue)
                db.commit()
                db.refresh(new_bg_venue)
                return BGCheckVenueSchema.model_validate(new_bg_venue).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating background check venue: {str(e)}")

################################################################################
    def availability(
        self,
        profile_id: int,
        day: int,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_avail = ProfileAvailabilityModel(
                    profile_id=profile_id,
                    day=day,
                    start_hour=start_hour,
                    start_minute=start_minute,
                    end_hour=end_hour,
                    end_minute=end_minute
                )
                db.add(new_avail)
                db.commit()
                db.refresh(new_avail)
                return ProfileAvailabilitySchema.model_validate(new_avail).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating profile availability: {str(e)}")

################################################################################
    def additional_image(self, profile_id: int, url: str, caption: Optional[str]) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_img = ProfileAdditionalImageModel(profile_id=profile_id, url=url, caption=caption)
                db.add(new_img)
                db.commit()
                db.refresh(new_img)
                return AdditionalImageSchema.model_validate(new_img).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating additional image: {str(e)}")

################################################################################
    def profile(self, user_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_profile = StaffProfileModel(user_id=user_id)
                db.add(new_profile)
                db.commit()
                db.refresh(new_profile)
                return StaffProfileSchema.model_validate(new_profile).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating profile: {str(e)}")

################################################################################
    def temporary_job(
        self,
        venue_id: int,
        user_id: int,
        position_id: int,
        description: str,
        salary: str,
        start_dt: datetime,
        end_dt: datetime,
        genres: List[int]
    ) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_job = TemporaryJobPostingModel(
                    venue_id=venue_id,
                    user_id=user_id,
                    position_id=position_id,
                    description=description,
                    salary=salary,
                    start_dt=start_dt,
                    end_dt=end_dt,
                    genres=genres
                )
                db.add(new_job)
                db.commit()
                db.refresh(new_job)
                return TemporaryJobPostingSchema.model_validate(new_job).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating temporary job: {str(e)}")

################################################################################
    def permanent_job(
        self,
        venue_id: int,
        user_id: int,
        position: int,
        descr: str,
        salary: Optional[str]
    ) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_job = PermanentJobPostingModel(
                    venue_id=venue_id,
                    user_id=user_id,
                    position_id=position,
                    description=descr,
                    salary=salary
                )
                db.add(new_job)
                db.commit()
                db.refresh(new_job)
                return PermanentJobPostingSchema.model_validate(new_job).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating permanent job: {str(e)}")

################################################################################
    def dj_profile(self, user_id: int) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_dj = DJProfileModel(user_id=user_id)
                db.add(new_dj)
                db.commit()
                db.refresh(new_dj)
                return DJProfileSchema.model_validate(new_dj).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating DJ profile: {str(e)}")

################################################################################
    def dj_availability(
        self,
        profile_id: int,
        day: int,
        start_hour: int,
        start_minute: int,
        end_hour: int,
        end_minute: int
    ) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_avail = DJProfileAvailabilityModel(
                    profile_id=profile_id,
                    day=day,
                    start_hour=start_hour,
                    start_minute=start_minute,
                    end_hour=end_hour,
                    end_minute=end_minute
                )
                db.add(new_avail)
                db.commit()
                db.refresh(new_avail)
                return DJAvailabilitySchema.model_validate(new_avail).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating dj availability: {str(e)}")

################################################################################
    def special_event(
        self,
        venue_id: int,
        title: str,
        description: Optional[str],
        location: Optional[str],
        start: Optional[str],
        length: Optional[str],
        links: List[str],
        requirements: Optional[str]
    ) -> Dict[str, Any]:

        with self._parent._get_db() as db:
            try:
                new_event = SpecialEventModel(
                    venue_id=venue_id,
                    title=title,
                    description=description,
                    location=location,
                    start=start,
                    length=length,
                    links=links,
                    requirements=requirements
                )
                db.add(new_event)
                db.commit()
                db.refresh(new_event)
                return SpecialEventSchema.model_validate(new_event).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating special event: {str(e)}")

################################################################################
    def service_request(
        self,
        user_id: int,
        service: int,
        dc: Optional[int],
        description: Optional[str],
        budget: Optional[str],
    ):

        with self._parent._get_db() as db:
            try:
                new_request = ServiceRequestModel(
                    user_id=user_id,
                    service=service,
                    dc=dc,
                    description=description,
                    budget=budget
                )
                db.add(new_request)
                db.commit()
                db.refresh(new_request)
                return ServiceRequestSchema.model_validate(new_request).model_dump()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating service request: {str(e)}")

################################################################################
