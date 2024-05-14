from array import *
#from machine import RTC
from machine import Timer
from playSound import WavFilePlayer
#import utime
import urequests
from lights import Light

#_rtc = RTC()

###
# Setup an Alarm
#
# All instanced of Alarm will be check every seconds through Alarmn._checkAlarm
# it is the responsibility of caller to call alarm.check with the time displayed "hh:mm"
# if the time match the alarm, the alarm will be flagged to be triggered 
class Alarm:

    __alarms = []

    @staticmethod
    def _checkAlarm(timer):
        for a in Alarm.__alarms:
            a.trigger()
            
    @staticmethod
    def __default_callback() -> bool:
        return False

    def __init__(self,id: int, sound: str):
        self.isOn = False  # this alarm is or not activated, if not activated it will never be triggered
        self.isSet = True  # the time of the alarm has been set
        self.hasRang = False # this alarm has rang, no need to trigger it again for the next 24h
        self.ring = False  # this alaram would be triggered ( an alarm sound will be emmitted)
        self.setTime = 0   # the time of the alarm in hhmm format
        self.fadeTime = 300 # 5 minutes fade time
        assert id < 100
        self.id = id # this alarm Id, used to persist on disk the alarm data
        self.lights = []
        Alarm.__alarms.append(self)
        self.sound = WavFilePlayer(sound)


    def addLight(self, l: Light)-> none:
        self.lights.append(l)

    def startFade(self, alarmInSec: int, now: bool=False)-> none:
        for l in self.lights:
            if l.isOff() and alarmInSec>=0 and (alarmInSec <= l.fadetime or now) :
                s = l.fadetime
                if now:
                    l.fadetime = alarmInSec
                l.fade()
                l.fadetime = s


    def setAlarm(self,setalarm: str):
        h = setalarm[0:2]
        m = setalarm[3:5]
        self.setTime = int(h)*100 + int(m)
        self.isSet = True
        self.hasRang = False
        self.ring = False

    def getAlarm(self) -> str:
        h = "{hour:02d}".format(hour= int(self.setTime / 100))
        m = "{minute:02d}".format(minute=int(self.setTime % 100))
        return h+":"+m

    def getAlarmValue(self,offset: int=0) -> int:
        h = self.setTime // 100
        m = self.setTime % 100 + offset
        while (m<0):
            h -= 1
            m += 60
        while (m>59):
            h += 1
            m -= 60
        return h*100+m

    def trigger(self):
        if self.ring:
            stopped = self.sound.play()
            if (stopped) :
                self.stop()

    def stop(self):
        if self.ring:
            self.ring = False
            self.hasRang = True

    def snoozeFunc(self, snoozePressed: Callable[[],bool]):
        self.sound.stopWhen(snoozePressed)

    def check(self,t: str):        
        if t == self.getAlarm():
            if self.isOn and not self.hasRang:
                self.ring = True
                self.hasRang = False
        else:
            self.hasRang = False

    def checkLights(self,timeInSec: int):        
        if self.isOn and not self.hasRang:
                self.startFade( self.getAlarmValue()* 100 - timeInSec)
                   
    def mock(self,t: str):
        self.setAlarm(t)
        if self.isOn and not self.hasRang:
            self.startFade(30,now=True)
            self.ring = True
            self.hasRang = False

    def load(self):
        try:
            filename  = 'alarm'+ '{id:02d}'.format(id=self.id)+'.txt'
            f = open(filename, 'r')
            strg = f.read()
            print(strg)
            self.setAlarm(strg[0:5])
            self.isSet = (strg[5:6] == '1')
            self.isOn = (strg[6:7] == '1')
            self.hasRang = (strg[7:8] == '1')
            self.ring = (strg[8:9] == '1')
            f.close()
        except OSError:
            print("*** Error loading "+filename)

    def store(self):
        try:
            filename  = 'alarm'+ '{id:02d}'.format(id=self.id)+'.txt'
            f = open(filename, 'w')
            f.write(self.getAlarm())
            f.write('{dat:1d}'.format(dat=self.isSet))
            f.write('{dat:1d}'.format(dat=self.isOn))
            f.write('{dat:1d}'.format(dat=self.hasRang))
            f.write('{dat:1d}'.format(dat=self.ring))
            f.close()
        except OSError:
            print("*** Error storing "+filename)

       
_timer_alarm = Timer()
_timer_alarm.init(freq=1, mode=Timer.PERIODIC, callback=Alarm._checkAlarm)
