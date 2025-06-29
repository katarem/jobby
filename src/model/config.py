from dataclasses import dataclass

@dataclass
class Config:
    title: str
    search_location: str
    filter_locations: list[str]
    keywords: list[str]