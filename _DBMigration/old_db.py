from __future__ import annotations

import psycopg2
import os
from dotenv import load_dotenv
from typing import TYPE_CHECKING, Any, Dict, Tuple

if TYPE_CHECKING:
    pass
################################################################################

__all__ = ("OldDatabaseLoader",)

################################################################################
class OldDatabaseLoader:
    """A utility class for loading data from the database."""

    def __init__(self):

        self._connection: connection = None  # type: ignore
        self._cursor: cursor = None  # type: ignore

################################################################################
    def _connect(self) -> None:

        load_dotenv()

        self._reset_connection()
        self._connection = psycopg2.connect(os.getenv("OLD_DB_URL"), sslmode="require")

        self._cursor = self._connection.cursor()

        print("Connecting to database")

################################################################################
    def _reset_connection(self) -> None:

        try:
            self._cursor.close()
            self._connection.close()
        except:
            pass
        finally:
            self._connection = None
            self._cursor = None

################################################################################
    def _get_all_data(self) -> Dict[str, Any]:
        """Performs all sub-loaders and returns a dictionary of their results."""

        return {
            "bot_config": self._load_bot_config(),
            "positions" : self._load_positions(),
            "requirements" : self._load_requirements(),
            "tusers" : self._load_tusers(),
            "availability" : self._load_availability(),
            "qualifications" : self._load_qualifications(),
            "trainings" : self._load_trainings(),
            "requirement_overrides" : self._load_requirement_overrides(),
            "profiles" : self._load_profiles(),
            "additional_images" : self._load_additional_images(),
            "venues" : self._load_venues(),
            "venue_hours" : self._load_venue_hours(),
            "job_postings" : self._load_job_postings(),
            "hours" : self._load_job_hours(),
            "bg_checks" : self._load_bg_checks(),
            "roles" : self._load_roles(),
            "channels": self._load_channels(),
            "profile_availability" : self._load_profile_availability(),
            "service_configs" : self._load_service_configs(),
            "service_profiles" : self._load_service_profiles(),
            "services" : self._load_services(),
            "sp_availability" : self._load_sp_availability(),
            "sp_images" : self._load_sp_images(),
            "group_trainings": self._load_group_trainings(),
            "group_training_signups": self._load_group_training_signups(),
        }

################################################################################
    def load_all(self) -> Dict[int, Dict[str, Any]]:

        data = self._get_all_data()

        # Set up the return dictionary.
        ret = { g_id : {
            "bot_config": None,
            "tusers": [],
            "availability": [],
            "qualifications": [],
            "positions": [],
            "requirements": [],
            "trainings": [],
            "requirement_overrides": [],
            "profiles": [],
            "venues": [],
            "job_postings": {},
            "bg_checks": [],
            "roles": None,
            "channels": None,
            "services": [],
            "service_profiles": [],
            "group_trainings": [],
        } for g_id in [cfg[0] for cfg in data["bot_config"]] }

        load_dotenv()

        ### Bot Config ###
        for cfg in data["bot_config"]:
            ret[cfg[0]]["bot_config"] = cfg
        for r in data["roles"]:
            ret[r[0]]["roles"] = r
        for c in data["channels"]:
            ret[c[0]]["channels"] = c

        ### Training ###
        for u in data["tusers"]:
            ret[u[1]]["tusers"].append(u)
        for a in data["availability"]:
            ret[a[1]]["availability"].append(a)
        for q in data["qualifications"]:
            ret[q[1]]["qualifications"].append(q)
        for p in data["positions"]:
            ret[p[1]]["positions"].append(p)
        for r in data["requirements"]:
            ret[r[1]]["requirements"].append(r)
        for t in data["trainings"]:
            ret[t[1]]["trainings"].append(t)
        for ro in data["requirement_overrides"]:
            ret[ro[1]]["requirement_overrides"].append(ro)
        for bg in data["bg_checks"]:
            ret[bg[6]]["bg_checks"].append(bg)

        ### Profiles ###
        for p in data["profiles"]:
            ret[p[2]]["profiles"].append(
                {
                    "profile": p,
                    "additional_images": [
                        a for a in data["additional_images"] if a[1] == p[0]
                    ],
                    "availability": [
                        prof for prof in data["profile_availability"]
                        if prof[0] == p[0]
                    ]
                }
            )

        ### Venues ###
        for v in data["venues"]:
            ret[v[1]]["venues"].append(
                {
                    "venue": v,
                    "hours": [],
                }
            )
        for vh in data["venue_hours"]:
            for v in ret[vh[1]]["venues"]:
                if v["venue"][0] == vh[0]:
                    v["hours"].append(vh)

        ### Job Postings ###
        for jp in data["job_postings"]:
            ret[jp[1]]["job_postings"][jp[0]] = {
                "data": jp,
                "hours": [],
            }
        for jpa in data["hours"]:
            ret[jpa[1]]["job_postings"][jpa[0]]["hours"].append(jpa)  # type: ignore

        ### Services ###
        for s in data["services"]:
            sconfig = None
            for scfg in data["service_configs"]:
                if scfg[0] == s[0]:
                    sconfig = scfg

            ret[s[1]]["services"].append(
                {
                    "service": s,
                    "config": sconfig
                }
            )
        for sp in data["service_profiles"]:
            ret[sp[1]]["service_profiles"].append(
                {
                    "profile": sp,
                    "availability": [
                        avail for avail in data["sp_availability"]
                        if avail[0] == sp[0]
                    ],
                    "images": [
                        img for img in data["sp_images"]
                        if img[1] == sp[0]
                    ]
                }
            )

        ### Group Trainings ###
        for gt in data["group_trainings"]:
            ret[gt[1]]["group_trainings"].append(
                {
                    "training": gt,
                    "signups": [
                        gts for gts in data["group_training_signups"]
                        if gts[1] == gt[0]
                    ]
                }
            )

        return ret

