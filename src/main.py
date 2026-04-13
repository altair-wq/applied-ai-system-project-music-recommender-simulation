"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = {
        "High-Energy Pop (Gym Hero)": {"genre": "pop", "mood": "intense", "energy": 0.9},
        "Chill Lofi (Study Session)": {"genre": "lofi", "mood": "chill", "energy": 0.3},
        "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.85},
        "Conflicting Profile (Sad EDM)": {"genre": "edm", "mood": "sad", "energy": 0.9}
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n======================================")
        print(f"Profile: {profile_name}")
        print(f"Preferences: {user_prefs}")
        print(f"======================================")
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("Top recommendations:\n")
        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
