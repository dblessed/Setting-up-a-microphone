import wave
import pyaudio
import numpy as np
import pylab
 
import pylab as pl
 
# calculate the energy of 256 samples per frame as a frame
def rmsEnergy(wave_data) :
    energy = []
    sum = 0
    for i in range(len(wave_data)) :
        sum = sum + (int(wave_data[i]) * int(wave_data[i]))
        if (i + 1) % 256 == 0 :
            energy.append(sum)
            sum = 0
        elif i == len(wave_data) - 1 :
            energy.append(sum)
    return energy
 
 
 
 
 
f=wave.open("C:/Users/Admin/Anaconda3/Lib/delme_rec_unlimited_ian0oqjd.wav","rb")
# getparams() 一time of return format information for all of the WAV files
params = f.getparams()
# nframes sampling points
nchannels, sampwidth, framerate, nframes = params[:4]
# readframes()  reading data by sampling point
str_data = f.readframes(nframes)            # str_data Is a binary string
 
# The above can be written directly as str_data = f.readframes(f.getnframes())
 
# Into a two-byte array (two bytes per sample point)
wave_data = np.frombuffer(str_data, dtype = np.short)
print( "Number of sampling points：" + str(len(wave_data)))          #The output should be the number of samples
f.close()
 
 
 
energy = rmsEnergy(wave_data)
 
 
time = np.arange(0, len(wave_data)) * (1.0 / framerate)
time2 = np.arange(0, len(energy)) * (len(wave_data)/len(energy) / framerate)
pl.subplot(211)
pl.plot(time, wave_data)
pl.ylabel("Amplitude")
pl.subplot(212)
pl.plot(time2, energy)
pl.ylabel("short energy")
pl.xlabel("time (seconds)")
pl.show()
 
 
print("Short-term energy：",energy)
