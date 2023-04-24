import numpy as np
import random

# cd audio at 44,100 hz and 16 bits per sample
SAMPLES_S = 44_100
BITS_SAMPLE = 16



# wave header constants
CHUNK_ID = b'RIFF'
FORMAT = b'WAVE'
SUBCHUNK_1_ID = b'fmt '
SUBCHUNK_2_ID = b'data'

# PCM constants
SUBCHUNK_1_SIZE = (16).to_bytes(4, byteorder='little')
AUDIO_FORMAT = (1).to_bytes(2, byteorder='little')



def create_pcm(frequencies):
    x_vals = np.arange(SAMPLES_S)
    y_vals = np.zeros(SAMPLES_S)

    for freqs, amp in frequencies:
        if not isinstance(freqs, tuple):
            freqs = (freqs,)
        for frequency in freqs:
            ang_freq = 2 * np.pi * frequency
            y_vals += 32767 * amp * np.sin(ang_freq * x_vals / SAMPLES_S)

    return np.int16(y_vals)

def new_wav(channels, filename, *args):
    seconds = len(args) // channels

    chunk_size = (int(36 + (seconds * SAMPLES_S * BITS_SAMPLE/8))).to_bytes(4, 'little')
    num_channels = (channels).to_bytes(2, byteorder='little')
    sample_rate = (SAMPLES_S).to_bytes(4, byteorder='little')
    byte_rate = (int(SAMPLES_S * channels * BITS_SAMPLE/8)).to_bytes(4, byteorder='little')
    block_align = (int(channels * BITS_SAMPLE/8)).to_bytes(2, byteorder='little')
    bits_per_sample = (BITS_SAMPLE).to_bytes(2, byteorder='little')
    subchunk_2_size = (int(seconds * SAMPLES_S * BITS_SAMPLE/8)).to_bytes(4, byteorder='little')

    my_pcm = []

    for arg in args:
        my_pcm.append(create_pcm(arg))

    mat = np.array(my_pcm)

    with open(f'{filename}.wav', 'wb') as fo:
        fo.write(
            CHUNK_ID +
            chunk_size +
            FORMAT +
            SUBCHUNK_1_ID +
            SUBCHUNK_1_SIZE +
            AUDIO_FORMAT +
            num_channels +
            sample_rate +
            byte_rate +
            block_align +
            bits_per_sample +
            SUBCHUNK_2_ID +
            subchunk_2_size +
            mat.tobytes()
        )

amp_chords = 0.15
amp_notes = 0.15
amp_bass_drum = 0.1
amp_snare_drum = 0.1

n = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
}

chords = [
    (n['C'], n['E'], n['G']),
    (n['F'], n['A'], n['C']),
    (n['G'], n['B'], n['D']),
]

rest = (0, 0, 0)
short_rest = (0,)

# minor chords
minor_chords = [
    (n['C'], n['E'] * 2**(1/12), n['G']),
    (n['F'], n['A'] * 2**(-1/12), n['C']),
    (n['G'], n['B'] * 2**(-1/12), n['D']),
]

# bass notes
bass_notes = [
    n['C'] / 2,
    n['F'] / 2,
    n['G'] / 2,
]

# pentatonic scale for the bass solo
pentatonic_scale = [
    n['C'],
    n['D'],
    n['F'],
    n['G'],
    n['A'],
]

bass_drum = 60
snare_drum = 200

bass_pattern = [
    bass_notes[0], bass_notes[0], bass_notes[0], bass_notes[0],
    bass_notes[1], bass_notes[1], bass_notes[1], bass_notes[1],
    bass_notes[2], bass_notes[2], bass_notes[2], bass_notes[2],
    bass_notes[0], bass_notes[0], bass_notes[0], bass_notes[0],
]

epic_fast_paced_bass_line = [
    (bass_note, bass_drum)
    for bass_note in bass_pattern
    for _ in range(4)
]

dark_bass = (
    *[((minor_chords[0], amp_chords), (n['E'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[0], amp_chords), (n['C'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum))],
    *[((minor_chords[1], amp_chords), (n['A'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[1], amp_chords), (n['F'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum))],
    *[((minor_chords[2], amp_chords), (n['E'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[2], amp_chords), (n['C'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum))],
    *[((minor_chords[0], amp_chords), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[0], amp_chords), (bass_drum, amp_bass_drum), (0, snare_drum))],
    *([
        ((minor_chords[0], amp_chords), (n['E'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[0], amp_chords), (n['C'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)),
        ((minor_chords[1], amp_chords), (n['A'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[1], amp_chords), (n['F'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)),
        ((minor_chords[2], amp_chords), (n['E'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[2], amp_chords), (n['C'], amp_notes), (bass_drum, amp_bass_drum), (0, snare_drum)),
        ((minor_chords[0], amp_chords), (bass_drum, amp_bass_drum), (0, snare_drum)), ((minor_chords[0], amp_chords), (bass_drum, amp_bass_drum), (0, snare_drum))
    ] * 5)
)

# Call the new_wav function
new_wav(1, 'pySong', *dark_bass)


