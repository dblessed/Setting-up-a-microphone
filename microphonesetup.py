import sounddevice as sd
from scipy.io.wavfile import write
fs = 44100
seconds = 10
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()
write('output.wav', fs, myrecording)
