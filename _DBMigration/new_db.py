from __future__ import annotations

import os
import json
from datetime import date, time, datetime
from contextlib import contextmanager
from typing import Any, Tuple, Dict, Type, List, Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from Enums import *
from Database.Models import StaffProfileModel
from Models import *
################################################################################

__all__ = ("NewDatabaseManager", )

################################################################################
class NewDatabaseManager:

    __slots__ = (
        "_engine",
        "_session",
        "_pos_relations",
        "_profile_relations",
    )

################################################################################
    def __init__(self) -> None:

        load_dotenv()
        self._engine: Engine = create_engine(
            os.getenv("DEVELOPMENT_DATABASE_URL"),
            pool_size=10,
            max_overflow=0,
            pool_pre_ping=True,
            pool_timeout=30,
            pool_recycle=1800
        )
        self._session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        )

        self._pos_relations: Dict[str, int] = {}
        self._profile_relations: Dict[str, int] = {}

################################################################################
    @contextmanager
    def _get_db(self) -> Generator[Session | Any, Any, None]:

        db = self._session()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

################################################################################
    def _insert_all(self, _items: List[Any]) -> None:

        with self._get_db() as db:
            try:
                db.add_all(_items)
                db.commit()
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating {_items[0].__class__.__name__}: {str(e)}")

################################################################################
    def _insert_one(self, _item: Any) -> int:

        with self._get_db() as db:
            try:
                db.add(_item)
                db.commit()
                db.refresh(_item)
                if hasattr(_item, "id"):
                    return _item.id
                else:
                    return _item.user_id
            except IntegrityError as ex:
                db.rollback()
                print(f"IntegrityError... Examining records...")
                print(f"Error creating {_item.__class__.__name__}")
                match _item.__class__.__name__:
                    case "StaffProfileModel":
                        existing = db.query(StaffProfileModel).filter(StaffProfileModel.user_id == _item.user_id).first()
                        if not existing:
                            raise ex
                        print("Existing Profile Data:")
                        print(existing.__dict__)
                        print("New Profile Data:")
                        print(_item.__dict__)
                        choice = input("Which record do you want to keep? (New/Existing): ").lower().strip()
                        assert choice in ("new", "existing", "n", "e")
                        if choice in ("new", "n"):
                            print("Keeping new record...")
                            db.delete(existing)
                            db.commit()
                            db.add(_item)
                            db.commit()
                            db.refresh(_item)
                            return _item.user_id
                        else:
                            print("Keeping existing record...")
                            return existing.user_id
                    case _:
                        raise Exception(f"Undefined duplicate handling behavior for {_item.__class__.__name__}: {str(ex)}")
            except Exception as e:
                db.rollback()
                raise ValueError(f"Error creating {_item.__class__.__name__}: {str(e)}")

################################################################################
    def migrate_positions(self, payload: Dict[str, Any]) -> None:

        print("Caching positions...")

        position_data = payload["positions"]
        for pos in position_data:
            print(f"Saving position: {pos[2]}")
            pos_enum = Position.General_Training
            for member in Position:
                if member.proper_name == pos[2]:
                    pos_enum = member

            self._pos_relations[pos[0]] = pos_enum.value  # type: ignore

        print(f"{len(self._pos_relations)} position references cached.")

