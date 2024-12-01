import tkinter as tk
import random


class Display:
    def __init__(self, chord_decoder):
        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Dynamic Chord Display")
        self.root.geometry("800x400")

        self.chord_decoder = chord_decoder

        # current ch | recommended ch
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Current chord
        self.chord_label = tk.Label(
            self.left_frame,
            text="",
            font=("Arial", 100, "bold"),
            fg="blue",
        )
        self.chord_label.pack(expand=True)

        # Recommended chords
        self.recommendation_label = tk.Label(
            self.right_frame,
            text="Recommended Chords:\n",
            font=("Arial", 20),
            fg="black",
        )
        self.recommendation_label.pack(expand=True)

        self.update_chord()

    def get_random_chords(self):
        """
        Generate a list of random chords to recommend.
        """
        chords = ["C", "D", "E", "F", "G", "A", "B", "C#m", "D#m", "Em", "Fm", "G#m", "Am", "Bm"]
        return random.sample(chords, 5)  # Return a random sample of 5 chords

    def update_chord(self):
        """
        Continuously update the displayed chord in real-time.
        """
        chord = self.chord_decoder.get_chord()
        if chord:
            self.chord_label.config(text=chord)
            recommended_chords = self.get_random_chords()  # Get the list of recommended chords
            self.recommendation_label.config(text=f"Recommended Chords:\n" + "\n".join(recommended_chords))

        self.root.after(100, self.update_chord)  # This updates every 100ms (10 Hz)

    def run(self):
        self.root.mainloop()

# if __name__ == "__main__":
#     detector = cd()
#     gui = Display(detector)
#     gui.run()
