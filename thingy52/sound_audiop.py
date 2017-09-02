import wave
import sys
import audioop
import binascii

wave_file_path = "audiop_output.wav"
# Get the fragments of ADPCM data:
# Here, blocks is an array of 259byte data represented as strings which is parsed
# from the ADPCM data file, write this according to the structure of your ADPCM file
block = getAdpcmFragments(adpcm_file_path)

#Set parameters for the wavefile according to your audio stream
wave_file = wave.open(wave_file_path, 'wb')
wave_file.setparams((2,2,16000, 0, 'NONE', 'NONE'))

# Using ASCII to Binary from the binascii lib to convert strings represented as e.g
# 4A, 6F etc into actual binary values. Then I am writing the linear PCM data from
# adpcm2lin to the wav-file.
state = None
for this in block:
pcm, state = audioop.adpcm2lin(binascii.a2b_hex(this), 4, state)
wave_file.writeframes(pcm)
