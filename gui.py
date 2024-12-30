import tkinter as tk


class Display:
    def __init__(self, chord_decoder, chord_recommender):
        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Dynamic Chord Display")
        self.root.geometry("800x400")

        self.chord_decoder = chord_decoder
        self.chord_recommender = chord_recommender

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


    def update_chord(self):
        """
        Continuously update the displayed chord in real-time.
        """
        chord = self.chord_decoder.get_chord()
        if chord:
            self.chord_label.config(text=chord)
            if chord  != "None":
                try:
                    recommended_chords = self.chord_recommender.get_recommended_chords(chord,
                                                                   key="C")  # Get the list of recommended chords with key C
                    self.recommendation_label.config(text=f"Recommended Chords:\n" + "\n".join(recommended_chords))
                except KeyError:
                    print(f"Chord '{chord}' not found in chord_chromas dictionary")

        self.root.after(10, self.update_chord)  # This updates every 10ms (1 Hz)

    def run(self):
        self.root.mainloop()
#
# if __name__ == "__main__":
#     detector = cd()
#     gui = Display(detector)
#     gui.run()
