from machine import Pin, Timer, SPI
import network,time,urequests,utime
from machine import RTC, I2C, Pin
import framebuf
from button import Button
from alarm import Alarm
from DisplayTime import DisplayTime
from array import *
import max7219
from lights import Light

global fb
# internal real time clock
ALARM = const(1)
TIME = const(2)
SETTING = const(3)

led = Pin("LED", Pin.OUT)

timer = Timer()

btn1 = Button(Pin(14, Pin.IN, Pin.PULL_DOWN))
btn2 = Button(Pin(13, Pin.IN, Pin.PULL_DOWN))
btn3 = Button(Pin(12, Pin.IN, Pin.PULL_DOWN))
btn4 = Button(Pin(15, Pin.IN, Pin.PULL_DOWN))

def blink(timer):
    led.toggle()

#initialisation. blink onboard led fast
timer.init(freq=20, mode=Timer.PERIODIC, callback=blink)

spi = SPI(0,sck=Pin(2),mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi,cs,4)
display.brightness(0)
display.fill(1)
display.show()

###
#  connect to Lan
###
wlan = network.WLAN(network.STA_IF) #initialize the wlan object
wlan.active(True) #activates the wlan interface
accessPoints = wlan.scan() #perform a WiFi Access Points scan
# set power mode to get WiFi power-saving off (if needed)
wlan.config(pm = 0xa11140)

################
################ ADD YOUR WIFI DETAILS BELOW
################
wlan.connect('<your wifi name>', '<your wifi password>')

while not wlan.isconnected() and wlan.status() >= 0:
   print("Waiting to connect:")
   time.sleep(1)

print("Connected.")

displayTime = DisplayTime(display)

###
### Define Lights
###

l1 = Light(5, fadetime=5*60) 
l2 = Light(2, fadetime=5*60) 
l3 = Light(3, fadetime=5*60) 

###
### Define Alarms
###

alrm = Alarm(1,"alarm8db.wav")

def checkSnooze()->bool:
    Button.checkButton()
    return (btn1.isOn or btn2.isOn or btn3.isOn or btn4.isOn)

alrm.load()    
alrm.snoozeFunc(checkSnooze)
alrm.addLight(l1)
alrm.addLight(l2)
#alrm.addLight(l3)

#init done, blink onborad led slowly
timer.init(freq=1, mode=Timer.PERIODIC, callback=blink)

mode = TIME
bn = 0
mock = False
somethinOnScreen = True
active = 0
toggleLight = False

# main loop
while True:
    # if lose wifi connection, reboot ESP8266
    # if not wlan.isconnected():
    #    machine.reset()

    if btn1.isOn or btn2.isOn or btn3.isOn or btn4.isOn:  # show time if any button pressed 
        active = utime.ticks_ms() 

    if btn1.isOn and not btn2.isOn and not btn3.isOn and not btn4.isOn: # bt1 pushed, entering alarm mode
        mode = ALARM
        
    if not btn1.isOn and btn2.isOn and not btn3.isOn and not btn4.isOn:
        mode = SETTING

    if not btn1.isOn and not btn2.isOn and not btn3.isOn and not btn4.isOn:
        if mock:
            mock = False
            alrm.mock(displayTime.getTime())

        if mode == ALARM: # exiting from alarm mode
            alrm.store()
        mode = TIME

    if mode == TIME:
        
        if not btn1.isOn and not btn2.isOn:
            if btn3.checkOnce() :
                bn = ((bn + 1) % 2 ) * 15
                display.brightness(bn)
            
            if btn4.checkOnce() :
                display.fill(0)
                displayTime.showLight()
                l2.checkLight()
                if l2.isOff():
                    #switch on the lights
                    l2.switchOn()
                    l1.switchOn()
                else:
                    #switch off
                    l2.switchOff()
                    l1.switchOff()
                display.fill(0)
                display.show()
            
        alrm.check(displayTime.getTime())
        alrm.checkLights(displayTime.getTimeValueSec())

        showtime = alrm.getAlarmValue(-10) # show clock 10 minutes before alarm, or from 7am
        bedtime = 2100 # don't show time after 21:00 
        thetime = displayTime.getTimeValue()
        showClock = (utime.ticks_ms() - active < 5000)
        if showtime> bedtime: 
            if thetime >= showtime or thetime < bedtime:
                showClock = True
        if showtime <= bedtime: 
            if displayTime.getTimeValue() >= showtime and displayTime.getTimeValue() <= bedtime:
                showClock = True

        if showClock:
            somethinOnScreen = True
            displayTime.show()
        else: # past 9pm, don't display the time
            if somethinOnScreen: # only clear screen if something is displayed
                display.fill(0)
                if alrm.isOn:
                    display.pixel(0,0,1)
                display.show()
                somethinOnScreen = False

    elif mode == ALARM:
        
        somethinOnScreen = True
        if btn2.checkOnce():
            alrm.setTime = (alrm.setTime + 100) % 2400
        if btn3.checkOnce():
            m = alrm.setTime % 100
            m = (m-1+60) % 60
            alrm.setTime = int(alrm.setTime/100)*100 + m
        if btn4.checkOnce():
            m = alrm.setTime % 100
            m = (m+1) % 60
            alrm.setTime = int(alrm.setTime/100)*100 + m
            
        t = alrm.getAlarm()
        displayTime.showTime(t)

    elif mode == SETTING:

        somethinOnScreen = True
        display.fill(0)
        displayTime.showAlarn(alrm.isOn)
        
        if btn3.checkOnce():
            alrm.isOn = not alrm.isOn
            alrm.store()

        if btn1.checkOnce():
            print("Mocking alarm")
            mock = True

    utime.sleep(0.1) # refresh display every 0.1 seconds, this affect how button repeats
