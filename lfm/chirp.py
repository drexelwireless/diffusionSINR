import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import chirp, spectrogram

# Set parameters
t = np.linspace(0, 1, 44100)  # 1 second duration, sampled at 44100 Hz
f0 = 100  # Starting frequency
f1 = 1000  # Ending frequency at time t1
num_chirps = 1000  # Number of chirps to generate
folder_name = "lfm"

# Create folder if it does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Generate and save each chirp signal's spectrogram as a PNG image
for i in range(num_chirps):
    # Calculate the end frequency for each chirp
    freq_end = f0 + i * (f1 - f0) / num_chirps
    
    # Create chirp signal
    chirp_signal = chirp(t, f0=f0, t1=1, f1=freq_end, method='linear')
    
    # Generate spectrogram
    f, t_spec, Sxx = spectrogram(chirp_signal, fs=44100)
    
    # Plot and save the spectrogram
    plt.figure(figsize=(10, 4))
    plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title(f'LFM Chirp: Start={f0} Hz, End={int(freq_end)} Hz')
    plt.colorbar(label='Intensity [dB]')
    
    # Save as PNG
    filename = os.path.join(folder_name, f"chirp_{int(freq_end)}Hz.png")
    plt.savefig(filename, format='png')
    plt.close()

print("100 LFM chirp spectrograms have been saved to the 'lfm' folder as PNG images.")
