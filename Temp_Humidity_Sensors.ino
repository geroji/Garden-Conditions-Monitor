#include "dht.h"         //include dht library
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int dht_pin0 = A0;     // Analog Pins A0 - A4 of Arduino are connected to DHT11 out pins
int dht_pin1 = A1;    
int dht_pin2 = A2;
int dht_pin3 = A3;
int dht_pin4 = A4;

dht DHT; //defining the DHT variable from the library

double TempC;     //defining temperature variables
double TempC0;
double TempC1;
double TempC2;
double TempC3;
double TempC4;
double AvTempC;

double TempF;  //defining Farenheit temp variables
double TempF0;
double TempF1;
double TempF2;
double TempF3;
double TempF4;
double AvTempF;

double Humid; //defining humidity variables
double Humid0;
double Humid1;
double Humid2;
double Humid3;
double Humid4;
double AvHumid;

void setup(){
  Serial.begin(9600);
  lcd.begin(2,16);
}
void loop(){
  
  DHT.read11(dht_pin0); //Arduino reads pin A0 for DHT. . This is data from station 5.
  Humid0 = DHT.humidity; //humid0 stores humidity data for station #1 with DHT's humidity funtion
  TempC0 = DHT.temperature; //same with temperature data
  TempF0 = (TempC0*1.8) + 32; //converts to 
//  Serial.println("Station 1 readings"); //uncomment to read station one readings in serial moniter with labels. This is useful for
//  Serial.print("Humidity = ");          //determining if there are errors with DHT sensors
   Serial.println(Humid0); //prints humidity data to serial moniter, with Python will read
//  Serial.println("%    ");
//  Serial.print("Temperature = ");
  Serial.println(TempC0); //prints temp(C) data to serial mon.
//  Serial.print(" C; ");
  Serial.println(TempF0); //prints temp(F) data to serial monitor
//  Serial.println(" F");
//  Serial.println("");
  
  DHT.read11(dht_pin1); //Arduino reads pin A1 for DHT. This is data from station 2.
  Humid1 = DHT.humidity; //same process as above
  TempC1 = DHT.temperature;
  TempF1 = (TempC1*1.8) + 32;
//  Serial.println("Station 2 readings");
//  Serial.print("Humidity = ");
  Serial.println(Humid1);
//  Serial.println("%    ");
//  Serial.print("Temperature = ");
  Serial.println(TempC1); 
//  Serial.print(" C; ");
  Serial.println(TempF1);
//  Serial.println(" F");
//  Serial.println("");

  DHT.read11(dht_pin2); //Reads A2 pin for DHT data. This is data from station 3.
  Humid2 = DHT.humidity;
  TempC2 = DHT.temperature;
  TempF2 = (TempC2*1.8) + 32; 
//  Serial.println("Station 3 readings");
//  Serial.print("Humidity = ");
  Serial.println(Humid2);
// Serial.println("%    ");
// Serial.print("Temperature = ");
  Serial.println(TempC2); 
//  Serial.print(" C; ");
  Serial.println(TempF2);
//   Serial.println(" F");
//  Serial.println("");
  
  DHT.read11(dht_pin3); //Reads A3 pin for DHT data. This is data from station 4.
  Humid3 = DHT.humidity;
  TempC3 = DHT.temperature;
  TempF3 = (TempC3*1.8) + 32; 
//  Serial.println("Station 4 readings");
//  Serial.print("Humidity = ");
  Serial.println(Humid3);
//  Serial.println("%    ");
//  Serial.print("Temperature = ");
  Serial.println(TempC3); 
//  Serial.print(" C; ");
  Serial.println(TempF3);
//  Serial.println(" F");
//  Serial.println("");
  
  DHT.read11(dht_pin4); //Reads A4 pin for DHT data. This is data from station 5.
  Humid4 = DHT.humidity;
//  Humid4 = Humid;
  TempC4 = DHT.temperature;
//  TempC4 = TempC;
  TempF4 = (TempC4*1.8) + 32; 
//  Serial.println("Station 5 readings");
//  Serial.print("Humidity = ");
  Serial.println(Humid4);
//  Serial.println("%    ");
//  Serial.print("Temperature = ");
  Serial.println(TempC4); 
//  Serial.print(" C; ");
  Serial.println(TempF4);
//  Serial.println(" F");
//  Serial.println("");
//  Serial.println("--------------------------------------------");
  
  
  AvHumid = (Humid0 + Humid1 + Humid2 + Humid3 + Humid4)/5; 
  AvTempC = (TempC0 + TempC1 + TempC2 + TempC3 + TempC4)/5;
  AvTempF = (TempF0 + TempF1 + TempF2 + TempF3 + TempF4)/5;
  //  Serial.print("Average Humidity: ");
  Serial.println(AvHumid);
 //Serial.print(" %");
  //Serial.print("Average temps: ");
  Serial.println(AvTempC);
//  Serial.print(" C; ");
  Serial.println(AvTempF);
//  Serial.println(" F");


//Prints data for each station to LCD. Each station shows
//the current humidity for five seconds and temperature values
//for an additional five seconds. It then prints the average humidity
//values for five seconds and the average temperature for five seconds.
//Once this has cycled, the program will loop again. Because each value
// prints for five seconds, the program takes one minute to loop. 
//The timing of the LCD display is important because as soon as new data is written to the Serial Monitor, 
//the Python program will read it. Because the Arduino code takes one minute to run, the Arduino code prints
//new data to the Serial Monitor each minute, and thus the Python program reads and plots new data every minute.
lcd.setCursor(0,0);
lcd.print("Stat 1 Currently");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(Humid0);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(TempC0);
lcd.print(" C, ");
lcd.print(TempF0);
lcd.print(" F");
delay(5000);
lcd.clear();

lcd.setCursor(0,0);
lcd.print("Stat 2 Currently");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(Humid1);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(TempC1);
lcd.print(" C, ");
lcd.print(TempF1);
lcd.print(" F");
delay(5000);
lcd.clear();

lcd.setCursor(0,0);
lcd.print("Stat 3 Currently");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(Humid2);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(TempC2);
lcd.print(" C, ");
lcd.print(TempF2);
lcd.print(" F");
delay(5000);
lcd.clear();

lcd.setCursor(0,0);
lcd.print("Stat 4 Currently");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(Humid3);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(TempC3);
lcd.print(" C, ");
lcd.print(TempF3);
lcd.print(" F");
delay(5000);
lcd.clear();

lcd.setCursor(0,0);
lcd.print("Stat 5 Currently");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(Humid4);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(TempC4);
lcd.print(" C, ");
lcd.print(TempF4);
lcd.print(" F");
delay(5000);
lcd.clear();

lcd.setCursor(0,0);
lcd.print("Av. Current Cond");
lcd.setCursor(0,1);
lcd.print("Humid.: ");
lcd.print(AvHumid);
lcd.print(" %");
delay(5000);
lcd.clear();
lcd.setCursor(0,0);
lcd.print("Temperature:");
lcd.setCursor(0,1);
lcd.print(AvTempC);
lcd.print(" C, ");
lcd.print(AvTempF);
lcd.print(" F");
delay(5000);
lcd.clear();

  
}
