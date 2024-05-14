from array import *
from machine import RTC,Timer
import urequests,utime
import max7219,framebuf,display


#get time

class DisplayTime:

    _rtc = RTC()
    _timer_rtc = Timer()
    _url = "http://worldtimeapi.org/api/timezone/Australia/Brisbane" # see http://worldtimeapi.org/timezones
    _web_query_delay = 600000 # ms interval time of web JSON query
    _retry_delay = 5000 # ms interval time of retry after a failed Web query

    @staticmethod
    def update_rtctime(timer):

        response = urequests.get(DisplayTime._url)

        if response.status_code == 200: # query success
        
            # print("JSON response:\n", response.text)
            
            # parse JSON
            parsed = response.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[0:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))
        
            # update internal RTC
            DisplayTime._rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
            print("RTC updated\n")

    def __init__(self, screen):
        self.display = screen
        self.sep = True # H:M seprator shown
        self.lastShow = 0
        self.firstShow = 0
        self.lastTime = ""
        self.numbers = display.NumberDisplay()
        self.text = display.TextDisplay()
        DisplayTime._timer_rtc.init(period=DisplayTime._web_query_delay, callback=DisplayTime.update_rtctime)
        DisplayTime.update_rtctime(DisplayTime._timer_rtc)

    def getTime(self):
        t = "{4:02d}:{5:02d}".format(*DisplayTime._rtc.datetime())
        return t

    def getTimeValue(self):
        t = DisplayTime._rtc.datetime()[4]*100 + DisplayTime._rtc.datetime()[5]
        return t
        
    def getTimeValueSec(self):
        t = (DisplayTime._rtc.datetime()[4]*100 + DisplayTime._rtc.datetime()[5])*100 + DisplayTime._rtc.datetime()[6]
        return t
        
    def show(self):
        self.showTime(self.getTime())
        
    def showTime(self,t):        
        td = t # time to display

        if self.sep:
            td = t[0:2]+":"+t[3:5]
            if self.firstShow == 0:
                self.firstShow = utime.ticks_ms()
            if utime.ticks_ms() - self.firstShow >= 750: # sep been on for 250ms
                self.sep = False
                self.firstShow = 0
                self.lastShow = utime.ticks_ms()
        else:
            td = t[0:2]+" "+t[3:5]
            if utime.ticks_ms() - self.lastShow >= 250: # sep been on for 250ms
                self.sep = True
                self.firstShow = 0

        #show time if it changed
        if td != self.lastTime:
            self.display.fill(0)
            self.display.blit(self.numbers.fb(t[0]),26,1)
            self.display.blit(self.numbers.fb(t[1]),19,1)
            if td[2] == ":":
                self.display.blit(self.text.fb(":"),14,1)
            self.display.blit(self.numbers.fb(t[3]),7,1)
            self.display.blit(self.numbers.fb(t[4]),0,1)
            self.display.show()
            self.lastTime = td

    def showAlarn(self,isOn):        
        s = "alarm:off"
        if isOn:
            s = "alarm:on"
        self.display.blit(self.text.fb(s),0,2)
        self.display.show()

    def showLight(self):        
        s = "light"
        self.display.blit(self.text.fb(s),0,2)
        self.display.show()
