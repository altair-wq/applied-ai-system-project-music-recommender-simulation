"""
Command line runner for the Music Recommender Simulation - AI Assistant Version.
"""

import sys
from src.recommender import load_songs, recommend_songs
from src.rag_assistant import RagAssistant
from src.guardrails import check_unsupported_query, calculate_confidence, check_recommendation_quality
from src.logger import logger

def parse_query_to_prefs(query: str) -> dict:
    """
    Very simple keyword-based parser to extract user preferences from a query.
    In a real system, an LLM would do this extraction.
    """
    query_lower = query.lower()
    prefs = {"genre": None, "mood": None, "energy": None}
    
    # Genres
    for g in ["pop", "lofi", "rock", "ambient", "jazz", "synthwave", "indie pop", "electronic", "folk", "edm", "classical"]:
        if g in query_lower:
            prefs["genre"] = g
            break
            
    # Moods
    for m in ["happy", "chill", "intense", "relaxed", "moody", "focused", "energetic", "sad"]:
        if m in query_lower:
            prefs["mood"] = m
            break
            
    # Energy heuristics
    if "high-energy" in query_lower or "gym" in query_lower or "workout" in query_lower:
        prefs["energy"] = 0.9
    elif "chill" in query_lower or "study" in query_lower or "sleep" in query_lower or "sad" in query_lower:
        prefs["energy"] = 0.3
    
    return prefs

def process_query(query: str, songs: list, assistant: RagAssistant):
    logger.info(f"Received query: '{query}'")
    
    # 1. Guardrail Check
    is_supported, warning = check_unsupported_query(query)
    if not is_supported:
        logger.warning(f"Guardrail triggered: {warning}")
        print(f"Assistant: {warning}\n")
        return
        
    # 2. Parse Preferences
    prefs = parse_query_to_prefs(query)
    logger.info(f"Extracted preferences: {prefs}")
    
    # 3. Retrieve Context (RAG)
    context = assistant.retrieve(query, top_k=2)
    logger.info(f"Retrieved context chunks: {len(context)}")
    
    # 4. Generate Recommendations
    recommendations = recommend_songs(prefs, songs, k=3)
    
    # 5. Calculate Confidence & Quality Guardrail
    confidence = calculate_confidence(recommendations)
    logger.info(f"Calculated confidence: {confidence:.2f}")
    
    is_good_quality, quality_warning = check_recommendation_quality(recommendations)
    if not is_good_quality:
        logger.warning(quality_warning)
        print(f"Assistant: {quality_warning}")
        # Note: We still might want to show them if we have some, but with a warning.
    
    # 6. Generate Final Response
    response = assistant.generate_response(query, recommendations, context, confidence)
    logger.info("Successfully generated response.")
    
    print(f"\n{response}\n")
    print("="*50 + "\n")

def main() -> None:
    logger.info("Starting up Music Discovery Assistant...")
    songs = load_songs("data/songs.csv") 
    assistant = RagAssistant("data/knowledge_base.txt")
    
    test_queries = [
        "Recommend chill songs for studying",
        "I want high-energy pop songs for the gym",
        "Suggest sad acoustic music",
        "Can you recommend some good movies?",
        "Why did you recommend this song? What about genre?"
    ]

    for q in test_queries:
        process_query(q, songs, assistant)

if __name__ == "__main__":
    main()
