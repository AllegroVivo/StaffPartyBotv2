from __future__ import annotations

import os
from typing import TYPE_CHECKING, List

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

    load_dotenv()
    DEBUG = os.getenv("DEBUG") == "True"

    if DEBUG:
        # URL_BASE = "https://api.ffxivvenues.dev/venue"
        URL_BASE = "https://api.ffxivvenues.com/venue"
    else:
        URL_BASE = "https://api.ffxivvenues.com/venue"

################################################################################
    def __init__(self, state: StaffPartyBot):

        self._state: StaffPartyBot = state

################################################################################
    async def get_venues_by_manager(self, manager_id: int) -> List[XIVVenue]:

        query = self.URL_BASE + "?manager=" + str(manager_id)

        if self.DEBUG:
            print("Executing XIVClient query: " + query)

        response = requests.get(query)

        if response.status_code != 200:
            raise Exception(
                "Failed to get venue by manager - response status code: " +
                str(response.status_code)
            )

        if self.DEBUG:
            print("Response: " + str(response.json()))

        return [XIVVenue.from_data(venue) for venue in response.json()]

################################################################################
    async def get_venues_by_name(self, name: str) -> List[XIVVenue]:

        query = self.URL_BASE + "?search=" + str(name)

        load_dotenv()
        if os.getenv("DEBUG") == "True":
            print("Executing XIVClient query: " + query)

        response = requests.get(query)

        if response.status_code != 200:
            raise Exception(
                "Failed to get venue by name - response status code: " +
                str(response.status_code)
            )

        if os.getenv("DEBUG") == "True":
            print("Response: " + str(response.json()))

        ret = []

        for venue in response.json():
            ret.append(XIVVenue.from_data(venue))

        return ret

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
