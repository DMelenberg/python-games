"""
Generate sound effects for the 2048 game using wave synthesis.
This creates simple but pleasant sound effects without external dependencies.
"""
import wave
import struct
import math
import os

def generate_sine_wave(frequency, duration, sample_rate=44100, amplitude=0.3):
    """Generate a sine wave with given frequency and duration."""
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        # Add envelope (fade in/out) for smoother sound
        envelope = 1.0
        if i < sample_rate * 0.01:  # Fade in
            envelope = i / (sample_rate * 0.01)
        elif i > num_samples - sample_rate * 0.05:  # Fade out
            envelope = (num_samples - i) / (sample_rate * 0.05)
        
        sample = amplitude * envelope * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(int(sample * 32767))
    return samples

def generate_chord(frequencies, duration, sample_rate=44100, amplitude=0.2):
    """Generate a chord from multiple frequencies."""
    num_samples = int(sample_rate * duration)
    samples = [0] * num_samples
    
    for freq in frequencies:
        wave_samples = generate_sine_wave(freq, duration, sample_rate, amplitude / len(frequencies))
        for i in range(num_samples):
            samples[i] += wave_samples[i]
    
    # Normalize
    max_val = max(abs(s) for s in samples)
    if max_val > 32767:
        samples = [int(s * 32767 / max_val) for s in samples]
    
    return samples

def save_wav(filename, samples, sample_rate=44100):
    """Save samples as a WAV file."""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        for sample in samples:
            wav_file.writeframes(struct.pack('h', sample))

def main():
    sounds_dir = os.path.dirname(__file__) + '/sounds'
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("Generating sound effects...")
    
    # Tile move sound - short click
    move_samples = generate_sine_wave(800, 0.05, amplitude=0.2)
    save_wav(f'{sounds_dir}/move.wav', move_samples)
    print("✓ move.wav")
    
    # Tile merge sound - pleasant ascending tones
    merge_samples = []
    for freq in [440, 550, 660]:
        merge_samples.extend(generate_sine_wave(freq, 0.08, amplitude=0.15))
    save_wav(f'{sounds_dir}/merge.wav', merge_samples)
    print("✓ merge.wav")
    
    # Win sound - triumphant chord progression
    win_samples = []
    chords = [
        [523, 659, 784],  # C major
        [587, 740, 880],  # D major
        [659, 831, 988],  # E major
    ]
    for chord in chords:
        win_samples.extend(generate_chord(chord, 0.4))
    save_wav(f'{sounds_dir}/win.wav', win_samples)
    print("✓ win.wav")
    
    # Lose sound - descending tones
    lose_samples = []
    for freq in [440, 370, 330, 294]:
        lose_samples.extend(generate_sine_wave(freq, 0.2, amplitude=0.15))
    save_wav(f'{sounds_dir}/lose.wav', lose_samples)
    print("✓ lose.wav")
    
    # Menu click sound
    click_samples = generate_sine_wave(1000, 0.03, amplitude=0.2)
    save_wav(f'{sounds_dir}/click.wav', click_samples)
    print("✓ click.wav")
    
    # New tile sound - soft pop
    new_tile_samples = []
    for i, freq in enumerate([300, 500, 700]):
        amp = 0.1 * (1 - i * 0.2)
        new_tile_samples.extend(generate_sine_wave(freq, 0.03, amplitude=amp))
    save_wav(f'{sounds_dir}/new_tile.wav', new_tile_samples)
    print("✓ new_tile.wav")
    
    print("\nAll sound effects generated successfully!")

if __name__ == "__main__":
    main()
