# Model Card: Music Discovery AI Assistant

## Model/System Name
Music Discovery AI Assistant (Project 4)

## Goal / Task
The goal of this system is to act as an intelligent music recommendation assistant. It takes natural language user queries, extracts music preferences, retrieves helpful context from a knowledge base, scores songs based on the user's profile, and provides a final response that includes recommendations, confidence scoring, and explanations.

## Original Module 3 Base Project
This system builds upon the CodePath AI110 Module 3 "Music Recommender Simulation." The base project successfully implemented a weighted scoring algorithm (using genre, mood, and energy) to rank songs from a CSV file against a static user taste profile.

## Data Used
- `data/songs.csv`: A synthetic dataset of songs containing attributes like genre, mood, energy, tempo, valence, and acousticness.
- `data/knowledge_base.txt`: A simple text file containing rules and facts about music recommendation (e.g., how genre and mood affect scores, limitations of recommenders).

## Algorithm Summary
1. **Preference Parsing**: Extracts keywords (genre, mood, energy indicators) from the user query.
2. **RAG Retrieval**: Uses simple token overlap to retrieve the most relevant facts from the knowledge base based on the user query.
3. **Scoring**: Calculates a score for each song by comparing its attributes to the parsed preferences (genre match = +2.0, mood match = +1.0, energy similarity = up to +1.0).
4. **Guardrails**: Checks for unsupported domains (e.g., movies, medical advice) and low-confidence results.
5. **Confidence Scoring**: Normalizes the average score of the top recommendations into a 0.0 - 1.0 confidence value.

## RAG/Retrieval Summary
The RAG component is implemented using a custom, lightweight Python retriever (`RagAssistant`). It splits the knowledge base text into chunks and uses a basic word intersection (overlap) algorithm to find chunks that match the vocabulary of the user's query.

## Guardrails
- **Domain Guardrail**: Rejects queries containing keywords unrelated to music (e.g., "movies", "health").
- **Quality Guardrail**: Warns the user if the top recommended songs produce an average confidence score below 0.3, indicating the dataset lacks songs that strongly match the user's complex preferences.

## Observed Behavior and Biases
- **Filter Bubble**: The system heavily favors exact genre matches. If a user only asks for "pop", they will only see pop songs. A small diversity penalty exists but may not be enough to introduce entirely new genres.
- **Limited Nuance**: The simple keyword parser can misinterpret complex natural language (e.g., "I don't want pop" might still trigger the "pop" genre if not carefully handled).

## Evaluation Process
The system is evaluated using an automated test harness (`evaluator.py`) that runs 6 distinct test cases from `tests/test_cases.json`, covering happy paths, edge cases, and out-of-domain requests.

## Testing Results
- The system correctly handles standard requests (e.g., "chill study songs", "high-energy gym").
- The domain guardrail successfully blocks out-of-scope requests.
- Queries with conflicting preferences (e.g., "sad edm") gracefully return results but with a lower confidence score.

## Intended Use
For users looking to discover new music based on specific activities, moods, or genres within a controlled, safe dataset.

## Non-Intended Use
- Providing non-music recommendations (e.g., movies, medical advice).
- Replacing professional, large-scale recommendation systems like Spotify or Apple Music.

## Limitations
- The dataset is extremely small (15-20 songs).
- The parser is primitive and lacks true semantic understanding (it relies on hardcoded keywords).
- The RAG system does not use dense vector embeddings, so it struggles with synonyms.

## Possible Misuse and Prevention
- **Misuse**: Users attempting to bypass the system to get inappropriate or out-of-domain advice.
- **Prevention**: Hardcoded keyword blocklists in the guardrails module prevent the system from engaging with sensitive or non-music topics.

## Ideas for Improvement
- Integrate a real LLM API (like OpenAI or Gemini) for better natural language understanding and preference extraction.
- Expand the dataset to thousands of songs.
- Upgrade the RAG system to use a vector database (like ChromaDB or FAISS) for semantic search instead of token overlap.

## AI Collaboration Reflection
- **One helpful AI suggestion**: The AI suggested using a simple normalized average of the recommender scores to create a "confidence score," which elegantly reused the existing logic without adding complex probability math.
- **One flawed AI suggestion**: Initially, the AI suggested using `sklearn` for TF-IDF in the RAG module.
- **How I verified or corrected the AI output**: I realized `scikit-learn` was not in our `requirements.txt` and I wanted to keep the project simple without adding heavy dependencies, so I corrected the approach to use a lightweight token overlap algorithm using built-in Python standard libraries.
