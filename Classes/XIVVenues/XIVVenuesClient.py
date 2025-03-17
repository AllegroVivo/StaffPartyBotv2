from __future__ import annotations

import os
from typing import TYPE_CHECKING, List, Optional

import requests
from dotenv import load_dotenv

from .XIVVenue import XIVVenue

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################

__all__ = ("XIVVenuesClient",)

################################################################################
class XIVVenuesClient:

    __slots__ = (
        "_state",
    )

    URL_BASE = "https://api.ffxivvenues.com/venue"

################################################################################
    def __init__(self, state: StaffPartyBot):

        self._state: StaffPartyBot = state

################################################################################
    def get_venues_by_manager(self, manager_id: int) -> List[XIVVenue]:

        query = self.URL_BASE + "?manager=" + str(manager_id)

        if self._state.DEBUG:
            print("Executing XIVClient query: " + query)

        response = requests.get(query)

        if response.status_code != 200:
            raise Exception(
                "Failed to get venue by manager - response status code: " +
                str(response.status_code)
            )

        if self._state.DEBUG:
            print("Response: " + str(response.json()))

        return [XIVVenue.from_data(venue) for venue in response.json()]

################################################################################
    def get_venue_by_id(self, _id: str) -> Optional[XIVVenue]:

        query = self.URL_BASE + f"/{_id}"

        if self._state.DEBUG:
            print("Executing XIVClient query: " + query)

        response = requests.get(query)

        if response.status_code != 200:
            raise Exception(
                "Failed to get venue by name - response status code: " +
                str(response.status_code)
            )

        if self._state.DEBUG:
            print("Response: " + str(response.json()))

        js = response.json()
        if "status" in js and js["status"] == 404:
            return None

        return XIVVenue.from_data(js)

################################################################################
    async def get_all_venues(self) -> List[XIVVenue]:

        query = self.URL_BASE

        load_dotenv()
        if os.getenv("DEBUG") == "True":
            print("Executing XIVClient query: " + query)

        response = requests.get(query)

        if response.status_code != 200:
            raise Exception(
                "Failed to get all venues - response status code: " +
                str(response.status_code)
            )

        ret = []

        for venue in response.json():
            ret.append(XIVVenue.from_data(venue))

        print(f"Returned {len(ret)} venues.")
        return ret

################################################################################
