class ExtractionService:

    def __init__(self, keywords: list[str]):
        self.keywords = keywords

    def detect_keywords(self, description: str) -> bool:
        for keyword in self.keywords:
            if keyword in description.lower():
                return True
        return False