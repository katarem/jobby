class ExtractionService:

    def __init__(self, keywords: list[str]):
        self.keywords = keywords

    def detect_keywords(self, description: str) -> bool:
        desc_lower = description.lower()
        for keyword in self.keywords:
            if keyword in desc_lower:
                return True
        return False