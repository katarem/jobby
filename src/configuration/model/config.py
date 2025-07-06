from dataclasses import dataclass

@dataclass
class Config:
    title: str
    pages: int
    search_location: str
    filter_locations: list[str]
    keywords: list[str]
    card_template: str = ''
    card_language: str = 'en'
    card_name: str = ''