import pyaudio
import wave
from array import array




CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECOND = 5
WAVE_OUTPUT_FILENAME = "output.wav"
RECORD_SECONDS=14400
FILE_NAME="RECORDING.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECOND)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()




audio=pyaudio.PyAudio() #instantiate the pyaudio

#recording prerequisites
stream=audio.open(format=FORMAT,channels=CHANNELS, 
                  rate=RATE,
                  input=True,
                  frames_per_buffer=CHUNK)

#starting recording
frames=[]

for i in range(0,int(RATE/CHUNK*RECORD_SECONDS)):
    data=stream.read(CHUNK)
    data_chunk=array('h',data)
    vol=max(data_chunk)
    if(vol>=500):
        print("something said")
        frames.append(data)
    else:
        print("nothing")
    print("\n")


#end of recording
stream.stop_stream()
stream.close()
audio.terminate()
#writing to file
wavfile=wave.open(FILE_NAME,'wb')
wavfile.setnchannels(CHANNELS)
wavfile.setsampwidth(audio.get_sample_size(FORMAT))
wavfile.setframerate(RATE)
wavfile.writeframes(b''.join(frames))#append frames recorded to file
wavfile.close()
