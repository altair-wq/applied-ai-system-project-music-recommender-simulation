# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0 (Content-Based Simulation)**

---

## 2. Intended Use  

This model is intended for educational exploration of content-based music recommendation algorithms. It generates small, ranked lists of tracks for hypothetical listener personas. It is strictly a classroom simulation designed to highlight algorithm bias and data representation issues. It is NOT intended for commercial use or deployed in any real application, as its heuristic approach does not capture the multidimensionality of actual musical preference.

---

## 3. How the Model Works  

VibeFinder 1.0 scores songs entirely based on content metadata. It completely ignores what other users are doing and strictly looks to answer one question: "How closely does this song match the user's specific request parameters?"

It does this by looking at three core features:
- **Genre**: If the genre is a 1-to-1 exact string match, the song earns a significant 2.0 point boost.
- **Mood**: If the mood matches exactly, the song earns an additional 1.0 point.
- **Energy**: Energy is treated as a dial from 0.0 to 1.0. We calculate the absolute distance between what the user wanted and what the song provides, resulting in up to 1.0 point for an exact match. Points drop linearly as the energetic distance grows.

---

## 4. Data  

The original dataset contained exactly 10 mock songs spanning genres like pop, lofi, rock, and ambient. We augmented the catalog manually, adding 6 new mock tracks to a total of 16. Included in our additions were more varieties of electronic, edm, classical, and indie. However, this dataset remains severely undersized and reflects incredibly simplified taste categorizations that do not capture subgenres, global sounds, or distinct artist eras.

---

## 5. Strengths  

VibeFinder is incredibly consistent. For single-dimensional users who want precisely one type of music ("Chill Lofi for studying", "High Energy Pop for the gym"), the logic behaves flawlessly. Its extreme emphasis on genre combined with distance-matching on numerical energy ensures that when the user asks for a category, that category immediately surfaces to the top. The simplistic heuristic models are highly interpretable—you always know *why* a song was recommended.

---

## 6. Limitations and Bias 

VibeFinder struggles catastrophically with nuanced taste due to its reliance on hard-coded heuristics. 
- Over-index on Genre: By granting "genre match" an overwhelming +2.0 weight, we run the risk of creating a massive filter bubble. A user asking for 'Rock' will be drowned in Rock music, even if a high-energy Pop anthem matches their 'intense' and 'high-energy' profile better.
- Demographic Ignore: It doesn't factor in era, popularity, or language. 
- The "Conflicting Profile" Bug: If a user specifies conflicting preferences (e.g., they want a song with high energy, but a 'sad' mood), the model fractures and returns chaotic overlaps because it doesn't understand the intersectional context of these tags. It treats variables independently.

---

## 7. Evaluation  

We evaluated VibeFinder against four highly targeted user profiles, using standard printing heuristics to ensure the list felt somewhat intuitive.
1. High-Energy Pop (Gym Hero)
2. Chill Lofi (Study Session)
3. Deep Intense Rock
4. Conflicting Profile (Sad EDM)

For 1, 2, and 3, our manually set weights of (+2 genre, +1 mood) achieved perfect alignment, returning the expected mock tracks at the exact top slots. Profile 4 surprised us by highlighting the algorithm's vulnerability edge-case: when conflicting dimensions arise, rather than recommending atmospheric high-energy tracks, the math breaks down and begins surfacing tracks based almost exclusively on random single-variable matches, heavily penalizing any track that fails a primary category.

---

## 8. Future Work  

If given more time, we would implement:
1. **Diversity Penalties**: A rule that depreciates the score of a track if a track by the exact same artist (or in the exact same genre) has already been recommended 2 or 3 times in the output. This prevents filter bubbles.
2. **Normalized Distances**: Applying Euclidean distance formulas across multiple audio features (danceability, valence, bpm) synchronously, rather than adding disparate flat points (+1 or +2) to a base.
3. **Collaborative Elements**: Injecting a "popularity" node or "users also liked" node to emulate massive neural network deployments.

---

## 9. Personal Reflection  

This project fundamentally highlighted the translation error between human "vibes" and mathematical heuristics. I learned that algorithms are intrinsically literal. They do not know what "music" is, they only know metadata values. It was surprising to see how quickly a simple +2 weight created an unshakeable filter bubble where the user became trapped inside one genre regardless of energy fit. This radically changes how I view apps like TikTok or Spotify; their AI models must be doing thousands of hyper-complex non-linear mappings just to simulate what human judgment handles intuitively in seconds. Human curatorial touch still absolutely rules in bridging conflicting emotional states that simple math just can't categorize.
