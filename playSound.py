# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:  Play a pure audio tone out of a speaker or headphones
#
# - write audio samples containing a pure tone to an I2S amplifier or DAC module
# - tone will play continuously in a loop until
#   a keyboard interrupt is detected or the board is reset
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S

import os
import math
import struct
from machine import I2S
from machine import Pin
import wave
import time

class WavFilePlayer:
    _SCK_PIN = 27
    _WS_PIN = 28
    _SD_PIN = 26
    _I2S_ID = 0
    _BUFFER_LENGTH_IN_BYTES = 512

    @staticmethod
    def __default_cb()->bool:
        return False

    def __init__(self,waveFilename: str="alarm8db.wav"):

        self.WAV_FILE = waveFilename
        f = wave.open(waveFilename,'rb')
        self.rate = f.getframerate()
        self.bytesDepth = f.getsampwidth()
        self.channels = f.getnchannels()
        self.callback = WavFilePlayer.__default_cb
        if self.channels > 1:
            self.FORMAT = I2S.STEREO
        else:
            self.FORMAT = I2S.MONO
        f.close()

    def stopWhen(self,callback: Callable[[],bool]):
        self.callback =callback

    def play(self) -> bool:
        hasStopped = False
        _audio_out = I2S(
            WavFilePlayer._I2S_ID,
            sck=Pin(WavFilePlayer._SCK_PIN),
            ws=Pin(WavFilePlayer._WS_PIN),
            sd=Pin(WavFilePlayer._SD_PIN),
            mode=I2S.TX,
            bits=self.bytesDepth*8,
            format=self.FORMAT,
            rate=self.rate,
            ibuf=WavFilePlayer._BUFFER_LENGTH_IN_BYTES*self.bytesDepth*self.channels,
        )

        f = wave.open(self.WAV_FILE ,'rb')
            
        frameCount = f.getnframes()

        frameLeft = frameCount
        nbFrame = WavFilePlayer._BUFFER_LENGTH_IN_BYTES
        nbData = nbFrame*self.bytesDepth

        while frameLeft > 0:
        # first DMA
            if frameLeft < nbFrame:
                nbFrame = frameLeft
                nbData = nbFrame*self.bytesDepth
            t1 = f.readframes(nbFrame)
            _audio_out.write(t1[:nbData])
            if self.callback():
                hasStopped = True
                break
            frameLeft -= nbFrame 

        f.close()
        _audio_out.deinit()

        return hasStopped