################################################################################
    def execute(self, query: str, *fmt_args: Any) -> None:

        try:
            self._cursor.execute("SELECT 1")
        except:
            self._connect()

        load_dotenv()

        try:
            self._cursor.execute(query, fmt_args)
            self._connection.commit()
            if os.getenv("DEBUG") == "True":
                print(f"Database execution succeeded on query: '{query}', Args: {fmt_args}")
        except:
            print(f"Database execution failed on query: '{query}', Args: {fmt_args}")

################################################################################
    def fetchall(self) -> Tuple[Tuple[Any, ...]]:

        return self._cursor.fetchall()

################################################################################
    def fetchone(self) -> Tuple[Any, ...]:

        return self._cursor.fetchone()

################################################################################
    def _load_bot_config(self) -> Tuple[Any, ...]:
        
        self.execute("SELECT * FROM bot_config;")
        return self.fetchall()
        
################################################################################
    def _load_positions(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM positions;")
        return self.fetchall()
    
################################################################################
    def _load_requirements(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM requirements;")
        return self.fetchall()
    
################################################################################
    def _load_tusers(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM tuser_master;")
        return self.fetchall()
    
################################################################################
    def _load_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM availability;")
        return self.fetchall()
    
################################################################################
    def _load_qualifications(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM qualifications;")
        return self.fetchall()
    
################################################################################
    def _load_trainings(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM trainings;")
        return self.fetchall()
    
################################################################################
    def _load_requirement_overrides(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM requirement_overrides;")
        return self.fetchall()
    
################################################################################
    def _load_profiles(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM profile_master;")
        return self.fetchall()

################################################################################
    def _load_additional_images(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM additional_images;")
        return self.fetchall()
    
################################################################################
    def _load_venues(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_master;")
        return self.fetchall()
    
################################################################################
    def _load_venue_hours(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM venue_hours;")
        return self.fetchall()
    
################################################################################
    def _load_job_postings(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM job_postings;")
        return self.fetchall()
    
################################################################################
    def _load_job_hours(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM job_hours;")
        return self.fetchall()
    
################################################################################
    def _load_bg_checks(self) -> Tuple[Tuple[Any, ...], ...]:

        self.execute("SELECT * FROM bg_checks;")
        return self.fetchall()
    
################################################################################
    def _load_roles(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM roles;")
        return self.fetchall()
    
################################################################################
    def _load_channels(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM channels;")
        return self.fetchall()
    
################################################################################
    def _load_profile_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM profile_availability;")
        return self.fetchall()
    
################################################################################
    def _load_service_configs(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM service_config;")
        return self.fetchall()
    
################################################################################
    def _load_service_profiles(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM service_profiles;")
        return self.fetchall()
    
################################################################################
    def _load_services(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM services;")
        return self.fetchall()
    
################################################################################
    def _load_sp_availability(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM sp_availability;")
        return self.fetchall()
    
################################################################################
    def _load_sp_images(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM sp_images;")
        return self.fetchall()
    
################################################################################
    def _load_group_trainings(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM group_trainings;")
        return self.fetchall()
    
################################################################################
    def _load_group_training_signups(self) -> Tuple[Tuple[Any, ...], ...]:
        
        self.execute("SELECT * FROM group_training_signups;")
        return self.fetchall()
    
################################################################################
