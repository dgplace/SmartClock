from machine import Timer
from array import *
import utime


class Button:
    @staticmethod
    def checkButton():
        for b in _btn:
            b.check()

    @staticmethod
    def _checkButton(timer):
        Button.checkButton()

    def __init__(self,button):
        self.isOn = False
        self.isHold = False
        self.isChecked = False
        self.repeating = False
        self.button = button
        self.holdTime = 3000 # Hold state on after 250ms
        self.repeat = 750 # repeat after 1000ms
        self.pushTime = utime.ticks_ms()
        _btn.append(self)

    def check(self):
        if self.button.value():
            if not self.isOn:
                self.isOn = True
                self.isChecked = True
                self.pushTime = utime.ticks_ms()
            else:
                if utime.ticks_ms() - self.pushTime > self.repeat:
                    self.repeating = True
                elif utime.ticks_ms() - self.pushTime > self.holdTime:
                    self.isHold = True
        else:
            self.isOn = False
            self.isHold = False
            self.repeating = False
            self.isChecked = False

    def checkOnce(self):
        ret = self.isChecked or self.repeating
        self.isChecked = False
        return ret


_btn = []
_timer = Timer()
_timer.init(freq=20, mode=Timer.PERIODIC, callback=Button._checkButton)
