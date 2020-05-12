# -*- coding: utf-8 -*-
"""
Created on Thu May  7 23:14:31 2020

@author: geroj
"""

'''
Author: Jacob Gero, Original finished 26 April 2020
RPi GPIO extention: Finished 30 April 2020
Testing: Finished 7 May 2020

This code imports data from arduino code, which simultaneously collects
data from five DHT-11 (temperature and humidity sensors) and five YL-69 (soil moisture sensors).
The Arduino code writes to the serial monitor, which this code reads and interprets. 
The user has to choose between growing peas, 
beans, squash, corn, tomatoes, or has the option of growing his/her own input of crop. The program
will tell the user if any of the modules 

This code uses the GPIO pins to turn on LED pins that signal if the crop's humidity levels are too high or low, temperature
is too high or low, or if the soil is too dry or wet. This code DOES NOT run from a laptop connected to the 
two arduinos, unless the RPi.GPIO library is installed for some reason. Comment out the RPi library and any GPIO mentions 
within the program and the program should run fine and interpret/plot data from your laptop.

Known bugs: Not that I am aware of, I tested this program multiple times and caught I believe most. I won't promise there aren't any.
'''
import RPi.GPIO as GPIO #For LED signals
import sys #Used for sys.exit()
import serial as serial #Used to read serial monitor
import time #Used for time.sleep()
import matplotlib.pyplot as plt #Used to plot the data.

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Set up RPi pins for humid/temp signals. All initially low.
#Future work includes setting up seperate lighting system for humidity meausurements.
#The reason this wasn't implemented was due to a lack of time, lack of LEDs to use, 
#and a lack of RPi GPIO pins.
GPIO.setup(16,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(12,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(26,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(13,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(6,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(5,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(22,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(27,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(17,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(4,GPIO.OUT,initial = GPIO.LOW)
#Set up RPi pins for soil moisture signals
#These pins should be better organized in the future.
GPIO.setup(21,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(20,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(19,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(11,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(9,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(10,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(7,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(8,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(24,GPIO.OUT,initial = GPIO.LOW)
GPIO.setup(23,GPIO.OUT,initial = GPIO.LOW)
'''
This reads the serial port for the Arduino reading the DHT-11 sensors. Error catches if port not connected
or if there is some issue with reading the serial port. A common error is the Serial Monitor window being open
from the Arduino IDE at the same time you attempt to run this code.
'''
try:
    arduino = serial.Serial('/dev/ttyACM1',9600) #interprets RPi port, which connects to the Arduino reading the DHT-11 sensors.
except serial.SerialException:
    print("No Arduino. Please check your port and try again.") #Rather than crashing, the program will error catch
    time.sleep(2)
    sys.exit()

'''
Same as above,  only this module reads the serial port where the arduino reading the YL-69 sensors is attached.
Ensure these ports are not confused. Run both Arduino codes at once by opening up the Arduino IDE two seperate times,
and opening the two codes in the respective windows. Then you will be able to run the two codes at once from different ports.
'''
try:
    arduino2 = serial.Serial('/dev/ttyACM0',9600) #interprets second RPi port, which connects to the Arduino reading the YL 69 sensors.
except serial.SerialException:
    print("No Arduino2. Please check your port and try again.")
    time.sleep(2) #Allows user to read message for two seconds
    arduino.close() #If COM4 has already been opened to be read, the program will close the program before ending.
    sys.exit()#closes program.


'''
Method: q()
Author: Jacob Gero

This method offers the quite function when a program has completed. It accepts appropriate yes or no options.
If the user types an invalid input, the program will run again until yes or no is entered. If no if chosen,
the user 
'''
def q():
    print("Would you like to run again? y/n")
    yn = input("")
    arduino.close()
    arduino2.close()
    if yn in ['y','yes','Yes','y']:
        arduino.open()
        arduino2.open()
        main()
    if yn in ['no','n','N','No']:
        print("Thank you!")
        time.sleep(2)
        sys.exit()
    else:
        print("Not a valid response.")
        q()

'''
Module: helpfulPlanner
Author: Jacob Gero

This module runs in a similar fashion to the single planner modules, 
in that it reads the Arduino inputs and segregates the data into temperature,
humidity, and soil moisture arrays and interprets it and plots it on a graph over
a certain period of minutes, which the user inputs. Howevertthis module, the user
decides what he/she is planting for each station, and thus the parameters are different for
each station.

'''
def helpfulPlanner():
    data1 = []
    
    print("Hello! Here are some options for vegetables: ")
    print("1) Tomatoes")
    print("2) Beans")
    print("3) Peas")
    print("4) Corn")
    print("5) Squash")
    print("6) Other")
    print("7) I am not planting in this station.")
    
    print("Which of these are you planting for station 1?")
    userVeg1 = input("")
    if userVeg1 in ['1)','1','Tomatoes','tomatoes']:
        data1.append("Tomatoes")
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg1 in ['2','2)','Beans','beans']:
        data1.append("Beans")
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg1 in ['3','3)','Peas','peas']:
        data1.append("Peas")
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg1 in ['4','4)','Corn','corn']:
        data1.append("Corn")
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg1 in ['5','5)','Squash','squash']:
        data1.append("Squash")
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg1 in ['6','6)','Other','other']:
        print("What vegetable will you grow instead?")
        V1 = input("")
        data1.append(V1)
        try:
            print("What is the minimum accepted temperature in celsius?")
            TempMin1 = float(input(""))
            TempMinF1 = TempMin1*(9/5)+32
            print("What is the maximum accepted temperature in celsius?")
            TempMax1 = float(input(""))
            TempMaxF1 = TempMax1*(9/5)+32
            print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
            HumMin1 = float(input(""))
            print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
            HumMax1 = float(input(""))
        except ValueError:
            print("Invalid input. Please try again.")
            helpfulPlanner()
    elif userVeg1 in ['7','7)','I am not planting in this station']:
        data1.append("Nothing")
    else:
        print("Please select a correct option.")
        helpfulPlanner()
        
    print("Which of these are you planting for station 2?")
    userVeg2 = input("")
    if userVeg2 in ['1)','1','Tomatoes','tomatoes']:
        data1.append("Tomatoes")
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg2 in ['2','2)','Beans','beans']:
        data1.append("Beans")
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg2 in ['3','3)','Peas','peas']:
        data1.append("Peas")
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg2 in ['4','4)','Corn','corn']:
        data1.append("Corn")
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg2 in ['5','5)','Squash','squash']:
        data1.append("Squash")
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg2 in ['6','6)','Other','other']:
        print("What vegetable will you grow instead?")
        V2 = input("")
        data1.append(V2)
        try:
            print("What is the minimum accepted temperature in celsius?")
            TempMin2 = float(input(""))
            TempMinF2 = TempMin2*(9/5)+32
            print("What is the maximum accepted temperature in celsius?")
            TempMax2 = float(input(""))
            TempMaxF2 = TempMax2*(9/5)+32
            print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
            HumMin2 = float(input(""))
            print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
            HumMax2 = float(input(""))
        except ValueError:
            print("Invalid input. Please try again.")
            helpfulPlanner()
    elif userVeg2 in ['7','7)','I am not planting in this station']:
        data1.append("Nothing")
    else:
        print("Please select an option.")
        helpfulPlanner()
        
    print("Which of these are you planting for station 3?")
    userVeg3 = input("")
    if userVeg3 in ['1)','1','Tomatoes','tomatoes']:
        data1.append("Tomatoes")
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg3 in ['2','2)','Beans','beans']:
        data1.append("Beans")
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg3 in ['3','3)','Peas','peas']:
        data1.append("Peas")
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg3 in ['4','4)','Corn','corn']:
        data1.append("Corn")
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg3 in ['5','5)','Squash','squash']:
        data1.append("Squash")
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg3 in ['6','6)','Other','other']:
        print("What vegetable will you grow instead?")
        V3 = input("")
        try:
            print("What is the minimum accepted temperature in celsius?")
            TempMin3 = float(input(""))
            TempMinF3 = TempMin3*(9/5)+32
            print("What is the maximum accepted temperature in celsius?")
            TempMax3 = float(input(""))
            TempMaxF3 = TempMax3*(9/5)+32
            print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
            HumMin3 = float(input(""))
            print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
            HumMax3 = float(input(""))
            data1.append(V3)
        except ValueError:
            print("Invalid input. Please try again.")
            helpfulPlanner()
    elif userVeg3 in ['7','7)','I am not planting in this station']:
        data1.append("Nothing")
    else:
        print("Please select an option.")
        helpfulPlanner()
        
    print("Which of these are you planting for station 4?")
    userVeg4 = input("")
    if userVeg4 in ['1)','1','Tomatoes','tomatoes']:
        data1.append("Tomatoes")
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg4 in ['2','2)','Beans','beans']:
        data1.append("Beans")
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg4 in ['3','3)','Peas','peas']:
        data1.append("Peas")
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg4 in ['4','4)','Corn','corn']:
        data1.append("Corn")
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg4 in ['5','5)','Squash','squash']:
        data1.append("Squash")
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg4 in ['6','6)','Other','other']:
        print("What vegetable will you grow instead?")
        V4 = input("")
        try:
            print("What is the minimum accepted temperature in celsius?")
            TempMin4 = float(input(""))
            TempMinF4 = TempMin4*(9/5)+32
            print("What is the maximum accepted temperature in celsius?")
            TempMax4 = float(input(""))
            TempMaxF4 = TempMax4*(9/5)+32
            print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
            HumMin4 = float(input(""))
            print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
            HumMax4 = float(input(""))
            data1.append(V4)
        except ValueError:
            print("Invalid input. Please try again.")
            helpfulPlanner()
    elif userVeg4 in ['7','7)','I am not planting in this station']:
        data1.append("Nothing")
    else:
        print("Please select an option.")
        helpfulPlanner()
        
    print("Which of these are you planting for station 5?")
    userVeg5 = input("")
    if userVeg5 in ['1)','1','Tomatoes','tomatoes']:
        data1.append("Tomatoes")
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg5 in ['2','2)','Beans','beans']:
        data1.append("Beans")
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg5 in ['3','3)','Peas','peas']:
        data1.append("Peas")
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg5 in ['4','4)','Corn','corn']:
        data1.append("Corn")
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
    elif userVeg5 in ['5','5)','Squash','squash']:
        data1.append("Squash")
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
    elif userVeg5 in ['6','6)','Other','other']:
        print("What vegetable will you grow instead?")
        V5 = input("")
        try:
            print("What is the minimum accepted temperature in celsius?")
            TempMin5 = float(input(""))
            TempMinF5 = TempMin5*(9/5)+32
            print("What is the maximum accepted temperature in celsius?")
            TempMax5 = float(input(""))
            TempMaxF5 = TempMax5*(9/5)+32
            print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
            HumMin5 = float(input(""))
            print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
            HumMax5 = float(input(""))
            data1.append(V5)
        except ValueError:
            print("Invalid input. Please try again.")
            helpfulPlanner()
    elif userVeg5 in ['7','7)','I am not planting in this station']:
        data1.append("Nothing")
    else:
        print("Please select an option.")
        helpfulPlanner()
    
    print("For station 1, you are planting ", data1[0])
    print("For station 2, you are planting ", data1[1])
    print("For station 3, you are planting ", data1[2])
    print("For station 4, you are planting ", data1[3])
    print("For station 5, you are planting ", data1[4])
    print("If the above is true, press any key to continue, or type 'r' to restart. Type 'Q' to quit.")
    g = input("")
    if g in ['Q','q','quit','Quit']:
        q()
    elif g in ['r']:
        helpfulPlanner()
    else:
        print("Continuing with monitoring your garden!")
        
        
    if data1[0] in ['Tomatoes']:
        HumMin1 = 40
        HumMax1 = 80
        TempMin1 = 18.3
        TempMinF1 = TempMin1*(9/5)+32
        TempMax1 = 29.4
        TempMaxF1 = TempMax1*(9/5)+32
    elif data1[0] in ['Beans']:
        HumMin1 = 40
        HumMax1 = 80
        TempMin1 = 21 
        TempMinF1 = TempMin1*(9/5)+32
        TempMax1 = 29.4
        TempMaxF1 = TempMax1*(9/5)+32
    elif data1[0] in ['Corn']:
        HumMin1 = 40
        HumMax1 = 80
        TempMin1 = 25
        TempMinF1 = TempMin1*(9/5)+32
        TempMax1 = 32.8
        TempMaxF1 = TempMax1*(9/5)+32
    elif data1[0] in ['Squash']:
        HumMin1 = 40
        HumMax1 = 60
        TempMin1 = 21
        TempMinF1 = TempMin1*(9/5)+32
        TempMax1 = 29.4
        TempMaxF1 = TempMax1*(9/5)+32
    elif data1[0] in ['Peas']:
        HumMin1 = 40
        HumMax1 = 60
        TempMin1 = 10
        TempMinF1 = TempMin1*(9/5)+32
        TempMax1 = 21
        TempMaxF1 = TempMax1*(9/5)+32
    elif data1[0] in ['Nothing']:
        HumMin1 = None
        HumMax1 = None
        TempMin1 = None
        TempMax1 = None
    elif data1[0] in ['Other']:
       print("")
        
    if data1[1] in ['Tomatoes']:
        HumMin2 = 40
        HumMax2 = 80
        TempMin2 = 18.3
        TempMinF2 = TempMin2*(9/5)+32
        TempMax2 = 29.4
        TempMaxF2 = TempMax2*(9/5)+32
    elif data1[1] in ['Beans']:
        HumMin2 = 40
        HumMax2 = 80
        TempMin2 = 21
        TempMinF2 = TempMin2*(9/5)+32
        TempMax2 = 29.4
        TempMaxF2 = TempMax2*(9/5)+32
    elif data1[1] in ['Corn']:
        HumMin2 = 40
        HumMax2 = 80
        TempMin2 = 25
        TempMinF2 = TempMin2*(9/5)+32
        TempMax2 = 32.8
        TempMaxF2 = TempMax2*(9/5)+32
    elif data1[1] in ['Squash']:
        HumMin2 = 40
        HumMax2 = 60
        TempMin2 = 21
        TempMinF2 = TempMin2*(9/5)+32
        TempMax2 = 29.4
        TempMaxF2 = TempMax2*(9/5)+32
    elif data1[1] in ['Peas']:
        HumMin2 = 40
        HumMax2 = 60
        TempMin2 = 10
        TempMinF2 = TempMin2*(9/5)+32
        TempMax2 = 21
        TempMaxF2 = TempMax2*(9/5)+32
    elif data1[1] in ['Nothing']:
        HumMin2 = None
        HumMax2 = None
        TempMin2 = None
        TempMax2 = None
    elif data1[1] in ['Other']:
        print("")
        
    if data1[2] in ['Tomatoes']:
        HumMin3 = 40
        HumMax3 = 80
        TempMin3 = 18.3
        TempMinF3 = TempMin3*(9/5)+32
        TempMax3 = 29.4
        TempMaxF3 = TempMax3*(9/5)+32
    elif data1[2] in ['Beans']:
        HumMin3 = 40
        HumMax3 = 80
        TempMin3 = 21
        TempMinF3 = TempMin3*(9/5)+32
        TempMax3 = 29.4
        TempMaxF3 = TempMax3*(9/5)+32
    elif data1[2] in ['Corn']:
        HumMin3 = 40
        HumMax3 = 80
        TempMin3 = 25
        TempMinF3 = TempMin3*(9/5)+32
        TempMax3 = 32.8
        TempMaxF3 = TempMax3*(9/5)+32
    elif data1[2] in ['Squash']:
        HumMin3 = 40
        HumMax3 = 60
        TempMin3 = 21
        TempMinF3 = TempMin3*(9/5)+32
        TempMax3 = 29.4
        TempMaxF3 = TempMax3*(9/5)+32
    elif data1[2] in ['Peas']:
        HumMin3 = 40
        HumMax3 = 60
        TempMin3 = 10
        TempMinF3 = TempMin3*(9/5)+32
        TempMax3 = 21
        TempMaxF3 = TempMax3*(9/5)+32
    elif data1[2] in ['Nothing']:
        HumMin3 = None
        HumMax3 = None
        TempMin3 = None
        TempMax3 = None
    elif data1[2] in ['Other']:
        print("")
        
    if data1[3] in ['Tomatoes']:
        HumMin4 = 40
        HumMax4 = 80
        TempMin4 = 18.3
        TempMinF4 = TempMin4*(9/5)+32
        TempMax4 = 29.4
        TempMaxF4 = TempMax4*(9/5)+32
    elif data1[3] in ['Beans']:
        HumMin4 = 40
        HumMax4 = 80
        TempMin4 = 21
        TempMinF4 = TempMin4*(9/5)+32
        TempMax4 = 29.4
        TempMaxF4 = TempMax4*(9/5)+32
    elif data1[3] in ['Corn']:
        HumMin4 = 40
        HumMax4 = 80
        TempMin4 = 25
        TempMinF4 = TempMin4*(9/5)+32
        TempMax4 = 32.8
        TempMaxF4 = TempMax4*(9/5)+32
    elif data1[3] in ['Squash']:
        HumMin4 = 40
        HumMax4 = 60
        TempMin4 = 21
        TempMinF4 = TempMin4*(9/5)+32
        TempMax4 = 29.4
        TempMaxF4 = TempMax4*(9/5)+32
    elif data1[3] in ['Peas']:
        HumMin4 = 40
        HumMax4 = 60
        TempMin4 = 10
        TempMinF4 = TempMin4*(9/5)+32
        TempMax4 = 21
        TempMaxF4 = TempMax4*(9/5)+32
    elif data1[3] in ['Nothing']:
        HumMin4 = None
        HumMax4 = None
        TempMin4 = None
        TempMax4 = None
    elif data1[3] in ['Other']:
        print("")
        
    if data1[4] in ['Tomatoes']:
        HumMin5 = 40
        HumMax5 = 80
        TempMin5 = 18.3
        TempMinF5 = TempMin5*(9/5)+32
        TempMax5 = 29.4
        TempMaxF5 = TempMax5*(9/5)+32
    elif data1[4] in ['Beans']:
        HumMin5 = 40
        HumMax5 = 80
        TempMin5 = 21
        TempMinF5 = TempMin5*(9/5)+32
        TempMax5 = 29.4
        TempMaxF5 = TempMax5*(9/5)+32
    elif data1[4] in ['Corn']:
        HumMin5 = 40
        HumMax5 = 80
        TempMin5 = 25
        TempMinF5 = TempMin5*(9/5)+32
        TempMax5 = 32.8
        TempMaxF5 = TempMax5*(9/5)+32
    elif data1[4] in ['Squash']:
        HumMin5 = 40
        HumMax5 = 60
        TempMin5 = 21
        TempMinF5 = TempMin5*(9/5)+32
        TempMax5 = 29.4
        TempMaxF5 = TempMax5*(9/5)+32
    elif data1[4] in ['Peas']:
        HumMin5 = 40
        HumMax5 = 60
        TempMin5 = 7
        TempMinF5 = TempMin5*(9/5)+32
        TempMax5 = 21
        TempMaxF5 = TempMax5*(9/5)+32
    elif data1[4] in ['Nothing']:
        HumMin5 = None
        HumMax5 = None
        TempMin5 = None
        TempMaxF5 = None
        TempMax5 = None
        TempMinF5 = None
    elif data1[4] in ['Other']:
        print("")
        
    try:
        print("How long would you like this code to run in minutes?")
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        
        count = 0
        
        while count < user + 1:
            print("--------------------------------------------------------------------------------") 
            print("Iteration ", count, " out of ",user)
            
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))

            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))

            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)   
            i = 0
            
            while i <= 17:
                    
                    if i == 0:
                        if HumMin1 == None:
                            print("You have planted nothing in station 1.")
                        else:
                            print("Station 1 soil moisture levels: ")
                            if data2[0] < 200:
                                print("Soil is saturated. Do not water and ensure proper drainage.")
                                GPIO.output(21, True)
                            if data2[0] > 200 and data2[0] < 400:
                                print("Soil is moist. ")
                                GPIO.output(21, True)
                            if data2[0] > 400 and data2[0] < 700:
                                print("Soil is well watered!")
                            if data2[0] > 700 and data2[0] < 900:
                                print("Soil is dry. Water your plants.")
                                GPIO.output(20, True)
                            if data2[0] > 900:
                                print("Your plants are under stress due to lack of water.")
                                print("Please water your plants immediatedly.")
                                GPIO.output(20, True)
                            print("current humidity, station 1: ",data[0])
                            humid1.append(data[0])
                    if i == 1:
                        if HumMin1 == None:
                            print("")
                        else:
                            print("current temperature(C), station 1: ",data[1])
                            tempC1.append(data[1])
                    if i == 2:
                        if HumMin1 == None:
                            print("")
                        else:
                            print("current temperature(F), station 1: ",data[2])
                            tempF1.append(data[2])
                            fig,axs = plt.subplots(3)
                            fig.suptitle('Station 1 Humidity and Temperature')
                            axs[0].plot(humid1)
                            axs[0].set_ylabel('humidity(%)')
                            axs[1].plot(tempC1)
                            axs[1].set_ylabel('Temp(C)')
                            axs[2].plot(tempF1)
                            axs[2].set_ylabel('Temp(F)')
                            axs[2].set_xlabel('Time Passed (Minutes)')
                            plt.show()
      
                    if i == 3:
                        if HumMin2 == None:
                            print("You have planted nothing at Station 2.")
                        else:
                            print("Station 2 soil moisture levels: ")
                            if data2[1] < 200:
                                print("Soil is saturated. Do not water and ensure proper drainage.")
                                GPIO.output(19, True)
                            elif data2[1] > 200 and data2[1] < 400:
                                print("Soil is moist. ")
                                GPIO.output(19, True)
                            elif data2[1] > 400 and data2[1] < 700:
                                print("Soil is well watered!")
                            elif data2[1] > 700 and data2[1] < 900:
                                print("Soil is dry. Water your plants.")
                                GPIO.output(11, True)
                            elif data2[1] > 900:
                                print("Your plants are under stress due to lack of water.")
                                print("Please water your plants immediatedly.")
                                GPIO.output(11, True)
                            print("current humidity, station 2: ", data[3])
                            humid2.append(data[3])
                    if i == 4:
                        if HumMin2 == None:
                            print("")
                        else:
                            print("current temperature(C), station 2: ", data[4])
                            tempC2.append(data[4])
                    if i == 5:
                        if HumMin2 == None:
                            print("")
                        else:
                            print("current temperature(F), station 2: ", data[5])
                            tempF2.append(data[5])
                            print("")
                            fig,axs = plt.subplots(3)
                            fig.suptitle('Station 2 Humidity and Temperature')
                            axs[0].plot(humid2)
                            axs[0].set_ylabel('humidity(%)')
                            axs[1].plot(tempC2)
                            axs[1].set_ylabel('Temp(C)')
                            axs[2].plot(tempF2)
                            axs[2].set_ylabel('Temp(F)')
                            axs[2].set_xlabel('Time Passed (Minutes)')
                            plt.show()
                    if i == 6:
                        if HumMin3 == None:
                            print("You have planted nothing in station 3.")
                        else:
                            print("Station 3 soil moisture levels: ")
                            if data2[2] < 200:
                                print("Soil is saturated. Do not water and ensure proper drainage.")
                                GPIO.output(9, True)
                            elif data2[2] > 200 and data2[2] < 400:
                                print("Soil is moist. ")
                                GPIO.output(9, True)
                            elif data2[2] > 400 and data2[2] < 700:
                                print("Soil is well watered!")
                            elif data2[2] > 700 and data2[2] < 900:
                                print("Soil is dry. Water your plants.")
                                GPIO.output(10, True)
                            elif data2[2] > 900:
                                print("Your plants are under stress due to lack of water.")
                                print("Please water your plants immediatedly.")
                                GPIO.output(10, True)
                            print("current humidity, station 3: ", data[6])
                            humid3.append(data[6])
                    if i == 7:
                        if HumMin3 == None:
                            print("")
                        else:
                            print("current temperature(C), station 3: ", data[7])
                            tempC3.append(data[7])
                    if i == 8:
                        if HumMin3 == None:
                            print("")
                        else:
                            print("current temperature(F), station 3: ", data[8])
                            tempF3.append(data[8])
                            print("")
                            fig,axs = plt.subplots(3)
                            fig.suptitle('Station 3 Humidity and Temperature')
                            axs[0].plot(humid3)
                            axs[0].set_ylabel('humidity(%)')
                            axs[1].plot(tempC3)
                            axs[1].set_ylabel('Temp(C)')
                            axs[2].plot(tempF3)
                            axs[2].set_ylabel('Temp(F)')
                            axs[2].set_xlabel('Time Passed (Minutes)')
                            plt.show()
                    if i == 9:
                        if HumMin4 == None:
                            print("You have planted nothing in station 4.")
                        else:
                            print("Station 4 soil moisture levels: ")
                            if data2[3] < 200:
                                print("Soil is saturated. Do not water and ensure proper drainage.")
                                GPIO.output(7, True)
                            elif data2[3] > 200 and data2[3] < 400:
                                print("Soil is moist. ")
                                GPIO.output(7, True)
                            elif data2[3] > 400 and data2[3] < 700:
                                print("Soil is well watered!")
                            elif data2[3] > 700 and data2[3] < 900:
                                print("Soil is dry. Water your plants.")
                                GPIO.output(8, True)
                            elif data2[3] > 900:
                                print("Your plants are under stress due to lack of water.")
                                print("Please water your plants immediatedly.")
                                GPIO.output(8, True)
                            print("current humidity, station 4: ", data[9])
                            humid4.append(data[9])
                    if i == 10:
                        if HumMin4 == None:
                            print("")
                        else:
                            print("current temperature(C), station 4: ", data[10])
                            tempC4.append(data[10]) 
                    if i == 11:
                        if HumMin4 == None:
                            print("")
                        else:
                            print("current temperature(F), station 4: ", data[11])
                            tempF4.append(data[11])
                            print("")
                            fig,axs = plt.subplots(3)
                            fig.suptitle('Station 4 Humidity and Temperature')
                            axs[0].plot(humid4)
                            axs[0].set_ylabel('humidity(%)')
                            axs[1].plot(tempC4)
                            axs[1].set_ylabel('Temp(C)')
                            axs[2].plot(tempF4)
                            axs[2].set_ylabel('Temp(F)')
                            axs[2].set_xlabel('Time Passed (Minutes)')
                            plt.show()
                    if i == 12:
                        if HumMin5 == None:
                            print("You have planted nothing in station 5.")
                        else:
                            print("Station 5 soil moisture levels: ")
                            if data2[4] < 200:
                                print("Soil is saturated. Do not water and ensure proper drainage.")
                                GPIO.output(24, True)
                            elif data2[4] > 200 and data2[4] < 400:
                                print("Soil is moist. ")
                                GPIO.output(24, True)
                            elif data2[4] > 400 and data2[4] < 700:
                                print("Soil is well watered!")
                            elif data2[4] > 700 and data2[4] < 900:
                                print("Soil is dry. Water your plants.")
                                GPIO.output(23, True)
                            elif data2[4] > 900:
                                print("Your plants are under stress due to lack of water.")
                                print("Please water your plants immediatedly.")
                                GPIO.output(23, True)
                            print("current humidity, station 5: ", data[12])
                            humid5.append(data[12])
                    if i == 13:
                        if HumMin5 == None:
                            print("")
                        else:
                            print("current temperature(C), station 5: ", data[13])
                            tempC5.append(data[13])
                    if i == 14:
                        if HumMin5 == None:
                            print("")
                        else:
                            print("current temperature(F), station 5: ", data[14])
                            tempF5.append(data[14])
                            print("")
                            fig,axs = plt.subplots(3)
                            fig.suptitle('Station 5 Humidity and Temperature')
                            axs[0].plot(humid5)
                            axs[0].set_ylabel('humidity(%)')
                            axs[1].plot(tempC5)
                            axs[1].set_ylabel('Temp(C)')
                            axs[2].plot(tempF5)
                            axs[2].set_ylabel('Temp(F)')
                            axs[2].set_xlabel('Time Passed (Minutes)')
                            plt.show()
                    if i == 15:
                        print("CAUTION: These are values calculated from all stations, including stations you may not be using.")
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        
                        
                        print("WARNINGS:")
                        try:
                            if data[0] < HumMin1:
                                    print("")
                                    print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                                    print("Try misting your plants or adding a humidifier.")
                                    GPIO.output(16, True)
                                    print("")
                            if data[0] > HumMax1:
                                    print("")
                                    print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                                    print("Try adding a dehumidifier in the area.")
                                    GPIO.output(12, True)
                                    print("")
                                
                            if data[1] < TempMin1:
                                    print("")
                                    print("Temperature at station 1 is too cold.")
                                    print("Recommended temperature for ",data1[0]," is over ",TempMin1," C (",TempMinF1," F) and under ",TempMax1," C (", TempMaxF1,") F")
                                    GPIO.output(16, True)
                                    print("")
                            if data[1] > TempMax1:
                                    print("")
                                    print("Temperature at station 1 is too warm.")
                                    print("Recommended temperature for ",data1[0]," is over ",TempMin1," C (",TempMinF1," F) and under ",TempMax1," C (", TempMaxF1,") F")
                                    GPIO.output(12, True)
                                    print("")
                        except TypeError:
                                print("You have planted nothing at station 1.")
                        try:      
                            if data[3] < HumMin2:
                                    print("")
                                    print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                                    print("Try misting your plants or adding a humidifier.")
                                    GPIO.output(26, True)
                                    print("")
                            if data[3] > HumMax2:
                                    print("")
                                    print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                                    print("Try adding a dehumidifier in the area.")
                                    GPIO.output(13, True)
                                    print("")
                            
                            if data[4] < TempMin2:
                                    print("")
                                    print("Temperature at station 2 is too cold.")
                                    print("Recommended temperature for ",data1[1]," is over ",TempMin2," C (",TempMinF2," F) and under ",TempMax2," C (", TempMaxF2,") F")
                                    GPIO.output(26, True)
                                    print("")
                            if data[4] > TempMax2:
                                    print("")
                                    print("Temperature at station 2 is too warm.")
                                    print("Recommended temperature for ",data1[1]," is over ",TempMin2," C (",TempMinF2," F) and under ",TempMax2," C (", TempMaxF2,") F")
                                    GPIO.output(13, True)
                                    print("")
                        except TypeError:
                                print("You have planted nothing at station 2.")
                                
                        try:       
                            if data[6] < HumMin3:
                                    print("")
                                    print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                                    print("Try misting your plants or adding a humidifier.")
                                    GPIO.output(6, True)
                                    print("")
                            if data[6] > HumMax3:
                                    print("")
                                    print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                                    print("Try adding a dehumidifier in the area.")
                                    GPIO.output(5, True)
                                    print("")
                            
                            if data[7] < TempMin3:
                                    print("")
                                    print("Temperature at station 3 is too cold.")
                                    print("Recommended temperature for ",data1[2]," is over ",TempMin3," C (",TempMinF3," F) and under ",TempMax3," C (", TempMaxF3,") F")
                                    GPIO.output(6, True)
                                    print("")
                            if data[7] > TempMax3:
                                    print("")
                                    print("Temperature at station 3 is too warm.")
                                    print("Recommended temperature for ",data1[2]," is over ",TempMin3," C (",TempMinF3," F) and under ",TempMax3," C (", TempMaxF3,") F")
                                    GPIO.output(5, True)
                                    print("")
                        except TypeError:
                                print("You have planted nothing at station 3.")
                                
                        try:
                            if data[9] < HumMin4:
                                    print("")
                                    print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                                    print("Try misting your plants or adding a humidifier.")
                                    GPIO.output(22, True)
                                    print("")
                            if data[9] > HumMax4:
                                    print("")
                                    print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                                    print("Try adding a dehumidifier in the area.")
                                    GPIO.output(27, True)
                                    print("")
                            
                            if data[10] < TempMin4:
                                    print("")
                                    print("Temperature at station 4 is too cold.")
                                    print("Recommended temperature for ",data1[3]," is over ",TempMin4," C (",TempMinF4," F) and under ",TempMax4," C (", TempMaxF4,") F")
                                    GPIO.output(22, True)
                                    print("")
                            if data[10] > TempMax4:
                                    print("")
                                    print("Temperature at station 4 is too warm.")
                                    print("Recommended temperature for ",data1[3]," is over ",TempMin4," C (",TempMinF4," F) and under ",TempMax4," C (", TempMaxF4,") F")
                                    GPIO.output(27, True)
                                    print("")
                        except TypeError:
                                print("You have planted nothing at station 4.")
                        
                        try:
                            if data[13] < HumMin5:
                                    print("")
                                    print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                                    print("Try misting your plants or adding a humidifier.")
                                    GPIO.output(17, True)
                                    print("")
                            if data[13] > HumMax5:
                                    print("")
                                    print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                                    print("Try adding a dehumidifier in the area.")
                                    GPIO.output(4, True)
                                    print("")
                            
                            if data[14] < TempMin5:
                                    print("")
                                    print("Temperature at station 5 is too cold.")
                                    print("Recommended temperature for ",data1[4]," is over ",TempMin5," C (",TempMinF5," F) and under ",TempMax5," C (", TempMaxF5,") F")
                                    GPIO.output(17, True)
                                    print("")
                            if data[14] > TempMax5:
                                    print("")
                                    print("Temperature at station 5 is too warm.")
                                    print("Recommended temperature for ",data1[4]," is over ",TempMin5," C (",TempMinF5," F) and under ",TempMax5," C (", TempMaxF5,") F")
                                    GPIO.output(4, True)
                                    print("")
                        except TypeError:
                                print("You have planted nothing at station 5.")
                        
                        try:
                            if data[15] < ((HumMax1 + HumMax2 + HumMax3 + HumMax4 + HumMax5)/5):
                                print("")
                                print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                                print("check your stations for low humidity levels.")
                                print("Try misting your plants or adding a humidifier.")
                                print("")
                            if data[15] > ((HumMax1 + HumMax2 + HumMax3 + HumMax4 + HumMax5)/5):
                                print("")
                                print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                                print("check your stations for high humidity levels.")
                                print("Try adding a dehumidifier in the area.")
                                print("")
        
                            if data[16] < ((TempMin1 + TempMin2 + TempMin3 + TempMin4 + TempMin5)/5):
                                print("")
                                print("The average temperature is too cold for most of these plants.")
                                print("Check to see where your growing stations are too cold.")
                                print("")
                            if data[16] > ((TempMax1 + TempMax2 + TempMax3 + TempMax4 + TempMax5)/5):
                                print("")
                                print("Average temperature is too warm for most of these plants.")
                                print("Check to see where your growing stations are too warm.")
                                print("")
                        except TypeError:
                                print("Average values are only calculated if all five stations are used.")
                      
                    i += 1
            print("--------------------------------------------------------------------------------")  
            count += 1
    except ValueError:
        print("invalid input.")
    
    q()

'''
Module: readArduinoPea()

Author: Jacob Gero, 23 April 2020
RPi "extention": 29 April 2020

The Arduinos are both programmed to delay 60000ms (60 Sec)
between each reading. The user can tell the program 
how long to run in minutes, which is implemented by using
a counter to count how many times the program recieves
new data from the Arduinos. If the user types in a non-integer value, the program
catches this error, and tells the user to input a proper value. The DHT-11 Arduino outputs 
18 pieces of data, which are the humidity readings (%) and temperature (both C and F) for each of the
five stations, as well as the average values. The array which fills 
with this data each minute is called data[], and is emptied and refilled
for every minute, or when the arduino sends the information.
COM3 outputs a reading on the soil module for each of the five 
stations, so this array (labeled data2[]) fills with s

Other veggie modules are nearly the same, with the primary
difference being the temperature thresholds for sending a 
light signal.

'''
def readArduinoPea():
    print("How long would you like this code to run in minutes?")
    user = int(input(""))
    try:
        
        humid1 = [] #Initializes empty arrays representing each data set coming in from the Arduinos.
        tempF1 = [] #These are appended every time new data comes in in the appropriate order recieved from the
        tempC1 = [] #Arduino.
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:

            data = [] 
            for y in range(0,18): 
                data.append(float(arduino.readline()))
                
            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))
            
            i = 0
            print("Iteration ", count, " out of ",user)
                        #This resets all LEDs that are possibly used for every iteration of i.
            #This is important, as LEDs will otherwise remain on if turned on before for the 
            #duration of running the program, thus leading to unreliable use.
            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)

            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)

            while i <= 17:
                    
                    if i == 0:
                        
                        print("Station 1 soil moisture levels: ")
                        if data2[0] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(21, True)
                        elif data2[0] > 200 and data2[0] < 400:
                            print("Soil is moist. ")
                            GPIO.output(21, True)
                        elif data2[0] > 400 and data2[0] < 700:
                            print("Soil is well watered!")
                        elif data2[0] > 700 and data2[0] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(20, True)
                        elif data2[0] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(20, True)    
                        print("current humidity, station 1: ",data[0])
                        humid1.append(data[0])
                    if i == 1:
                        print("current temperature(C), station 1: ",data[1])
                        tempC1.append(data[1])
                    if i == 2:
                        print("current temperature(F), station 1: ",data[2])
                        tempF1.append(data[2])
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 1 Humidity and Temperature')
                        axs[0].plot(humid1)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC1,tempF1)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF1)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        print("")
     
                    if i == 3:
                        print("Station 2 soil moisture levels: ")
                        if data2[1] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(19, True)
                        elif data2[1] > 200 and data2[1] < 400:
                            print("Soil is moist. ")
                            GPIO.output(19, True)
                        elif data2[1] > 400 and data2[1] < 700:
                            print("Soil is well watered!")
                        elif data2[1] > 700 and data2[1] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(11, True)
                        elif data2[1] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(11, True)
                        print("current humidity, station 2: ", data[3])
                        humid2.append(data[3])
                    if i == 4:
                        print("current temperature(C), station 2: ", data[4])
                        tempC2.append(data[4])
                    if i == 5:
                        print("current temperature(F), station 2: ", data[5])
                        tempF2.append(data[5])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 2 Humidity and Temperature')
                        axs[0].plot(humid2)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC2)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF2)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        
                    if i == 6:
                        print("Station 3 soil moisture levels: ")
                        if data2[2] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(9, True)
                        elif data2[2] > 200 and data2[2] < 400:
                            print("Soil is moist. ")
                            GPIO.output(9, True)
                        elif data2[2] > 400 and data2[2] < 700:
                            print("Soil is well watered!")
                        elif data2[2] > 700 and data2[2] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(10, True)
                        elif data2[2] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(10, True)
                        print("current humidity, station 3: ", data[6])
                        humid3.append(data[6])
                    if i == 7:
                        print("current temperature(C), station 3: ", data[7])
                        tempC3.append(data[7])
                    if i == 8:
                        print("current temperature(F), station 3: ", data[8])
                        tempF3.append(data[8])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 3 Humidity and Temperature')
                        axs[0].plot(humid3)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC3)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF3)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 9:
                        print("Station 4 soil moisture levels: ")
                        if data2[3] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(7, True)
                        elif data2[3] > 200 and data2[3] < 400:
                            print("Soil is moist. ")
                            GPIO.output(7, True)
                        elif data2[3] > 400 and data2[3] < 700:
                            print("Soil is well watered!")
                        elif data2[3] > 700 and data2[3] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(8, True)
                        elif data2[3] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(8, True)
                        print("current humidity, station 4: ", data[9])
                        humid4.append(data[9])
                    if i == 10:
                        print("current temperature(C), station 4: ", data[10])
                        tempC4.append(data[10]) 
                    if i == 11:
                        print("current temperature(F), station 4: ", data[11])
                        tempF4.append(data[11])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 4 Humidity and Temperature')
                        axs[0].plot(humid4)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC4)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF4)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 12:
                        print("Station 5 soil moisture levels: ")
                        if data2[4] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(24, True)
                        elif data2[4] > 200 and data2[4] < 400:
                            print("Soil is moist. ")
                            GPIO.output(24, True)
                        elif data2[4] > 400 and data2[4] < 700:
                            print("Soil is well watered!")
                        elif data2[4] > 700 and data2[4] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(23, True)
                        elif data2[4] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(23, True)
                        print("current humidity, station 5: ", data[12])
                        humid5.append(data[12])
                    if i == 13:
                        print("current temperature(C), station 5: ", data[13])
                        tempC5.append(data[13])
                    if i == 14:
                        print("current temperature(F), station 5: ", data[14])
                        tempF5.append(data[14])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 5 Humidity and Temperature')
                        axs[0].plot(humid5)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC5)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF5)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 15:
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        print("WARNINGS:")
                        
                        if data[0] < 40:
                            print("")
                            print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(16, True)
                            print("")
                        if data[0] > 60:
                            print("")
                            print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(12,True)
                            print("")
                        
                        if data[1] < 10:
                            print("")
                            print("Temperature at station 1 is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(16, True)
                            print("")
                        if data[1] > 21:
                            print("")
                            print("Temperature at station 1 is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(12,True)
                            print("")
    
                        if data[3] < 40:
                            print("")
                            print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(26,True)
                            print("")
                        if data[3] > 60:
                            print("")
                            print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(13,True)
                            print("")
                    
                        if data[4] < 10:
                            print("")
                            print("Temperature at station 2 is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(26,True)
                            print("")
                        if data[4] > 21:
                            print("")
                            print("Temperature at station 2 is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70C).")
                            GPIO.output(13,True)
                            print("")
                        
                        if data[6] < 40:
                            print("")
                            print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(6,True)
                            print("")
                        if data[6] > 60:
                            print("")
                            print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(5,True)
                            print("")
    
                        if data[7] < 10:
                            print("")
                            print("Temperature at station 3 is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(6,True)
                            print("")
                        if data[7] > 21:
                            print("")
                            print("Temperature at station 3 is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70C).")
                            GPIO.output(5,True)
                            print("")
                     
                        if data[9] < 40:
                            print("")
                            print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(22,True)
                            print("")
                        if data[9] > 60:
                            print("")
                            print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(27,True)
                            print("")
                    
                        if data[10] < 7:
                            print("")
                            print("Temperature at station 4 is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(22,True)
                            print("")
                        if data[10] > 21:
                            print("")
                            print("Temperature at station 4 is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70C).")
                            GPIO.output(27,True)
                            print("")
                    
                    
                        if data[12] < 40:
                            print("")
                            print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(17,True)
                            print("")
                        if data[12] > 60:
                            print("")
                            print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(4,True)
                            print("")
                    
                        if data[13] < 10:
                            print("")
                            print("Temperature at station 5 is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            GPIO.output(17, True)
                            print("")
                        
                            
                        if data[13] > 21:
                            print("")
                            print("Temperature at station 5 is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70C).")
                            GPIO.output(4,True)
                            print("")
        
                    
                        if data[15] < 40:
                            print("")
                            print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                            print("check your stations for low humidity levels.")
                            print("Try misting your plants or adding a humidifier.")
                            print("")
                        if data[15] > 60:
                            print("")
                            print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                            print("check your stations for high humidity levels.")
                            print("Try adding a dehumidifier in the area.")
                            print("")
    
                        if data[16] < 10:
                            print("")
                            print("The average temperature is too cold.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70F).")
                            print("Check to see where your growing stations are too cold.")
                            print("")
                        if data[16] > 21:
                            print("")
                            print("Average temperature is too warm.")
                            print("Recommended temperature for Peas is over 10C (50F) and under 21C (70C).")
                            print("Check to see where your growing stations are too warm.")
                            print("")
  
                        
                    i += 1
            print("--------------------------------------------------------------------------------")
            
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoPea()

def readArduinoBean():
    print("How long would you like this code to run in minutes?")
    
    try:
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))
                
            p = 0
            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))
                p += 1
            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)    
            
            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
            i = 0
            print("Iteration ", count, " out of ",user)
            while i <= 17:
                    
                    if i == 0:
                        print("Station 1 soil moisture levels: ")
                        if data2[0] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(21, True)
                        elif data2[0] > 200 and data2[0] < 400:
                            print("Soil is moist. ")
                            GPIO.output(21, True)
                        elif data2[0] > 400 and data2[0] < 700:
                            print("Soil is well watered!")
                        elif data2[0] > 700 and data2[0] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(20, True)
                        elif data2[0] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(20, True)    
                        print("current humidity, station 1: ",data[0])
                        humid1.append(data[0])
                    if i == 1:
                        print("current temperature(C), station 1: ",data[1])
                        tempC1.append(data[1])
                    if i == 2:
                        print("current temperature(F), station 1: ",data[2])
                        tempF1.append(data[2])
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 1 Humidity and Temperature')
                        axs[0].plot(humid1)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC1)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF1)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        print("")

                    if i == 3:
                        print("Station 2 soil moisture levels: ")
                        if data2[1] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(19, True)
                        elif data2[1] > 200 and data2[1] < 400:
                            print("Soil is moist. ")
                            GPIO.output(19, True)
                        elif data2[1] > 400 and data2[1] < 700:
                            print("Soil is well watered!")
                        elif data2[1] > 700 and data2[1] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(11, True)
                        elif data2[1] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(11, True)
                        print("current humidity, station 2: ", data[3])
                        humid2.append(data[3])
                    if i == 4:
                        print("current temperature(C), station 2: ", data[4])
                        tempC2.append(data[4])
                    if i == 5:
                        print("current temperature(F), station 2: ", data[5])
                        tempF2.append(data[5])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 2 Humidity and Temperature')
                        axs[0].plot(humid2)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC2)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF2)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 6:
                        print("Station 3 soil moisture levels: ")
                        if data2[2] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(9, True)
                        elif data2[2] > 200 and data2[2] < 400:
                            print("Soil is moist. ")
                            GPIO.output(9, True)
                        elif data2[2] > 400 and data2[2] < 700:
                            print("Soil is well watered!")
                        elif data2[2] > 700 and data2[2] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(10, True)
                        elif data2[2] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(10, True)
                        print("current humidity, station 3: ", data[6])
                        humid3.append(data[6])
                    if i == 7:
                        print("current temperature(C), station 3: ", data[7])
                        tempC3.append(data[7])
                    if i == 8:
                        print("current temperature(F), station 3: ", data[8])
                        tempF3.append(data[8])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 3 Humidity and Temperature')
                        axs[0].plot(humid3)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC3)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF3)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 9:
                        print("Station 4 soil moisture levels: ")
                        if data2[3] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(7, True)
                        elif data2[3] > 200 and data2[3] < 400:
                            print("Soil is moist. ")
                            GPIO.output(7, True)
                        elif data2[3] > 400 and data2[3] < 700:
                            print("Soil is well watered!")
                        elif data2[3] > 700 and data2[3] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(8, True)
                        elif data2[3] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(8, True)
                        print("current humidity, station 4: ", data[9])
                        humid4.append(data[9])
                    if i == 10:
                        print("current temperature(C), station 4: ", data[10])
                        tempC4.append(data[10]) 
                    if i == 11:
                        print("current temperature(F), station 4: ", data[11])
                        tempF4.append(data[11])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 4 Humidity and Temperature')
                        axs[0].plot(humid4)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC4)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF4)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 12:
                        print("Station 5 soil moisture levels: ")
                        if data2[4] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(24, True)
                        elif data2[4] > 200 and data2[4] < 400:
                            print("Soil is moist. ")
                            GPIO.output(24, True)
                        elif data2[4] > 400 and data2[4] < 700:
                            print("Soil is well watered!")
                        elif data2[4] > 700 and data2[4] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(23, True)
                        elif data2[4] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(23, True)
                        print("current humidity, station 5: ", data[12])
                        humid5.append(data[12])
                    if i == 13:
                        print("current temperature(C), station 5: ", data[13])
                        tempC5.append(data[13])
                    if i == 14:
                        print("current temperature(F), station 5: ", data[14])
                        tempF5.append(data[14])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 5 Humidity and Temperature')
                        axs[0].plot(humid5)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC5)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF5)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 15:
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        
                        print("WARNINGS:")
                        
                        if data[0] < 40:
                                print("")
                                print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(16, True)
                                print("")
                        if data[0] > 80:
                                print("")
                                print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(26, True)
                                print("")
                            
                        if data[1] < 21:
                                print("")
                                print("Temperature at station 1 is too cold.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(16, True)
                                print("")
                        if data[1] > 29.4:
                                print("")
                                print("Temperature at station 1 is too warm.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(26, True)
                                print("")
    
                        if data[3] < 40:
                                print("")
                                print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(26, True)
                                print("")
                        if data[3] > 80:
                                print("")
                                print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(13, True)
                                print("")
                        
                        if data[4] < 21:
                                print("")
                                print("Temperature at station 2 is too cold.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(26, True)
                                print("")
                        if data[4] > 29.4:
                                print("")
                                print("Temperature at station 2 is too warm.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(13, True)
                                print("")
                            
                        if data[6] < 40:
                                print("")
                                print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(6, True)
                                print("")
                        if data[6] > 80:
                                print("")
                                print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(5, True)
                                print("")
    
                        if data[7] < 21:
                                print("")
                                print("Temperature at station 3 is too cold.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(6, True)
                                print("")
                        if data[7] > 29.4:
                                print("")
                                print("Temperature at station 3 is too warm.")
                                print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                                GPIO.output(5, True)
                                print("")
    
                        if data[9] < 40:
                            print("")
                            print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(22, True)
                            print("")
                        if data[9] > 80:
                            print("")
                            print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(27, True)
                            print("")
                    
                        if data[10] < 21:
                            print("")
                            print("Temperature at station 4 is too cold.")
                            print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                            GPIO.output(22, True)
                            print("")
                        if data[10] > 29.4:
                            print("")
                            print("Temperature at station 4 is too warm.")
                            print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                            GPIO.output(27, True)
                            print("")
                    
                    
                        if data[12] < 40:
                            print("")
                            print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(17, True)
                            print("")
                        if data[12] > 80:
                            print("")
                            print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(4, True)
                            print("")
                    
                        if data[13] < 21:
                            print("")
                            print("Temperature at station 5 is too cold.")
                            print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F)).")
                            GPIO.output(17, True)
                            print("")
                        if data[13] > 29.4:
                            print("")
                            print("Temperature at station 5 is too warm.")
                            print("Recommended temperature for Beans is over 21C (70F) and under 29.4C (85F).")
                            GPIO.output(4, True)
                            print("")
                    
                        if data[15] < 40:
                            print("")
                            print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                            print("check your stations for low humidity levels.")
                            print("Try misting your plants or adding a humidifier.")
                            print("")
                        if data[15] > 80:
                            print("")
                            print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                            print("check your stations for high humidity levels.")
                            print("Try adding a dehumidifier in the area.")
                            print("")
    
                        if data[16] < 21:
                            print("")
                            print("The average temperature is too cold.")
                            print("Recommended temperature for beans is 21C (70F) and under 29.4C (85F).")
                            print("Check to see where your growing stations are too cold.")
                            print("")
                        if data[16] > 29.4:
                            print("")
                            print("Average temperature is too warm.")
                            print("Recommended temperature for beans is 21C (70F) and under 29.4C (85F).")
                            print("Check to see where your growing stations are too warm.")
                            print("")
                    i += 1
            print("--------------------------------------------------------------------------------")  
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoBean()
        
def readArduinoSquash():
    print("How long would you like this code to run in minutes?")
    
    try:
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))

            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))

            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)
            if GPIO.input(21):
                GPIO.output(21, False)
            
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
            
            i = 0
            print("Iteration ", count, " out of ",user)

            while i <= 17:
 
                    if i == 0:
                       print("Station 1 soil moisture levels: ")
                       if data2[0] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(21, True)
                       elif data2[0] > 200 and data2[0] < 400:
                            print("Soil is moist. ")
                            GPIO.output(21, True)
                       elif data2[0] > 400 and data2[0] < 700:
                            print("Soil is well watered!")
                       elif data2[0] > 700 and data2[0] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(20, True)
                       elif data2[0] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(20, True)    
                       print("current humidity, station 1: ",data[0])
                       humid1.append(data[0])
                    if i == 1:
                        print("current temperature(C), station 1: ",data[1])
                        tempC1.append(data[1])
                    if i == 2:
                        print("current temperature(F), station 1: ",data[2])
                        tempF1.append(data[2])
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 1 Humidity and Temperature')
                        axs[0].plot(humid1)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC1)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF1)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        
                    if i == 3:
                        print("Station 2 soil moisture levels: ")
                        if data2[1] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(19, True)
                        elif data2[1] > 200 and data2[1] < 400:
                            print("Soil is moist. ")
                            GPIO.output(19, True)
                        elif data2[1] > 400 and data2[1] < 700:
                            print("Soil is well watered!")
                        elif data2[1] > 700 and data2[1] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(11, True)
                        elif data2[1] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(11, True)
                        print("current humidity, station 2: ", data[3])
                        humid2.append(data[3])
                    if i == 4:
                        print("current temperature(C), station 2: ", data[4])
                        tempC2.append(data[4])
                    if i == 5:
                        print("current temperature(F), station 2: ", data[5])
                        tempF2.append(data[5])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 2 Humidity and Temperature')
                        axs[0].plot(humid2)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC2)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF2)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                    if i == 6:
                        print("Station 3 soil moisture levels: ")
                        if data2[2] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(9, True)
                        elif data2[2] > 200 and data2[2] < 400:
                            print("Soil is moist. ")
                            GPIO.output(9, True)
                        elif data2[2] > 400 and data2[2] < 700:
                            print("Soil is well watered!")
                        elif data2[2] > 700 and data2[2] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(10, True)
                        elif data2[2] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(10, True)
                        print("current humidity, station 3: ", data[6])
                        humid3.append(data[6])
                    if i == 7:
                        print("current temperature(C), station 3: ", data[7])
                        tempC3.append(data[7])
                    if i == 8:
                        print("current temperature(F), station 3: ", data[8])
                        tempF3.append(data[8])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 3 Humidity and Temperature')
                        axs[0].plot(humid3)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC3)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF3)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 9:
                        print("Station 4 soil moisture levels: ")
                        if data2[3] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(7, True)
                        elif data2[3] > 200 and data2[3] < 400:
                            print("Soil is moist. ")
                            GPIO.output(7, True)
                        elif data2[3] > 400 and data2[3] < 700:
                            print("Soil is well watered!")
                        elif data2[3] > 700 and data2[3] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(8, True)
                        elif data2[3] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(8, True)
                        print("current humidity, station 4: ", data[9])
                        humid4.append(data[9])
                    if i == 10:
                        print("current temperature(C), station 4: ", data[10])
                        tempC4.append(data[10]) 
                    if i == 11:
                        print("current temperature(F), station 4: ", data[11])
                        tempF4.append(data[11])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 4 Humidity and Temperature')
                        axs[0].plot(humid4)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC4)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF4)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 12:
                        print("Station 5 soil moisture levels: ")
                        if data2[4] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(24, True)
                        elif data2[4] > 200 and data2[4] < 400:
                            print("Soil is moist. ")
                            GPIO.output(24, True)
                        elif data2[4] > 400 and data2[4] < 700:
                            print("Soil is well watered!")
                        elif data2[4] > 700 and data2[4] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(23, True)
                        elif data2[4] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(23, True)
                        print("current humidity, station 5: ", data[12])
                        humid5.append(data[12])
                    if i == 13:
                        print("current temperature(C), station 5: ", data[13])
                        tempC5.append(data[13])
                    if i == 14:
                        print("current temperature(F), station 5: ", data[14])
                        tempF5.append(data[14])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 5 Humidity and Temperature')
                        axs[0].plot(humid5)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC5)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF5)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 15:
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                        print("WARNINGS:")
                        
                        if data[0] < 40:
                                print("")
                                print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(16, True)
                                print("")
                        if data[0] > 60:
                                print("")
                                print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(12, True)
                                print("")
                            
                        if data[1] < 15.6:
                                print("")
                                print("Temperature at station 1 is too cold.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(16, True)
                                print("")
                        if data[1] > 24:
                                print("")
                                print("Temperature at station 1 is too warm.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(12, True)
                                print("")
    
                        if data[3] < 40:
                                print("")
                                print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(26, True)
                                print("")
                        if data[3] > 60:
                                print("")
                                print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(13, True)
                                print("")
                        
                        if data[4] < 15.6:
                                print("")
                                print("Temperature at station 2 is too cold.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(26, True)
                                print("")
                        if data[4] > 24:
                                print("")
                                print("Temperature at station 2 is too warm.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(13, True)
                                print("")
                            
                        if data[6] < 40:
                                print("")
                                print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(26, True)
                                print("")
                        if data[6] > 60:
                                print("")
                                print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(13, True)
                                print("")
    
                        if data[7] < 15.6:
                                print("")
                                print("Temperature at station 3 is too cold.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(6, True)
                                print("")
                        if data[7] > 24:
                                print("")
                                print("Temperature at station 3 is too warm.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(5, True)
                                print("")
    
                        if data[9] < 40:
                            print("")
                            print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(6, True)
                            print("")
                        if data[9] > 60:
                            print("")
                            print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(5, True)
                            print("")
                    
                        if data[10] < 15.6:
                                print("")
                                print("Temperature at station 4 is too cold.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(6, True)
                                print("")
                        if data[10] > 24:
                                print("")
                                print("Temperature at station 4 is too warm.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(5, True)
                                print("")
                    
                    
                        if data[12] < 40:
                            print("")
                            print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(22, True)
                            print("")
                        if data[12] > 60:
                            print("")
                            print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(27, True)
                            print("")
                    
                        if data[13] < 15.6:
                                print("")
                                print("Temperature at station 5 is too cold.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(22, True)
                                print("")
                        if data[13] > 24:
                                print("")
                                print("Temperature at station 5 is too warm.")
                                print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                                GPIO.output(27, True)
                                print("")
                    
                        if data[15] < 40:
                            print("")
                            print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                            print("check your stations for low humidity levels.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(17, True)
                            print("")
                        if data[15] > 60:
                            print("")
                            print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                            print("check your stations for high humidity levels.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(4, True)
                            print("")
    
                        if data[16] < 15.6:
                            print("")
                            print("The average temperature is too cold.")
                            print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                            print("Check to see where your growing stations are too cold.")
                            GPIO.output(17, True)
                            print("")
                        if data[16] > 24:
                            print("")
                            print("Average temperature is too warm.")
                            print("Recommended temperature for squash is over 15.6C (60F) and under 24C (75F).")
                            print("Check to see where your growing stations are too warm.")
                            GPIO.output(4, True)
                            print("")
                    i += 1
            print("--------------------------------------------------------------------------------")  
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoSquash()
        
def readArduinoTomato():
    print("How long would you like this code to run in minutes?")
    
    try:
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))
                
            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))
            
            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)
            
            i = 0
            print("Iteration ", count, " out of ",user)
            while i <= 17:
                    
                    if i == 0:
                        print("Station 1 soil moisture levels: ")
                        if data2[0] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(21, True)
                        elif data2[0] > 200 and data2[0] < 400:
                            print("Soil is moist. ")
                            GPIO.output(21, True)
                        elif data2[0] > 400 and data2[0] < 700:
                            print("Soil is well watered!")
                        elif data2[0] > 700 and data2[0] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(20, True)
                        elif data2[0] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(20, True)    
                        print("current humidity, station 1: ",data[0])
                        humid1.append(data[0])
                    if i == 1:
                        print("current temperature(C), station 1: ",data[1])
                        tempC1.append(data[1])
                    if i == 2:
                        print("current temperature(F), station 1: ",data[2])
                        tempF1.append(data[2])
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 1 Humidity and Temperature')
                        axs[0].plot(humid1)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC1)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF1)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()

                        
                    if i == 3:
                        print("Station 2 soil moisture levels: ")
                        if data2[1] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(19, True)
                        elif data2[1] > 200 and data2[1] < 400:
                            print("Soil is moist. ")
                            GPIO.output(19, True)
                        elif data2[1] > 400 and data2[1] < 700:
                            print("Soil is well watered!")
                        elif data2[1] > 700 and data2[1] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(11, True)
                        elif data2[1] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(11, True)
                        print("current humidity, station 2: ", data[3])
                        humid2.append(data[3])
                    if i == 4:
                        print("current temperature(C), station 2: ", data[4])
                        tempC2.append(data[4])
                    if i == 5:
                        print("current temperature(F), station 2: ", data[5])
                        tempF2.append(data[5])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 2 Humidity and Temperature')
                        axs[0].plot(humid2)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC2)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF2)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 6:
                        print("Station 3 soil moisture levels: ")
                        if data2[2] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(9, True)
                        elif data2[2] > 200 and data2[2] < 400:
                            print("Soil is moist. ")
                            GPIO.output(9, True)
                        elif data2[2] > 400 and data2[2] < 700:
                            print("Soil is well watered!")
                        elif data2[2] > 700 and data2[2] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(10, True)
                        elif data2[2] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(10, True)
                        print("current humidity, station 3: ", data[6])
                        humid3.append(data[6])
                    if i == 7:
                        print("current temperature(C), station 3: ", data[7])
                        tempC3.append(data[7])
                    if i == 8:
                        print("current temperature(F), station 3: ", data[8])
                        tempF3.append(data[8])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 3 Humidity and Temperature')
                        axs[0].plot(humid3)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC3)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF3)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 9:
                        print("Station 4 soil moisture levels: ")
                        if data2[3] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(7, True)
                        elif data2[3] > 200 and data2[3] < 400:
                            print("Soil is moist. ")
                            GPIO.output(7, True)
                        elif data2[3] > 400 and data2[3] < 700:
                            print("Soil is well watered!")
                        elif data2[3] > 700 and data2[3] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(8, True)
                        elif data2[3] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(8, True)
                        print("current humidity, station 4: ", data[9])
                        humid4.append(data[9])
                    if i == 10:
                        print("current temperature(C), station 4: ", data[10])
                        tempC4.append(data[10]) 
                    if i == 11:
                        print("current temperature(F), station 4: ", data[11])
                        tempF4.append(data[11])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 4 Humidity and Temperature')
                        axs[0].plot(humid4)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC4)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF4)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 12:
                        print("Station 5 soil moisture levels: ")
                        if data2[4] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(24, True)
                        elif data2[4] > 200 and data2[4] < 400:
                            print("Soil is moist. ")
                            GPIO.output(24, True)
                        elif data2[4] > 400 and data2[4] < 700:
                            print("Soil is well watered!")
                        elif data2[4] > 700 and data2[4] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(23, True)
                        elif data2[4] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(23, True)
                        print("current humidity, station 5: ", data[12])
                        humid5.append(data[12])
                    if i == 13:
                        print("current temperature(C), station 5: ", data[13])
                        tempC5.append(data[13])
                    if i == 14:
                        print("current temperature(F), station 5: ", data[14])
                        tempF5.append(data[14])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 5 Humidity and Temperature')
                        axs[0].plot(humid5)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC5)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF5)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 15:
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                    
                        print("WARNINGS:")
                        
                        if data[0] < 40:
                                print("")
                                print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(16,True)
                                print("")
                        if data[0] > 80:
                                print("")
                                print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(12,True)
                                print("")
                            
                        if data[1] < 18.3:
                                print("")
                                print("Temperature at station 1 is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(16,True)
                                print("")
                        if data[1] > 29.4:
                                print("")
                                print("Temperature at station 1 is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(12,True)
                                print("")
    
                        if data[3] < 40:
                                print("")
                                print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(26,True)
                                print("")
                        if data[3] > 80:
                                print("")
                                print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(13,True)
                                print("")
                        
                        if data[4] < 18.3:
                                print("")
                                print("Temperature at station 2 is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(26,True)
                                print("")
                        if data[4] > 29.4:
                                print("")
                                print("Temperature at station 2 is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(13,True)
                                print("")
                            
                        if data[6] < 40:
                                print("")
                                print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(6,True)
                                print("")
                        if data[6] > 80:
                                print("")
                                print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(5,True)
                                print("")
    
                        if data[7] < 18.3:
                                print("")
                                print("Temperature at station 3 is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(6,True)
                                print("")
                        if data[7] > 29.4:
                                print("")
                                print("Temperature at station 3 is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(5,True)
                                print("")
    
                        if data[9] < 40:
                                print("")
                                print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(22,True)
                                print("")
                        if data[9] > 80:
                                print("")
                                print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(27,True)
                                print("")
                    
                        if data[10] < 18.3:
                                print("")
                                print("Temperature at station 4 is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(22,True)
                                print("")
                        if data[10] > 29.4:
                                print("")
                                print("Temperature at station 4 is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(27,True)
                                print("")

                        if data[12] < 40:
                                print("")
                                print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(17,True)
                                print("")
                        if data[12] > 80:
                                print("")
                                print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(4,True)
                                print("")
                    
                        if data[13] < 18.3:
                                print("")
                                print("Temperature at station 5 is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(17,True)
                                print("")
                        if data[13] > 29.4:
                                print("")
                                print("Temperature at station 5 is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                GPIO.output(4,True)
                                print("")
                    
                        if data[15] < 40:
                                print("")
                                print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                                print("check your stations for low humidity levels.")
                                print("Try misting your plants or adding a humidifier.")
                                print("")
                        if data[15] > 80:
                                print("")
                                print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                                print("check your stations for high humidity levels.")
                                print("Try adding a dehumidifier in the area.")
                                print("")
    
                        if data[16] < 18.3:
                                print("")
                                print("The average temperature is too cold.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                print("Check to see where your growing stations are too cold.")
                                print("")
                        if data[16] > 29.4:
                                print("")
                                print("Average temperature is too warm.")
                                print("Recommended temperature for tomatoes is over 18.3C (65F) and under 29.4C (85F).")
                                print("Check to see where your growing stations are too warm.")
                                print("")
                    i += 1
            print("--------------------------------------------------------------------------------")  
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoTomato()
        
def readArduinoCorn():
    print("How long would you like this code to run in minutes?")
    
    try:
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))
                
            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))

            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)
            
            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
            i = 0
            print("Iteration ", count, " out of ",user)
            while i <= 17:
                    
                    if i == 0:
                        print("Station 1 soil moisture levels: ")
                        if data2[0] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(21, True)
                        elif data2[0] > 200 and data2[0] < 400:
                            print("Soil is moist. ")
                            GPIO.output(21, True)
                        elif data2[0] > 400 and data2[0] < 700:
                            print("Soil is well watered!")
                        elif data2[0] > 700 and data2[0] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(20, True)
                        elif data2[0] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(20, True)    
                        print("current humidity, station 1: ",data[0])
                        humid1.append(data[0])
                        
                    if i == 1:
                        print("current temperature(C), station 1: ",data[1])
                        tempC1.append(data[1])
                    if i == 2:
                        print("current temperature(F), station 1: ",data[2])
                        tempF1.append(data[2])
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 1 Humidity and Temperature')
                        axs[0].plot(humid1)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC1)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF1)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()

                        
                    if i == 3:
                        print("Station 2 soil moisture levels: ")
                        if data2[1] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(19, True)
                        elif data2[1] > 200 and data2[1] < 400:
                            print("Soil is moist. ")
                            GPIO.output(19, True)
                        elif data2[1] > 400 and data2[1] < 700:
                            print("Soil is well watered!")
                        elif data2[1] > 700 and data2[1] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(11, True)
                        elif data2[1] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(11, True)
                        print("current humidity, station 2: ", data[3])
                        humid2.append(data[3])
                    if i == 4:
                        print("current temperature(C), station 2: ", data[4])
                        tempC2.append(data[4])
                    if i == 5:
                        print("current temperature(F), station 2: ", data[5])
                        tempF2.append(data[5])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 2 Humidity and Temperature')
                        axs[0].plot(humid2)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC2)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF2)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 6:
                        print("Station 3 soil moisture levels: ")
                        if data2[2] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(9, True)
                        elif data2[2] > 200 and data2[2] < 400:
                            print("Soil is moist. ")
                            GPIO.output(9, True)
                        elif data2[2] > 400 and data2[2] < 700:
                            print("Soil is well watered!")
                        elif data2[2] > 700 and data2[2] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(10, True)
                        elif data2[2] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(10, True)
                        print("current humidity, station 3: ", data[6])
                        humid3.append(data[6])
                    if i == 7:
                        print("current temperature(C), station 3: ", data[7])
                        tempC3.append(data[7])
                    if i == 8:
                        print("current temperature(F), station 3: ", data[8])
                        tempF3.append(data[8])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 3 Humidity and Temperature')
                        axs[0].plot(humid3)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC3)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF3)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                    if i == 9:
                        print("Station 4 soil moisture levels: ")
                        if data2[3] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(7, True)
                        elif data2[3] > 200 and data2[3] < 400:
                            print("Soil is moist. ")
                            GPIO.output(7, True)
                        elif data2[3] > 400 and data2[3] < 700:
                            print("Soil is well watered!")
                        elif data2[3] > 700 and data2[3] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(8, True)
                        elif data2[3] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(8, True)
                        print("current humidity, station 4: ", data[9])
                        humid4.append(data[9])
                    if i == 10:
                        print("current temperature(C), station 4: ", data[10])
                        tempC4.append(data[10]) 
                    if i == 11:
                        print("current temperature(F), station 4: ", data[11])
                        tempF4.append(data[11])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 4 Humidity and Temperature')
                        axs[0].plot(humid4)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC4)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF4)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 12:
                        print("Station 5 soil moisture levels: ")
                        if data2[4] < 200:
                            print("Soil is saturated. Do not water and ensure proper drainage.")
                            GPIO.output(24, True)
                        elif data2[4] > 200 and data2[4] < 400:
                            print("Soil is moist. ")
                            GPIO.output(24, True)
                        elif data2[4] > 400 and data2[4] < 700:
                            print("Soil is well watered!")
                        elif data2[4] > 700 and data2[4] < 900:
                            print("Soil is dry. Water your plants.")
                            GPIO.output(23, True)
                        elif data2[4] > 900:
                            print("Your plants are under stress due to lack of water.")
                            print("Please water your plants immediatedly.")
                            GPIO.output(23, True)
                        print("current humidity, station 5: ", data[12])
                        humid5.append(data[12])
                    if i == 13:
                        print("current temperature(C), station 5: ", data[13])
                        tempC5.append(data[13])
                    if i == 14:
                        print("current temperature(F), station 5: ", data[14])
                        tempF5.append(data[14])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Station 5 Humidity and Temperature')
                        axs[0].plot(humid5)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempC5)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempF5)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    if i == 15:
                        print("current humidity, average: ", data[15])
                        humidav.append(data[15])
                    if i == 16:
                        print("current temperature(C), average: ", data[16])
                        tempCav.append(data[16])
                    if i == 17:
                        print("current temperature(F), average: ", data[17])
                        tempFav.append(data[17])
                        print("")
                        fig,axs = plt.subplots(3)
                        fig.suptitle('Average Humidity and Temperature')
                        axs[0].plot(humidav)
                        axs[0].set_ylabel('humidity(%)')
                        axs[1].plot(tempCav)
                        axs[1].set_ylabel('Temp(C)')
                        axs[2].plot(tempFav)
                        axs[2].set_ylabel('Temp(F)')
                        axs[2].set_xlabel('Time Passed (Minutes)')
                        plt.show()
                    
                        print("WARNINGS:")
                        
                        if data[0] < 40:
                                print("")
                                print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(16, True)
                                print("")
                        if data[0] > 80:
                                print("")
                                print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(12, True)
                                print("")
                            
                        if data[1] < 25:
                                print("")
                                print("Temperature at station 1 is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F).")
                                GPIO.output(16, True)
                                print("")
                        if data[1] > 32.8:
                                print("")
                                print("Temperature at station 1 is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F).")
                                GPIO.output(12, True)
                                print("")
    
                        if data[3] < 40:
                                print("")
                                print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(26, True)
                                print("")
                        if data[3] > 80:
                                print("")
                                print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(13, True)
                                print("")
                        
                        if data[4] < 25:
                                print("")
                                print("Temperature at station 2 is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(26, True)
                                print("")
                        if data[4] > 32.8:
                                print("")
                                print("Temperature at station 2 is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(13, True)
                                print("")
                            
                        if data[6] < 40:
                                print("")
                                print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(6, True)
                                print("")
                        if data[6] > 80:
                                print("")
                                print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(5, True)
                                print("")
    
                        if data[7] < 25:
                                print("")
                                print("Temperature at station 3 is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(6, True)
                                print("")
                        if data[7] > 32.8:
                                print("")
                                print("Temperature at station 3 is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(5, True)
                                print("")
    
                        if data[9] < 40:
                                print("")
                                print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(22, True)
                                print("")
                        if data[9] > 80:
                                print("")
                                print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(27, True)
                                print("")
                    
                        if data[10] < 25:
                                print("")
                                print("Temperature at station 4 is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(22, True)
                                print("")
                        if data[10] > 32.8:
                                print("")
                                print("Temperature at station 4 is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(27, True)
                                print("")
                    
                    
                        if data[12] < 40:
                                print("")
                                print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                                print("Try misting your plants or adding a humidifier.")
                                GPIO.output(17, True)
                                print("")
                        if data[12] > 80:
                                print("")
                                print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                                print("Try adding a dehumidifier in the area.")
                                GPIO.output(4, True)
                                print("")
                    
                        if data[13] < 25:
                                print("")
                                print("Temperature at station 5 is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                GPIO.output(17, True)
                                print("")
                        if data[13] > 32.8:
                                print("")
                                print("Temperature at station 5 is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F).")
                                GPIO.output(4, True)
                                print("")
                    
                        if data[15] < 40:
                                print("")
                                print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                                print("check your stations for low humidity levels.")
                                print("Try misting your plants or adding a humidifier.")
                                print("")
                        if data[15] > 80:
                                print("")
                                print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                                print("check your stations for high humidity levels.")
                                print("Try adding a dehumidifier in the area.")
                                print("")
    
                        if data[16] < 25:
                                print("")
                                print("The average temperature is too cold.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                print("Check to see where your growing stations are too cold.")
                                print("")
                        if data[16] > 32.8:
                                print("")
                                print("Average temperature is too warm.")
                                print("Recommended temperature for corn is over 25C (77F) and under 32.8C (91F)")
                                print("Check to see where your growing stations are too warm.")
                                print("")
                    i += 1
            print("--------------------------------------------------------------------------------")  
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoCorn
        
def readArduinoOther():
    
    try:
        print("What are you planting here?")
        plant = input("")
        print("What is the minimum accepted temperature in celsius?")
        ThMin = float(input(""))
        ThMinF = ThMin*(9/5)+32
        print("What is the maximum accepted temperature in celsius?")
        ThMax = float(input(""))
        ThMaxF = ThMax*(9/5)+32
        print("What is the minimum accepted humidity? Recommended for most plants is 40%.")
        HumMin = float(input(""))
        print("What is the maximum accepted humidity? Recommended for most plants is 60%.")
        HumMax = float(input(""))
        print("How long would you like this code to run in minutes?")
        user = int(input(""))
        
        humid1 = []
        tempF1 = []
        tempC1 = []
        humid2 = []
        tempF2 = []
        tempC2 = []
        humid3 = []
        tempF3 = []
        tempC3 = []
        humid4 = []
        tempF4 = []
        tempC4 = []
        humid5 = []
        tempF5 = []
        tempC5 = []
        humidav = []
        tempFav = []
        tempCav = []
        
        count = 0
        while count < user + 1:
            data = []
            for y in range(0,18): 
                data.append(float(arduino.readline()))

            data2 = []
            for y2 in range(0,5): 
                data2.append(float(arduino2.readline()))
            
            if GPIO.input(21):
                GPIO.output(21, False)
            if GPIO.input(20):
                GPIO.output(20, False)
            if GPIO.input(19):
                GPIO.output(19, False)
            if GPIO.input(11):
                GPIO.output(11, False)
            if GPIO.input(9):
                GPIO.output(9, False)
            if GPIO.input(10):
                GPIO.output(10, False)
            if GPIO.input(7):
                GPIO.output(7, False)
            if GPIO.input(8):
                GPIO.output(8, False)
            if GPIO.input(24):
                GPIO.output(24, False)
            if GPIO.input(23):
                GPIO.output(23, False)
                
            if GPIO.input(12):
                GPIO.output(12, False)
            if GPIO.input(16):
                GPIO.output(16, False)
            if GPIO.input(26):
                GPIO.output(26, False)
            if GPIO.input(13):
                GPIO.output(13, False)
            if GPIO.input(6):
                GPIO.output(6, False)
            if GPIO.input(5):
                GPIO.output(5, False)
            if GPIO.input(22):
                GPIO.output(22, False)
            if GPIO.input(27):
                GPIO.output(27, False)
            if GPIO.input(17):
                GPIO.output(17, False)
            if GPIO.input(4):
                GPIO.output(4, False)
            i = 0
            print("Iteration ", count, " out of ",user)
            while i <= 17:
                
                if i == 0:
                    print("Station 1 soil moisture levels: ")
                    if data2[0] < 200:
                        print("Soil is saturated. Do not water and ensure proper drainage.")
                    if data2[0] > 200 and data2[0] < 400:
                        print("Soil is moist. ")
                    if data2[0] > 400 and data2[0] < 700:
                        print("Soil is well watered!")
                    if data2[0] > 700 and data2[0] < 900:
                        print("Soil is dry. Water your plants.")
                    if data2[0] > 900:
                        print("Your plants are under stress due to lack of water.")
                        print("Please water your plants immediatedly.")
                    print("current humidity, station 1: ",data[0])
                    humid1.append(data[0])
                if i == 1:
                    print("current temperature(C), station 1: ",data[1])
                    tempC1.append(data[1])
                if i == 2:
                    print("current temperature(F), station 1: ",data[2])
                    tempF1.append(data[2])
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Station 1 Humidity and Temperature')
                    axs[0].plot(humid1)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempC1)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempF1)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                    
                if i == 3:
                    print("Station 2 soil moisture levels: ")
                    if data2[1] < 200:
                        print("Soil is saturated. Do not water and ensure proper drainage.")
                        GPIO.output(19, True)
                    elif data2[1] > 200 and data2[1] < 400:
                        print("Soil is moist. ")
                        GPIO.output(19, True)
                    elif data2[1] > 400 and data2[1] < 700:
                        print("Soil is well watered!")
                    elif data2[1] > 700 and data2[1] < 900:
                        print("Soil is dry. Water your plants.")
                        GPIO.output(11, True)
                    elif data2[1] > 900:
                        print("Your plants are under stress due to lack of water.")
                        print("Please water your plants immediatedly.")
                        GPIO.output(11, True)
                    print("current humidity, station 2: ", data[3])
                    humid2.append(data[3])
                if i == 4:
                    print("current temperature(C), station 2: ", data[4])
                    tempC2.append(data[4])
                if i == 5:
                    print("current temperature(F), station 2: ", data[5])
                    tempF2.append(data[5])
                    print("")
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Station 2 Humidity and Temperature')
                    axs[0].plot(humid2)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempC2)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempF2)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                    
                if i == 6:
                    print("Station 3 soil moisture levels: ")
                    if data2[2] < 200:
                        print("Soil is saturated. Do not water and ensure proper drainage.")
                        GPIO.output(9, True)
                    elif data2[2] > 200 and data2[2] < 400:
                        print("Soil is moist. ")
                        GPIO.output(9, True)
                    elif data2[2] > 400 and data2[2] < 700:
                        print("Soil is well watered!")
                    elif data2[2] > 700 and data2[2] < 900:
                        print("Soil is dry. Water your plants.")
                        GPIO.output(10, True)
                    elif data2[2] > 900:
                        print("Your plants are under stress due to lack of water.")
                        print("Please water your plants immediatedly.")
                        GPIO.output(10, True)
                    print("current humidity, station 3: ", data[6])
                    humid3.append(data[6])
                if i == 7:
                    print("current temperature(C), station 3: ", data[7])
                    tempC3.append(data[7])
                if i == 8:
                    print("current temperature(F), station 3: ", data[8])
                    tempF3.append(data[8])
                    print("")
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Station 3 Humidity and Temperature')
                    axs[0].plot(humid3)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempC3)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempF3)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                    
                if i == 9:
                    print("Station 4 soil moisture levels: ")
                    if data2[3] < 200:
                        print("Soil is saturated. Do not water and ensure proper drainage.")
                        GPIO.output(7, True)
                    elif data2[3] > 200 and data2[3] < 400:
                        print("Soil is moist. ")
                        GPIO.output(7, True)
                    elif data2[3] > 400 and data2[3] < 700:
                        print("Soil is well watered!")
                    elif data2[3] > 700 and data2[3] < 900:
                        print("Soil is dry. Water your plants.")
                        GPIO.output(8, True)
                    elif data2[3] > 900:
                        print("Your plants are under stress due to lack of water.")
                        print("Please water your plants immediatedly.")
                        GPIO.output(8, True)
                    print("current humidity, station 4: ", data[9])
                    humid4.append(data[9])
                if i == 10:
                    print("current temperature(C), station 4: ", data[10])
                    tempC4.append(data[10]) 
                if i == 11:
                    print("current temperature(F), station 4: ", data[11])
                    tempF4.append(data[11])
                    print("")
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Station 4 Humidity and Temperature')
                    axs[0].plot(humid4)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempC4)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempF4)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                if i == 12:
                    if data2[4] < 200:
                        print("Soil is saturated. Do not water and ensure proper drainage.")
                        GPIO.output(24, True)
                    elif data2[4] > 200 and data2[0] < 400:
                        print("Soil is moist. ")
                        GPIO.output(24, True)
                    elif data2[4] > 400 and data2[0] < 700:
                        print("Soil is well watered!")
                    elif data2[4] > 700 and data2[0] < 900:
                        print("Soil is dry. Water your plants.")
                        GPIO.output(23, True)
                    elif data2[4] > 900:
                        print("Your plants are under stress due to lack of water.")
                        print("Please water your plants immediatedly.")
                        GPIO.output(23, True)
                    print("current humidity, station 5: ", data[12])
                    humid5.append(data[12])
                if i == 13:
                    print("current temperature(C), station 5: ", data[13])
                    tempC5.append(data[13])
                if i == 14:
                    print("current temperature(F), station 5: ", data[14])
                    tempF5.append(data[14])
                    print("")
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Station 5 Humidity and Temperature')
                    axs[0].plot(humid5)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempC5)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempF5)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                if i == 15:
                    print("current humidity, average: ", data[15])
                    humidav.append(data[15])
                if i == 16:
                    print("current temperature(C), average: ", data[16])
                    tempCav.append(data[16])
                if i == 17:
                    print("current temperature(F), average: ", data[17])
                    tempFav.append(data[17])
                    print("")
                    fig,axs = plt.subplots(3)
                    fig.suptitle('Average Humidity and Temperature')
                    axs[0].plot(humidav)
                    axs[0].set_ylabel('humidity(%)')
                    axs[1].plot(tempCav)
                    axs[1].set_ylabel('Temp(C)')
                    axs[2].plot(tempFav)
                    axs[2].set_ylabel('Temp(F)')
                    axs[2].set_xlabel('Time Passed (Minutes)')
                    plt.show()
                    
                    print("WARNINGS:")
                    
                    if data[0] < HumMin:
                            print("")
                            print("Low Humidity levels detected at station 1. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(16, True)
                            print("")
                    if data[0] > HumMax:
                            print("")
                            print("High humidity levels detected at station 1. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(12, True)
                            print("")
                        
                    if data[1] < ThMin:
                            print("")
                            print("Temperature at station 1 is too cold.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(16, True)
                            print("")
                    if data[1] > ThMax:
                            print("")
                            print("Temperature at station 1 is too warm.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(12, True)
                            print("")

                    if data[3] < HumMin:
                            print("")
                            print("Low Humidity levels detected at station 2. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(26, True)
                            print("")
                    if data[3] > HumMax:
                            print("")
                            print("High humidity levels detected at station 2. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(13, True)
                            print("")
                    
                    if data[4] < ThMin:
                            print("")
                            print("Temperature at station 2 is too cold.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(26, True)
                            print("")
                    if data[4] > ThMax:
                            print("")
                            print("Temperature at station 2 is too warm.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(13, True)
                            print("")
                        
                    if data[6] < HumMin:
                            print("")
                            print("Low Humidity levels detected at station 3. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(6, True)
                            print("")
                    if data[6] > HumMax:
                            print("")
                            print("High humidity levels detected at station 3. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(5, True)
                            print("")
                    
                    if data[7] < ThMin:
                            print("")
                            print("Temperature at station 3 is too cold.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(6, True)
                            print("")
                    if data[7] > ThMax:
                            print("")
                            print("Temperature at station 3 is too warm.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(5, True)
                            print("")

                    if data[9] < HumMin:
                            print("")
                            print("Low Humidity levels detected at station 4. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(22, True)
                            print("")
                    if data[9] > HumMax:
                            print("")
                            print("High humidity levels detected at station 4. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(27, True)
                            print("")
                    
                    if data[10] < ThMin:
                            print("")
                            print("Temperature at station 4 is too cold.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(22, True)
                            print("")
                    if data[10] > ThMax:
                            print("")
                            print("Temperature at station 4 is too warm.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(27, True)
                            print("")
                
                
                    if data[12] < HumMin:
                            print("")
                            print("Low Humidity levels detected at station 5. This can cause yellowing and drying of leaves or wilting.")
                            print("Try misting your plants or adding a humidifier.")
                            GPIO.output(17, True)
                            print("")
                    if data[12] > HumMax:
                            print("")
                            print("High humidity levels detected at station 5. This can cause mold or rot to grow on your plants.")
                            print("Try adding a dehumidifier in the area.")
                            GPIO.output(4, True)
                            print("")
                    
                    if data[13] < ThMin:
                            print("")
                            print("Temperature at station 5 is too cold.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(17, True)
                            print("")
                    if data[13] > ThMax:
                            print("")
                            print("Temperature at station 5 is too warm.")
                            print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                            GPIO.output(4, True)
                            print("")
                
                    if data[15] < HumMin:
                        print("")
                        print("Low Humidity levels detected. This can cause yellowing and drying of leaves or wilting.")
                        print("check your stations for low humidity levels.")
                        print("Try misting your plants or adding a humidifier.")
                        print("")
                    if data[15] > HumMax:
                        print("")
                        print("High humidity levels detected. This can cause mold or rot to grow on your plants.")
                        print("check your stations for high humidity levels.")
                        print("Try adding a dehumidifier in the area.")
                        print("")

                    if data[16] < ThMin:
                        print("")
                        print("The average temperature is too cold.")
                        print("Recommended temperature for for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                        print("Check to see where your growing stations are too cold.")
                        print("")
                    if data[16] > ThMax:
                        print("")
                        print("Average temperature is too warm.")
                        print("Recommended temperature for ",plant," is over ",ThMin," C (",ThMinF," F) and under ",ThMax," C (", ThMaxF,") F")
                        print("Check to see where your growing stations are too warm.")
                        print("")
                        
                i += 1
            print("--------------------------------------------------------------------------------")        
            count += 1
    except ValueError:
        print("invalid input.")
        readArduinoOther()
'''
Method: singlePlanner().
Author: Jacob Gero

This method runs if the user elects to plant only one plant in the garden. It lists different plants 
the user can enter, and if parameters are too high or low the program will send a method and a light signal
at the beginning of every iteration.

When the user selects a vegetable, the code will run the method with the accompanying vegetable. If an incorrect
value is used, the program will reject it and rerun until a correct value is reached.

Edit, 08 May 2020: I added a new feature that allows the user to quit the program. This has not been tested, but should work.
'''
def singlePlanner(): 
    print("Hello! What are you planting today?")
    print("1) Tomatoes")
    print("2) Beans")
    print("3) Peas")
    print("4) Corn")
    print("5) Squash")
    print("6) Other")
    print("Type 'q' to quit.")
    userVeggie = input("")
    if userVeggie in ['1)','1','Tomatoes','tomatoes']:
        print("Recommended temperature: between 18.3 and 29.4 C (65 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
        readArduinoTomato()
        q()
    elif userVeggie in ['2','2)','Beans','beans']:
        print("Recommended temperature: between 21 and 29.4 C (70 and 85F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
        readArduinoBean()
        q()
    elif userVeggie in ['3','3)','Peas','peas']:
        print("Recommended temperature: between 10 and 21 C (50 and 70F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
        readArduinoPea()
        q()
    elif userVeggie in ['4','4)','Corn','corn']:
        print("Recommended temperature: between 25 and 32.8 C (77 and 91F). ")
        print("Recommended Humidity: between 40 and 80 percent.")
        readArduinoCorn()
        q()
    elif userVeggie in ['5','5)','Squash','squash']:
        print("Recommended temperature: between 15.6C and 24C (60F and 75F). ")
        print("Recommended Humidity: between 40 and 60 percent.")
        readArduinoSquash()
        q()
    elif userVeggie in ['6','6)','Other','other']:
        readArduinoOther()
        q()
    elif userVeggie in ['q','Q','quit','Quit']:
        q()
    else:
        print("Please select a vegetable.")
        singlePlanner()         

'''
Method: main()
Author: Jacob Gero

This is the initial program. The reason this is a seperate method and not in the while true loop
was so that a user can return to this program if he/she wants to restart.

It asks if the user wishes to plant the same crop in the same area or not. The singlePlanner() module runs if the user 
hit a valid "yes" responce and helpfulPlanner() for a valid "no" response. If the user wishes to quite, he/she can
type "Quit" which will close the arduino ports and end the program.

'''
def main():
    print("Hello, welcome to the Helpful Garden Moderator! Five helpful stations will track air humidity, soil moisture, and temperature for your plants.")
    print("Are you planting the same crop at all stations? y/n")
    print("Press 'Q' to quit.")
    t = input("")
    if t in ['y','Y','Yes','yes']:
        singlePlanner()
    if t in ['n','No','N','no']:
        helpfulPlanner()
    if t in ['q','quit','Q','Quit']:
        print("Thank You!")
        time.sleep(2)
        arduino.close()
        arduino2.close()
        sys.exit()
    else:
        print("Please select yes, no, or quit.")
        
'''
while True calls the main() function, and the rest of the program will run until a sys.exit() command is reached.
'''
while True:
    main()
