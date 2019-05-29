# Audio recording with python

Any comments and suggestions are apreciated

## Install pyaudio and others dependencies

```pip install pyaudio```

and repeat for others modules that may be needed like matplotlib, etc

## Simple usage

on command line type to start recording:

```python record.py```

just press any key to stop

## Advanced settings
There are a few other options that can be provided, you can check with 

```python record.py -h```

examples are:

```python record.py -outwave beatles.wav -bit 16 -playback```


    usage: record.py [-h] [-outwave OUTWAVE] [-channels CHANNELS] [-rate RATE]
                     [-bit BIT] [-chunk CHUNK] [-ovr] [-tempfile TEMPFILE]
                     [-delay DELAY] [-playback]
    
    record wave files from default pc mic input
    
    optional arguments:
      -h, --help          show this help message and exit
      -outwave OUTWAVE    Name or path of output recording wave file (default:
                          record.wav)
                          
      -channels CHANNELS  1, 2 or more channels to record (default: 2)
    
      -rate RATE          unit in Hz use 44100 for cd quality, 48000 for studio,
                          88200 for cd doubled, 96000 for extra quality, or
                          whatever (default: 48000)
    
      -bit BIT            16 24 or 32. 16 bit for cd, 24/32 for recording. How
                          many values to represent the recording (default: 32)
    
      -chunk CHUNK        Each chunk of data to be read for each loop. (default:
                          10240)
    
      -ovr                This option overwrites the output wave, defaut is to
                          rename it. (default: False)
    
      -tempfile TEMPFILE  Temporary byte file to be created before writing the
                          real wave file. Use a drive with high velocity and
                          plenty of space (default: create)
    
      -delay DELAY        How many seconds to wait before start recording
                          (default: 0)
    
      -playback           if especified, it will playback the audio in the mic to
                          the speakers (default: False)
