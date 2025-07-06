class ExtractionService:

    def __init__(self, keywords: list[str]):
        self.keywords = [keyword.lower() for keyword in keywords]

    def detect_keywords(self, description: str) -> bool:
        desc_lower = description.lower()
        for keyword in self.keywords:
            if keyword in desc_lower:
                return True
        return False
    
    def extract_keywords(self, description: str) -> list[str]:
        desc_lower = description.lower()
        extracted = []
        for keyword in self.keywords:
            if keyword in desc_lower:
                extracted.append(keyword)
        return extracted