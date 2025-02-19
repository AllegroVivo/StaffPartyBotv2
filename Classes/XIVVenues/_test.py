import json
from typing import List, Dict, Any
from Classes.XIVVenues.XIVVenue import XIVVenue  # Ensure correct import path
################################################################################
def test_api_data_parsing(api_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Tests if all records in API data can be successfully parsed into XIVVenue objects.

    :param api_data: List of venue dictionaries from API response.
    :return: Summary dictionary containing the number of successes and failures.
    """
    successful = 0
    failures = []

    for index, record in enumerate(api_data):
        try:
            _ = XIVVenue.from_data(record)
            successful += 1
        except Exception as e:
            failures.append({"index": index, "error": str(e), "data": record})

    return {
        "total_records": len(api_data),
        "successful_parses": successful,
        "failed_parses": len(failures),
        "failures": failures
    }

################################################################################
if __name__ == "__main__":
    with open("C:/Python/StaffPartyBotv2/Classes/XIVVenues/data.json", "r", encoding="utf-8") as file:
        api_data = json.load(file)

    result = test_api_data_parsing(api_data)
    with open("C:/Python/StaffPartyBotv2/Classes/XIVVenues/test_results.json", "w", encoding="utf-8") as outfile:
        json.dump(result, outfile, indent=2, ensure_ascii=False)  # type: ignore
