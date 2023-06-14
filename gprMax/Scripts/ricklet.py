import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Define Ricker wavelet parameters
f = 10 # Center frequency
width = 0.1 # Wavelet width

# Generate Ricker wavelet
t = np.linspace(-1, 1, 1000, endpoint=False)
y = signal.ricker(len(t), width)

# Plot Ricker wavelet
plt.plot(t, y)
plt.title('Ricker Wavelet')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()

# Calculate frequency and decibel relationship
frequencies, power_spectrum = signal.periodogram(y, fs=1/np.mean(np.diff(t)))
db_spectrum = 10 * np.log10(power_spectrum)

# Plot frequency and decibel relationship
plt.plot(frequencies, db_spectrum)
plt.title('Frequency and Decibel Relationship of Ricker Wavelet')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power Spectral Density (dB/Hz)')
plt.show()