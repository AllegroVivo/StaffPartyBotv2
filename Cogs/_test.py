import json
from typing import TYPE_CHECKING

from Classes.Venues.Venue import Venue
from Classes.XIVVenues.XIVVenue import XIVVenue

if TYPE_CHECKING:
    from Classes import StaffPartyBot
################################################################################
async def test_api_data_parsing(bot: "StaffPartyBot") -> None:
    """
    Tests if all records in API data can be successfully parsed into XIVVenue objects.

    :param api_data: List of venue dictionaries from API response.
    :return: Summary dictionary containing the number of successes and failures.
    """
    successful = 0
    failures = []
    hours_ids = []
    venues = []

    with open("C:/Dev/Python/StaffPartyBotv2/Classes/XIVVenues/_test_data.json", "r", encoding="utf-8") as file:
        api_data = json.load(file)

    for index, record in enumerate(api_data):
        try:
            xiv = XIVVenue.from_data(record)
            venue = Venue.new(bot.venue_manager, xiv, hours_ids, venues)
            _ = await venue.status()
            successful += 1
            venues.append(venue)
            hours_ids.extend([sch.id for sch in venue._schedule])
            print(f"Successfully parsed record {index + 1} - {record['name']}")
        except Exception as e:
            raise
            # failures.append({"index": index, "error": str(e), "data": record})

    ret = {
        "total_records": len(api_data),
        "successful_parses": successful,
        "failed_parses": len(failures),
        "failures": failures
    }

    with open("C:/Dev/Python/StaffPartyBotv2/Classes/XIVVenues/test_results.json", "w", encoding="utf-8") as outfile:
        json.dump(ret, outfile, indent=2, ensure_ascii=False)  # type: ignore

################################################################################
def setup(_) -> None:

    pass

################################################################################
