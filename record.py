import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt
#import scipy.signal as signal
import wave
import sys
#import pylab
import time
import msvcrt
from subprocess import call
import os
import argparse

print('\n\t\t------ Starting record.py ------')
parser = argparse.ArgumentParser(description='record wave files from default pc mic input',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-outwave', type=str, default='record.wav',
                    help='Name or path of output recording wave file')
parser.add_argument('-channels', type=int, default=2,
                    help='1, 2 or more channels to record')
parser.add_argument('-rate', type=int, default=48000,
                    help='unit in Hz use 44100 for cd quality, 48000 for studio, 88200 for cd doubled, 96000 for extra quality, or whatever')
parser.add_argument('-bit', type=int, default=32,
                    help='16 24 or 32. 16 bit for cd, 24/32 for recording. How many values to represent the recording')
parser.add_argument('-chunk', type=int, default=10240,
                    help='Each chunk of data to be read for each loop.')
parser.add_argument('-ovr', action='store_true',
                    help='This option overwrites the output wave, defaut is to rename it.')
parser.set_defaults(ovr=False)
parser.add_argument('-tempfile', type=str, default='create',
                    help='Temporary byte file to be created before writing the real wave file. Use a drive with high velocity and plenty of space')
parser.add_argument('-delay', type=int, default=0,
                    help='How many seconds to wait before start recording')
parser.add_argument('-playback', action='store_true',
                    help='if especified, it will playback the audio in the mic to the speakers')
parser.set_defaults(playback=False)

args = parser.parse_args()
outwave = args.outwave
channels = args.channels
rate = args.rate
bit = args.bit
chunk = args.chunk
ovr = args.ovr
tempfile = args.tempfile
delay = args.delay
playback = args.playback

p = pyaudio.PyAudio()
dry_data = np.array([])
window = np.blackman(chunk*channels)

if bit == 32:
    FORMAT = pyaudio.paInt32
    npformat = np.int32
elif bit == 16:
    FORMAT = pyaudio.paInt16
    npformat = np.int16
elif bit == 24:
    FORMAT = pyaudio.paInt24
    npformat = np.uint8

if os.path.isfile(outwave):
    if ovr == True:    
        print('\n deleted file {}'.format(outwave))
        call('del {}'.format(outwave),shell=True)
    if ovr == False:
        numb = 2
        outwave = outwave[:-4]+'_{}.wav'.format(numb)
        while os.path.isfile(outwave):
            outwave = outwave[:-4]+'_{}.wav'.format(numb)
        print('\n file already exists renaming to {}'.format(outwave))

if 'create' in tempfile:
    tempfile = outwave.split('.')[0]+'.temp'

if os.path.isfile(tempfile):
    call('del {}'.format(tempfile),shell=True)

def callback(in_data, frame_count, time_info, flag):
    global dry_data,tempfile,playback
    dry_data = in_data
    with open(tempfile,'ab') as tempaudio:
        tempaudio.write(in_data)
    if playback == False:
        in_data = None
    return (in_data, pyaudio.paContinue)

def soundPlot(dry_data,ax1,channels,sampwidth,bit):
    try:
        npArrayData = np.fromstring(dry_data, dtype=npformat)
        indata = npArrayData*window
        ax1.cla()
        ax1.plot(indata)
        ax1.grid()
        if bit == 32:
            ax1.axis([0,len(indata),-10**8,10**8])
        elif bit == 16:
            ax1.axis([0,len(indata),-10**3,10**3])
        plt.pause(0.0000000000000000000000000000000000000000000000000000000000000000000000000000001)
    except Exception:
        print('bad numpy')

def main():
    if not delay == 0:
        time.sleep(delay)
    sampwidth_val = p.get_sample_size(FORMAT)
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=rate,
                    output=playback,
                    input=True,
                    frames_per_buffer=chunk,
                    stream_callback=callback)
    if not bit == 24:        
        plt.ion()
        fig = plt.figure(figsize=(15,5))
        ax1 = fig.add_subplot(211)
    stream.start_stream()
    done = False
    print('\n recording until you press some key in keyboard ...')
    while not done and stream.is_active():
        if len(dry_data) == 0:
            continue
        if not bit == 24:
            soundPlot(dry_data,ax1,channels,sampwidth_val,bit)
        if msvcrt.kbhit():
            print ("\n you pressed",msvcrt.getch()," converting temp to wave!")
            done = True
    if not bit == 24:
        plt.close('all')
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(outwave, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(rate)
    with open(tempfile,'rb') as tempaudio:
        audiodata = tempaudio.read(chunk*channels)
        while audiodata:
            wf.writeframes(audiodata)
            audiodata = tempaudio.read(chunk*channels)
    
    wf.close()

    print('\n\t\t------ Finished record.py ------')
if __name__ == "__main__":
    main()