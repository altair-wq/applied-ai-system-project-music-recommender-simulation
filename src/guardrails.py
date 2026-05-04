from typing import List

UNSUPPORTED_KEYWORDS = [
    "movie", "movies", "film", "films", "tv", "show", "book", "books",
    "medical", "health", "doctor", "advice", "recipe", "food", "cook"
]

def check_unsupported_query(query: str) -> tuple[bool, str]:
    """
    Checks if the user query contains unsupported keywords.
    Returns a tuple of (is_supported, warning_message).
    """
    query_lower = query.lower()
    for kw in UNSUPPORTED_KEYWORDS:
        if kw in query_lower:
            return False, f"Unsupported request: The system is designed for music recommendations only. Keyword '{kw}' detected."
    return True, ""

def calculate_confidence(recommendations: List[tuple]) -> float:
    """
    Calculates a confidence score based on the recommendation scores.
    recommendations: List of tuples (song, score, explanation)
    """
    if not recommendations:
        return 0.0
    
    # A perfect score in the original system is typically 3.0+ (2.0 genre + 1.0 mood + 1.0 energy)
    # We take the average score of the top recommendations and normalize it a bit.
    avg_score = sum(rec[1] for rec in recommendations) / len(recommendations)
    
    # Let's say a score of 3.0+ is 1.0 (100%) confidence.
    confidence = min(1.0, avg_score / 3.0)
    return confidence

def check_recommendation_quality(recommendations: List[tuple], min_confidence: float = 0.3) -> tuple[bool, str]:
    """
    Checks if we have enough quality recommendations.
    """
    if not recommendations:
        return False, "No recommendations found for the given criteria."
    
    confidence = calculate_confidence(recommendations)
    if confidence < min_confidence:
        return False, f"Low confidence ({confidence:.2f}): The dataset does not contain enough songs that strongly match your preferences."
        
    return True, ""
