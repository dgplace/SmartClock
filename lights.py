from array import *
#from machine import RTC
from machine import Timer
#import utime
import urequests

class Light:

    def __init__(self, light: int, fadetime:int) -> None:
        self.light = light
        self.fadetime = fadetime
        self.isOn = False

    def fade(self) ->bool: 
        url = "http://<your-hue-bride-api>/lights/{l:01d}".format(l= self.light)
        response = urequests.get(url)
        if response.status_code == 200: # query success
        
            # print("JSON response:\n", response.text)
            
            # parse JSON
            parsed = response.json()
            current_brightness = parsed["state"]["bri"] 

            url = url + '/state'
            data = {"bri": 254, "on": True, "transitiontime": int(self.fadetime*10)}
            response = urequests.put(url, json=data)
            if response.status_code == 200: # query succes
                self.isOn = True
                return True                
        return False



    def checkLight(self) : 
        url = "http://<your-hue-bride-api>/lights/{l:01d}".format(l= self.light)
        response = urequests.get(url)
        if response.status_code == 200: # query success
        
            # print("JSON response:\n", response.text)
            
            # parse JSON
            parsed = response.json()
            current_on = parsed["state"]["on"]
            self.isOn = current_on                               
            
    def switchOn(self) : 
        url = "http://<your-hue-bride-api>/lights/{l:01d}".format(l= self.light)
        response = urequests.get(url)
        if response.status_code == 200: # query success
        
            # print("JSON response:\n", response.text)
            
            # parse JSON
            parsed = response.json()
            current_brightness = parsed["state"]["bri"] 

            url = url + '/state'
            data = {"bri": 254, "on": True, "transitiontime": int(10)}
            response = urequests.put(url, json=data)
            if response.status_code == 200: # query succes
                self.isOn = True


    def switchOff(self) : 
        url = "http://<your-hue-bride-api>/lights/{l:01d}".format(l= self.light)
        response = urequests.get(url)
        if response.status_code == 200: # query success
        
            # print("JSON response:\n", response.text)
            
            # parse JSON
            parsed = response.json()
            current_brightness = parsed["state"]["bri"] 

            url = url + '/state'
            data = {"bri": 254, "on": False, "transitiontime": int(10)}
            response = urequests.put(url, json=data)
            if response.status_code == 200: # query succes
                self.isOn = False


    def isOff(self) -> bool:
        return not self.isOn
