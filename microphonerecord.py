import pyaudio

import math
import struct
import wave
import time
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import librosa

def record_data(filename, duration, fs, channels):
   
    # synchronous recording
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    y, sr = librosa.load(filename)
    a = np.array(librosa.feature.rms(y=y,))
    rmse=np.mean(librosa.feature.rms(y)[0])
    os.remove(filename)
    return rmse*1000

minimum=0
maximum=70
samples=list()
for i in range(100):
    # record 20ms of data
    sample=record_data('sample.wav',0.02, 44100, 1)
    if sample > maximum:
        maximum=sample
        print('new max is %s'%(maximum))
    samples.append(sample)
    
samples=np.array(samples)
b = np.mean(samples)
minval=np.amin(samples)
maxval=np.amax(samples)
    
Threshold = b+10 #(minval+maxval)//2

SHORT_NORMALIZE = (1.0/32768.0)
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
swidth = 2

TIMEOUT_LENGTH = 5

f_name_directory = r'C:/Users/Admin/Anaconda3/Lib/site-packages'




class Recorder:

    @staticmethod
    def rms(frame):
        count = len(frame) / swidth
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * SHORT_NORMALIZE
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=chunk)

    def record(self):
        print('Noise detected, recording beginning')
        rec = []
        current = time.time()
        end = time.time() + TIMEOUT_LENGTH

        while current <= end:

            data = self.stream.read(chunk)
            if self.rms(data) >= Threshold: end = time.time() + TIMEOUT_LENGTH

            current = time.time()
            rec.append(data)
        self.write(b''.join(rec))

    def write(self, recording):
        n_files = len(os.listdir(f_name_directory))

        filename = os.path.join(f_name_directory, '{}.wav'.format(n_files))

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(recording)
        wf.close()
        print('Written to file: {}'.format(filename))
        print('Returning to listening')



    def listen(self):
        print('Listening beginning')
        while True:
            input = self.stream.read(chunk)
            rms_val = self.rms(input)
            if rms_val > Threshold:
                self.record()

a = Recorder()

a.listen()
