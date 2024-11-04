Data Collection with Jamming for Spectrogram Analysis

Steps Overview
- Transmit a Continuous Tone from grid02 (Baseline Signal)
- Set Up IQ Data Logging on Receiver Node grid01
- Introduce Jamming with Varying Intensities on grid03
- Stop Data Logging and Transfer the File to Your Local Machine
- Generate Spectrogram Snippets from the Collected IQ Data

Step 1: Transmit a Continuous Tone (Baseline Signal)
Log into grid02.

Start Tone Transmission:

uhd_siggen -f 1.305e9 -s 1e6 -g 20 --sine -x 10e3

Frequency: 1.305 GHz
Sample Rate: 1 MHz
Gain: 20 dB
Leave this running throughout the data collection process.

Step 2: Set Up IQ Data Logging on Receiver (grid01)
Log into grid01.

Start IQ Data Logging using uhd_rx_cfile to capture 60 seconds of IQ data:


uhd_rx_cfile --freq 1.305e9 --samp-rate 1e6 --gain 20 /home/mt3429/logsFinal/iq_data_with_jamming.bin


Output file: /home/mt3429/logsFinal/iq_data_with_jamming.bin
Let this command run for the entire 60 seconds while you introduce jamming from grid03.

##Step 3: Introduce Jamming with Varying Intensities on grid03
Log into grid03.

Run DragonJammer to introduce jamming in 20-second increments with increasing strength:

First 20 Seconds


./DragonJammer -f 1.305e9 -b 1e6 -G 5 -t 20 (Low Jamming)
Next 20 Seconds 


./DragonJammer -f 1.305e9 -b 2e6 -G 15 -t 20 (Medium Jamming)
Final 20 Seconds


./DragonJammer -f 1.305e9 -b 4e6 -G 30 -t 20 (High Jamming)
Frequency: 1.305 GHz

Bandwidths: 1 MHz, 2 MHz, 4 MHz (progressively)

Gains: 5, 15, and 30 dB (progressively)

This creates a 60-second capture with varying jamming intensities.

Step 4: Stop IQ Data Logging and Transfer to Local Machine
Stop uhd_rx_cfile on grid01 after 60 seconds by pressing Ctrl+C.

Verify that the file was saved:


ls -lh /home/mt3429/logsFinal/iq_data_with_jamming.bin
Copy the IQ Data File to Your Local Machine:


scp mt3429@dwslgrid.ece.drexel.edu:/home/mt3429/logsFinal/iq_data_with_jamming.bin /path/to/your/local/directory/
Replace /path/to/your/local/directory/ with the actual path where you want to save the file.

Step 5: Generate Spectrogram Snippets with Visible Jamming Levels
Set up a Python script to create 60 spectrogram snippets (1 per second) to visualize varying jamming levels.

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import spectrogram
    import os
    
    # Path to your IQ data file with jamming and output directory
    file_path = '/Users/matthewtylek/repos/stable-diffusion-research/dataCollect/iq_data_with_jamming.bin'
    output_dir = '/Users/matthewtylek/repos/stable-diffusion-research/dataCollect/spectrogram_snippets_jamming'
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load the IQ data
    iq_data = np.fromfile(file_path, dtype=np.complex64)
    
    # Parameters for spectrogram generation
    sample_rate = 1e6  # Sampling rate in Hz
    snippet_duration = 1  # Duration of each snippet in seconds
    snippet_samples = int(sample_rate * snippet_duration)  # Number of samples per snippet
    
    # Loop through data in chunks and generate spectrograms
    for i in range(0, len(iq_data), snippet_samples):
        snippet = iq_data[i:i + snippet_samples]
        
        # Skip if the last chunk is smaller than snippet_samples
        if len(snippet) < snippet_samples:
            break
        
        # Generate the spectrogram
        f, t, Sxx = spectrogram(snippet, fs=sample_rate, nperseg=1024, noverlap=512)
        
        # Plot the spectrogram
        plt.figure(figsize=(10, 6))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [s]')
        plt.colorbar(label='Intensity [dB]')
        plt.title(f'Spectrogram Snippet {i // snippet_samples + 1}')
        plt.tight_layout()
        
        # Save the spectrogram as an image
        output_file = os.path.join(output_dir, f'spectrogram_snippet_{i // snippet_samples + 1}.png')
        plt.savefig(output_file)
        plt.close()
        
        print(f"Saved {output_file}")
    
    print("All spectrogram snippets with jamming levels saved.")
    




Make sure you have the required Python packages installed:


pip install numpy matplotlib scipy
