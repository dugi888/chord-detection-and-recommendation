import sounddevice as sd
import numpy as np
import librosa
import librosa.display


class ChordDecoder:
    def __init__(self, sample_rate=22050, buffer_duration=1, silence_threshold=0.001, smoothing_window=5):
        self.current_chord = "None"
        self.sample_rate = sample_rate
        self.buffer_duration = buffer_duration
        self.buffer_size = sample_rate * buffer_duration
        self.silence_threshold = silence_threshold
        self.chord_templates = {
            'C': [0, 4, 7],
            'C#m': [0, 3, 7],
            'D': [2, 6, 9],
            'Dm': [2, 5, 9],
            'E': [4, 8, 11],
            'Em': [4, 7, 11],
            'F': [5, 9, 0],
            'Fm': [5, 8, 0],
            'G': [7, 11, 2],
            'Gm': [7, 10, 2],
            'A': [9, 1, 4],
            'Am': [9, 0, 4],
            'B': [11, 3, 6],
            'Bm': [11, 2, 6],
        }
        self.smoothing_window = smoothing_window
        self.previous_chords = []  # To smooth chord transitions

    def get_chord(self):
        return self.current_chord

    def detect_chord(self, audio):
        chroma = librosa.feature.chroma_cqt(y=audio, sr=self.sample_rate, n_chroma=12)
        avg_chroma = chroma.mean(axis=1)

        detected_chord = None
        max_similarity = 0

        # Compare with each chord template
        for chord, indices in self.chord_templates.items():
            template = np.zeros(12)
            template[indices] = 1
            similarity = np.dot(template, avg_chroma)
            if similarity > max_similarity:
                max_similarity = similarity
                detected_chord = chord

        return detected_chord

    def smooth_chord(self, detected_chord):
        # Keep the last few detected chords for smoothing
        self.previous_chords.append(detected_chord)
        if len(self.previous_chords) > self.smoothing_window:
            self.previous_chords.pop(0)

        # Most frequent chord in the last few detections
        return max(set(self.previous_chords), key=self.previous_chords.count)

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")

        audio = indata[:, 0]

        rms_energy = np.sqrt(np.mean(audio ** 2))

        if rms_energy < self.silence_threshold:
            return

        audio = librosa.util.fix_length(audio, size=self.buffer_size)
        audio = librosa.util.normalize(audio)

        detected_chord = self.detect_chord(audio)
        if detected_chord:
            smoothed_chord = self.smooth_chord(detected_chord)
            if smoothed_chord != self.current_chord:
                self.current_chord = smoothed_chord
                print(f"Detected chord: {self.current_chord} (RMS: {rms_energy})")

    def start_listening(self):
        try:
            print("Listening for chords... Press Ctrl+C to stop.")
            with sd.InputStream(
                    channels=1,
                    callback=self.audio_callback,
                    samplerate=self.sample_rate,
                    blocksize=self.buffer_size,
            ):
                sd.sleep(int(1e5))  # Keep the stream alive
        except KeyboardInterrupt:
            print("Stopped listening.")