################################################################################
    def migrate_profiles(self, payload: Dict[str, Any]) -> None:

        print("Migrating profiles...")
        assert len(self._pos_relations) > 0

        profile_data = payload["profiles"]
        new_profiles = []
        for old_profile in profile_data:
            print(f"Saving profile: {old_profile['profile'][3]}")
            pdata = old_profile["profile"]
            old_profile_id = pdata[0]
            user_id = pdata[1]
            _ = pdata[2]  # Guild ID - not relevant
            user_name = pdata[3]
            custom_url = pdata[4]
            user_color = pdata[5]
            user_jobs = pdata[6] or []
            rates = pdata[7]
            post_url = pdata[8]
            old_pos_ids = pdata[9] or []
            dm_pref = pdata[10]
            likes = pdata[11] or []
            dislikes = pdata[12] or []
            personality = pdata[13]
            aboutme = pdata[14]
            gender = pdata[15]
            pronouns = pdata[16] or []
            race = pdata[17]
            clan = pdata[18]
            orientation = pdata[19]
            height = pdata[20]
            age = pdata[21]
            mare = pdata[22]
            data_center_ids = pdata[23] or []
            thumbnail_url = pdata[24]
            main_image_url = pdata[25]
            new_profile = StaffProfileModel(
                user_id=user_id,
                post_url=post_url,
                name=user_name,
                url=custom_url,
                color=user_color,
                jobs=user_jobs,
                rates=rates,
                position_ids=[self._pos_relations.get(p) for p in old_pos_ids],
                dm_pref=dm_pref,
                timezone="US/Eastern",
                gender=gender,
                pronouns=pronouns,
                race=race,
                clan=clan,
                orientation=orientation,
                height=height,
                age=age,
                mare=mare,
                data_centers=data_center_ids,
                likes=likes,
                dislikes=dislikes,
                personality=personality,
                about_me=aboutme,
                thumbnail_url=thumbnail_url,
                main_image_url=main_image_url
            )
            new_profile_id = self._insert_one(new_profile)
            self._profile_relations[old_profile_id] = new_profile_id
            new_profiles.append(new_profile_id)
            print(f"Profile saved: {new_profile_id}")

            old_availabilities = old_profile["availability"]
            new_avails = [ProfileAvailabilityModel(
                profile_id=new_profile_id,
                day=day,
                start_hour=start_time.hour,
                start_minute=start_time.minute,
                end_hour=end_time.hour,
                end_minute=end_time.minute
            ) for (_, day, start_time, end_time) in old_availabilities]
            self._insert_all(new_avails)
            print(f"Availabilities saved: {len(new_avails)}")

            addl_images = old_profile["additional_images"]
            new_addl_images = [ProfileAdditionalImageModel(
                profile_id=new_profile_id,
                url=url,
                caption=caption
            ) for (_, _, url, caption) in addl_images]
            self._insert_all(new_addl_images)
            print(f"Additional images saved: {len(new_addl_images)}")

        print(f"Profiles saved: {len(new_profiles)}")

################################################################################
    def migrate_venues(self, payload: Dict[str, Any]) -> None:

        print("Migrating venues...")
        assert len(self._pos_relations) > 0

        all_venues = payload["venues"]
        venues = []
        print(all_venues[0])
        for vdata in all_venues:
            v = vdata["venue"]
            print(f"Saving venue: {v[6]}")
            venue = VenueModel(
                xiv_id=v[12],
                name=v[6],
                description=v[7],
                mare_id=v[9],
                mare_password=v[10],
                hiring=v[8],
                nsfw=v[22],
                data_center=v[13],
                world=v[14],
                zone=v[15],
                ward=v[16],
                plot=v[17],
                apartment=v[18],
                room=v[19],
                subdivision=v[20],
                rp_level=v[21],
                tags=v[24],
                user_ids=v[2],
                position_ids=[self._pos_relations.get(p) for p in v[3]],
                mute_ids=v[11],
                discord_url=v[25],
                website_url=v[26],
                banner_url=v[27],
                logo_url=v[28],
                app_url=v[29],
                post_url=v[5]
            )
            new_venue_id = self._insert_one(venue)
            venues.append(new_venue_id)
            print(f"Venue saved: {v[6]}")

            print("Converting venue hours...")
            h = vdata["hours"]
            new_hours = [VenueScheduleModel(
                venue_id=new_venue_id,
                day=day,
                start_hour=start_time.hour,
                start_minute=start_time.minute,
                end_hour=end_time.hour,
                end_minute=end_time.minute,
                interval_type=interval_type,
                interval_arg=interval_arg
            ) for (_, _, day, start_time, end_time, interval_type, interval_arg) in h]
            self._insert_all(new_hours)

            print(f"Venue hours saved: {len(new_hours)}")

        print(f"Venues saved: {len(venues)}")

################################################################################
    def migrate_bg_checks(self, payload: Dict[str, Any]) -> None:

        bg_check_data = payload["bg_checks"]
        for old_bg_check in bg_check_data:
            user_id = old_bg_check[0]
            print(f"Saving background check for: {old_bg_check[2]} ({user_id})")
            bg_check = BGCheckModel(
                user_id=user_id,
                agree=old_bg_check[1],
                names=old_bg_check[2],
                approved=old_bg_check[5],
                post_url=old_bg_check[9],
                submitted_at=old_bg_check[10],
                approved_at=old_bg_check[11],
                approved_by=old_bg_check[12],
            )
            new_bg_check_id = self._insert_one(bg_check)
            print(f"Background check saved: {old_bg_check[2]} ({user_id})")

            print("Converting venues...")
            old_bg_check_venues = old_bg_check[3]

            if old_bg_check_venues:
                venues = []
                for old_venue in old_bg_check_venues:
                    name, dc, world, jobs = old_venue.split("::")
                    new_venue = BGCheckVenueModel(
                        bg_check_id=new_bg_check_id,
                        name=name,
                        data_center=dc,
                        world=world,
                        jobs=jobs.split("||")
                    )
                    venues.append(new_venue)

                self._insert_all(venues)
                print(f"Venues converted: {len(venues)}")
            else:
                print("No venues to convert...")

        print(f"Background checks saved: {len(bg_check_data)}")

################################################################################
