from location.constant.geocodes import GeoCodes


class LocationService:

    def parse_location(self, given_location: str) -> int | None:
        search_location = given_location.upper().strip().replace(' ','_')
        for geocode in GeoCodes:
            if search_location == geocode.name:
                return geocode.value
        return None
    
