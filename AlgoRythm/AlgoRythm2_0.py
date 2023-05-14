from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QSpinBox, QLabel
from PySide6.QtCore import Slot, Qt
from PySide6 import QtWidgets
import pygame
from textblob import TextBlob
import numpy as np
import music21 as m21

# Constants
CHORDS = {
    'C': (60, 64, 67),  # C Major
    'D': (62, 66, 69),  # D Major
    'E': (64, 68, 71),  # E Major
    'F': (65, 69, 72),  # F Major
    'G': (67, 71, 74),  # G Major
    'A': (69, 73, 76),  # A Major
    'B': (71, 75, 78),  # B Major
    'Cm': (60, 63, 67),  # C Minor
    'Dm': (62, 65, 69),  # D Minor
    'Em': (64, 67, 71),  # E Minor
    'Fm': (65, 68, 72),  # F Minor
    'Gm': (67, 70, 74),  # G Minor
    'Am': (69, 72, 76),  # A Minor
    'Bm': (71, 74, 78),  # B Minor
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton("Songiffy", self)
        self.button.setGeometry(100, 50, 200, 50)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(100, 100, 200, 50)
        self.text_edit.textChanged.connect(self.update_character_count)
        
         # Label to show the remaining characters
        self.character_count_label = QLabel("300", self)
        self.character_count_label.setGeometry(100, 140, 200, 50)
        self.character_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        #self.text_label = QLabel("Enter some text:", self)
        #self.text_label.setGeometry(100, 120, 200, 20)

        self.length_spinbox = QSpinBox(self)
        self.length_spinbox.setGeometry(100, 250, 100, 20)
        self.length_spinbox.setMinimum(1)
        self.length_spinbox.setMaximum(100)
        self.length_spinbox.setValue(10)

        # self.length_label = QLabel("Song length (in words):", self)
        # self.length_label.setGeometry(100, 220, 200, 20)

        self.tempo_spinbox = QSpinBox(self)
        self.tempo_spinbox.setGeometry(200, 250, 100, 20)
        self.tempo_spinbox.setMinimum(40)
        self.tempo_spinbox.setMaximum(240)
        self.tempo_spinbox.setValue(120)

        self.tempo_label = QLabel("Tempo (BPM):", self)
        self.tempo_label.setGeometry(200, 220, 200, 20)

        self.button.clicked.connect(self.play_sound)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Songiffy')
        
        # Set the maximum length to 300 characters
        self.max_lines = 4
        # Set the maximum length to 300 characters
        self.max_length = 300
        
    def update_character_count(self):
        # Update the remaining character count label as the user types
        text = self.text_edit.toPlainText()
        remaining_characters = self.max_length - len(text)
        self.character_count_label.setText(str(remaining_characters))

    @Slot()
    def play_sound(self):
        # Get the text and its sentiment using TextBlob
        text = self.text_edit.toPlainText()
        if len(text) > 300:
            error_dialog = QtWidgets.QMessageBox(self)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("Maximum limit of 300 characters has been reached.")
            error_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            error_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            error_dialog.exec()
            return
        
        sentiment = TextBlob(text).sentiment.polarity

        # Choose scale based on sentiment
        if sentiment < -0.9:
            scale = ['Cm', 'Dm', 'Em']  # Extremely dark moods
        elif -0.9 <= sentiment < -0.7:
            scale = ['Fm', 'Gm', 'Am']  # Very dark moods
        elif -0.7 <= sentiment < -0.5:
            scale = ['Bm', 'Cm', 'Dm']  # Dark moods
        elif -0.5 <= sentiment < -0.3:
            scale = ['Em', 'Fm', 'Gm']  # Slightly darker moods
        elif -0.3 <= sentiment < -0.1:
            scale = ['Am', 'Bm', 'Cm']  # Neutral to dark moods
        elif -0.1 <= sentiment < 0.1:
            scale = ['C', 'D', 'E']  # Neutral moods
        elif 0.1 <= sentiment < 0.3:
            scale = ['F', 'G', 'A']  # Neutral to happy moods
        elif 0.3 <= sentiment < 0.5:
            scale = ['B', 'C', 'D']  # Slightly happier moods
        elif 0.5 <= sentiment < 0.7:
            scale = ['E', 'F', 'G']  # Happy moods
        elif 0.7 <= sentiment < 0.9:
            scale = ['A', 'B', 'C']  # Very happy moods
        else:
            scale = ['D', 'E', 'F']  # Extremely happy moods

        # Generate chord progression and melody
        np.random.seed(len(text))
        num_chords = min(len(text) // 10, 100)
        chord_seq = np.random.choice(scale, size=num_chords)
        melody = generate_melody(chord_seq, len(chord_seq))

        # Create the MIDI file
        midi_stream = create_midi_stream(chord_seq, melody, self.tempo_spinbox.value())
        midi_stream.write('midi', fp='song.mid')

        # Play the MIDI file
        pygame.mixer.init()
        pygame.mixer.music.load("song.mid")
        pygame.mixer.music.play()

    @Slot()
    def limit_characters(self):
        text = self.text_edit.toPlainText()
        if len(text) > 300:
            self.text_edit.setText(text[:300])

def generate_melody(chord_seq, num_notes):
    # Generate melody that follows the chord progresion
    melody = []
    while len(melody) < num_notes:
        for i in range(len(chord_seq)):
            chord = CHORDS[chord_seq[i % len(chord_seq)]]
            melody.append(chord[np.random.randint(0, len(chord))] + (12 * np.random.randint(1, 4)))
    return melody

def create_midi_stream(chord_seq, melody, tempo):
    # Create a MIDI file from the chord progression and melody
    stream = m21.stream.Stream()
    stream.append(m21.tempo.MetronomeMark(number=tempo))
    for i in range(len(chord_seq)):
        chord = m21.chord.Chord(CHORDS[chord_seq[i]])
        chord.duration = m21.duration.Duration(4)
        stream.append(chord)

        for j in range(4):
            if 4 * i + j < len(melody):
                note = m21.note.Note()
                note.pitch.midi = melody[4 * i + j]
                note.duration = m21.duration.Duration(1)
                stream.append(note)

    return stream

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
