# Garden-Conditions-Monitor
  This project involves a Raspberry Pi 4, two Arduino Uno Boards, five YL-69 soil moisture sensors, five DHT-11 temperature and humidity sensors, 10 red or yellow LED bulbs, 10 blue LED bulbs, 20 220 ohm resistors, an LCD display, two Arduino USB cables, three breadboards, a potentiometer, and a way to display your RPi. One of the Arduinos reads the five DHT-11 modules. After interpreting the data into sensible temperature and humidity data with the DHT Arduino Library (which must be downloaded), the Arduino sends the data to the RPi through the Serial Monitor. The RPi reads the data with Python and graphs the temperature and humidity over a period of time. If the temperature or humidity is too low at one of the five sensors for the type of plants the person is growing,  the RPi will turn on a blue LED. If the temperature or humidity are too high, then a red LED will turn on.  Each station has a red and blue LED associated with it. An LCD display connected to the Arduino will display the current temperature and humidity  
  The second Arduino reads five YL-69 sensors. Because these sensors act as resistors, values collected from these sensors on a scale of 0 - 1023 with analogRead() in Arduino. These values are read directly into the RPi, where they are read in Python and send a message to user of the relative dryness of the soil on a scale, based on the fact that perfect dry soil is 1023(no conductivity across the sensor) and totally saturated soil is 0(perfect conductivity, or in water). 
  Future work will include a separate LED signal system for the humidity and temperature, but this was not accomplished due to a lack of space on the RPi GPIO pins. Another LCD Display will be added on for the soil moisture Arduino, but this was not accomplished in the initial assembly of the project due to a lack of breadboard space and available wires.
Some references I used:
Plotting data with multiple subplots:
https://matplotlib.org/devdocs/gallery/subplots_axes_and_figures/subplots_demo.html

Reading Arduino YL-69 sensors:
https://randomnerdtutorials.com/guide-for-soil-moisture-sensor-yl-69-or-hl-69-with-the-arduino/

Reading Arduino DHT-11 sensors:
https://electronicsprojectshub.com/setup-dht11-sensor-with-arduino/

Reading Arduino into Python:
https://www.instructables.com/id/Sending-Data-From-Arduino-to-Python-Via-USB/

Lighting LEDs with RPi GPIO pins:
CanaKit Raspberry Pi 4 Quick-Start Guide

Using GPIO pins on RPi:
https://raspi.tv/2013/rpi-gpio-basics-5-setting-up-and-using-outputs-with-rpi-gpio

LCD display in Arduino:
https://www.instructables.com/id/How-to-use-an-LCD-displays-Arduino-Tutorial/
