import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class ChordRecommender:
    def __init__(self):
        self.chord_chromas = {
            'C':   [1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
            'C#m': [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
            'D':   [0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
            'Dm':  [0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
            'E':   [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            'Em':  [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
            'F':   [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
            'Fm':  [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0],
            'G':   [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            'Gm':  [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            'A':   [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
            'Am':  [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
            'B':   [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1],
            'Bm':  [0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
        }

        # Common progressions relative to the key
        self.progressions = {
            'C': ['F', 'G', 'Am', 'Dm'],
            'D': ['G', 'A', 'Bm', 'Em'],
            'E': ['A', 'B', 'C#m', 'F#m'],
            'F': ['Bb', 'C', 'Dm', 'Gm'],
            'G': ['C', 'D', 'Em', 'Am'],
            'A': ['D', 'E', 'F#m', 'Bm'],
            'B': ['E', 'F#', 'G#m', 'C#m'],
        }

    def get_recommended_chords(self, current_chord, key=None):
        current_chroma = np.array(self.chord_chromas[current_chord]).reshape(1, -1)
        similarities = {}

        for chord, chroma in self.chord_chromas.items():
            if chord != current_chord:
                similarity = cosine_similarity(current_chroma, np.array(chroma).reshape(1, -1))[0][0]
                similarities[chord] = similarity

        # Sort chords by similarity
        recommended_chords = sorted(similarities, key=similarities.get, reverse=True)

        if key:
            # Prioritize chords in the same key
            key_progressions = self.progressions.get(key, [])
            recommended_chords = sorted(
                recommended_chords,
                key=lambda chord: (chord in key_progressions, similarities[chord]),
                reverse=True
            )

        return recommended_chords[:5]
