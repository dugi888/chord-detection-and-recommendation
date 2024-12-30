import tkinter as tk


class Display:
    def __init__(self, chord_decoder, chord_recommender):
        # Initialize the Tkinter window
        self.root = tk.Tk()
        self.root.title("Dynamic Chord Display")
        self.root.geometry("800x400")

        self.chord_decoder = chord_decoder
        self.chord_recommender = chord_recommender
        self.selected_key = tk.StringVar()

        self.create_key_selection_screen()

    def create_key_selection_screen(self):
        """
        Create the initial screen for key selection.
        """
        self.key_selection_frame = tk.Frame(self.root)
        self.key_selection_frame.pack(expand=True)

        label = tk.Label(self.key_selection_frame, text="Select Progression Key:", font=("Arial", 20))
        label.pack(pady=20)

        keys = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        self.key_dropdown = tk.OptionMenu(self.key_selection_frame, self.selected_key, *keys)
        self.key_dropdown.pack(pady=20)

        button = tk.Button(self.key_selection_frame, text="Start", command=self.start_chord_display)
        button.pack(pady=20)

    def start_chord_display(self):
        """
        Start the main chord display after key selection.
        """
        self.key_selection_frame.pack_forget()
        self.create_chord_display()
        self.update_chord()  # Start updating chords only after the display is created

    def create_chord_display(self):
        """
        Create the main chord display screen.
        """
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

    def update_chord(self):
        """
        Continuously update the displayed chord in real-time.
        """
        chord = self.chord_decoder.get_chord()
        if chord:
            self.chord_label.config(text=chord)
            if chord != "None":
                try:
                    recommended_chords = self.chord_recommender.get_recommended_chords(
                        chord, key=self.selected_key.get()
                    )
                    self.recommendation_label.config(text=f"Recommended Chords:\n" + "\n".join(recommended_chords))
                except KeyError:
                    print(f"Chord '{chord}' not found in chord_chromas dictionary")

        self.root.after(10, self.update_chord)  # This updates every 10ms (1 Hz)

    def run(self):
        self.root.mainloop()
