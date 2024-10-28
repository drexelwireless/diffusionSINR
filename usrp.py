import numpy as np
import SoapySDR
from SoapySDR import *  # SOAPY_SDR constants
import time
import matplotlib.pyplot as plt

# Parameters
tx_ip = "192.168.10.2"  # IP of the USRP transmitting
samp_rate = 1e6  # 1 MHz sample rate
center_freq = 2.4e9  # 2.4 GHz
tx_gain = 40  # Gain for the transmitter

# Create SDR object
sdr = SoapySDR.Device(dict(driver="uhd", addr=tx_ip))

# Set sample rate and frequency
sdr.setSampleRate(SOAPY_SDR_TX, 0, samp_rate)
sdr.setFrequency(SOAPY_SDR_TX, 0, center_freq)
sdr.setGain(SOAPY_SDR_TX, 0, tx_gain)

# Create LFM signal (chirp)
def lfm_signal(samples, bw, t):
    t_vals = np.linspace(0, t, samples)
    return np.exp(1j * np.pi * bw / t * t_vals ** 2)

# Create QPSK signal
def qpsk_mod(data):
    return np.exp(1j * (np.pi / 4 * data))  # QPSK modulation

# Parameters for signals
num_samples = int(samp_rate * 0.01)  # Number of samples for 10 ms transmission
lfm_bw = 500e3  # LFM bandwidth 500 kHz
qpsk_data = np.random.randint(0, 4, num_samples)  # Random QPSK data

# Create LFM and QPSK signals
lfm_sig = lfm_signal(num_samples, lfm_bw, 0.01)
qpsk_sig = qpsk_mod(qpsk_data)

# Combine the signals
tx_signal = lfm_sig + qpsk_sig

# Add noise/interference if required
noise_power = 0.01  # Adjust noise power for interference
tx_signal += np.random.normal(0, np.sqrt(noise_power), num_samples) + \
             1j * np.random.normal(0, np.sqrt(noise_power), num_samples)

# Transmit continuously
tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32, [0])
sdr.activateStream(tx_stream)
print("Transmitting...")

while True:
    sdr.writeStream(tx_stream, [tx_signal.astype(np.complex64)], num_samples)









import numpy as np
import SoapySDR
from SoapySDR import *  # SOAPY_SDR constants
import matplotlib.pyplot as plt

# Parameters
rx_ip = "192.168.10.3"  # IP of the USRP receiving
samp_rate = 1e6  # 1 MHz sample rate
center_freq = 2.4e9  # 2.4 GHz
rx_gain = 30  # Gain for the receiver

# Create SDR object
sdr = SoapySDR.Device(dict(driver="uhd", addr=rx_ip))

# Set sample rate and frequency
sdr.setSampleRate(SOAPY_SDR_RX, 0, samp_rate)
sdr.setFrequency(SOAPY_SDR_RX, 0, center_freq)
sdr.setGain(SOAPY_SDR_RX, 0, rx_gain)

# Set up receiver stream
rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [0])
sdr.activateStream(rx_stream)

# Function to calculate SINR
def calculate_sinr(signal, noise):
    signal_power = np.mean(np.abs(signal) ** 2)
    noise_power = np.mean(np.abs(noise) ** 2)
    sinr = 10 * np.log10(signal_power / noise_power)
    return sinr

# Receive and process
num_samples = int(samp_rate * 0.01)  # Number of samples to capture
buff = np.zeros(num_samples, dtype=np.complex64)

print("Receiving...")

# Capture signal
sr = sdr.readStream(rx_stream, [buff], num_samples)
received_signal = np.array(buff)

# Plot the received signal in time domain
plt.figure()
plt.plot(np.real(received_signal), label='Real')
plt.plot(np.imag(received_signal), label='Imag')
plt.title('Received Signal in Time Domain')
plt.legend()
plt.show()

# Calculate and display SINR
noise_power = 0.01  # Assumed noise power (can measure separately)
sinr = calculate_sinr(received_signal, noise_power)
print(f"SINR: {sinr:.2f} dB")

# Shutdown
sdr.deactivateStream(rx_stream)
sdr.closeStream(rx_stream)
