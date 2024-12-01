from chord_decoder import ChordDecoder
from gui import Display
import threading


def start_chord_detection(detector):
    detector.run()


def start_gui(gui):
    gui.run()


if __name__ == "__main__":
    # Create ChordDecoder instance
    chord_decoder = ChordDecoder()

    # Start the audio processing in a separate thread
    listening_thread = threading.Thread(target=chord_decoder.start_listening, daemon=True)
    listening_thread.start()

    # Start the GUI
    display = Display(chord_decoder)
    display.run()
