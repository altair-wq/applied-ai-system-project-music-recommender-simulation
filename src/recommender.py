import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'acousticness': 1.0 if user.likes_acoustic else 0.0
        }
        
        scored = []
        for song in self.songs:
            song_dict = song.__dict__
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
            
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'acousticness': 1.0 if user.likes_acoustic else 0.0
        }
        
        _, reasons = score_song(user_prefs, song.__dict__)
        return ", ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    for k, v in row.items():
                        if k in ['id', 'tempo_bpm']:
                            row[k] = int(v)
                        elif k in ['energy', 'valence', 'danceability', 'acousticness']:
                            row[k] = float(v)
                    songs.append(row)
                except ValueError:
                    continue
    except FileNotFoundError:
        print(f"Error: Could not find {csv_path}")
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []
    
    if song.get('genre') == user_prefs.get('genre'):
        score += 2.0
        reasons.append("genre match (+2.0)")
        
    if song.get('mood') == user_prefs.get('mood'):
        score += 1.0
        reasons.append("mood match (+1.0)")
        
    target_energy = user_prefs.get('energy')
    if target_energy is not None and 'energy' in song:
        energy_diff = abs(song['energy'] - target_energy)
        energy_score = max(0.0, 1.0 - energy_diff)
        score += energy_score
        reasons.append(f"energy similarity (+{energy_score:.2f})")
        
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, ", ".join(reasons)))
        
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
