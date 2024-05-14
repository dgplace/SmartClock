![Image](https://github.com/dgplace/SmartClock/blob/main/IMG_0371.jpeg)

Code for Alarm clock using 64x8 Matrix LED & RaspberryPi Pico W.

You can use Thonny to upload to you Raspeberry Pi Pico (https://thonny.org)
You need to deploy all the files.

If you have a hue bridge, it can be configured to switch on (fade in) a few lights when the alarm trigger.
The 4th button of the clock toggle those lights.

You'll need to know the ID & API URL of the light you want to switch (See https://developers.meethue.com/develop/get-started-2/)

The raspeberry pi need a Pico-Audio attached to it (https://www.waveshare.com/pico-audio.htm)

Features & Customisation required:
* Add your wifi detail in main.py (line 52) so date/time can be read from internet.
* Set your timezone in DisplayTime.py (line 18)
* Set the huebridge URL in lights.py (need to be entered 4x, looks like: http://192.168.0.22/api/sjdfhskhs-dferreg-gfergerg68532HDJgNnbF)
* The ID of light to switch on is confirgured in main.py (Line 66-68) and make sure they added in line 82-84
* The clock is configure to not display the time between 21:00 and 05:00, this can be confirgured in main.py (Line 146 and 148)
* The pinout for the button are configured in main.py Line 22-25
* The pinout for the LED matrix in main.py line 33-34

Enjoy.



