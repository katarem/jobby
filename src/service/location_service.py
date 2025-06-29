from constant.geocodes import GeoCodes


class LocationService:

    def parse_location(self, given_location: str) -> str | None:
        search_location = given_location.upper().strip().replace(' ','_')
        for geocode in GeoCodes:
            if search_location in geocode.name:
                return geocode.value
        return None
    
