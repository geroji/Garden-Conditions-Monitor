#include "dht.h"         //include dht library
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int dht_pin0 = A0;     // Analog Pin A0 of Arduino is connected to DHT11 out pin
int dht_pin1 = A1;
int dht_pin2 = A2;
int dht_pin3 = A3;
int dht_pin4 = A4;

int b0 = 11;
int r0 = 10;
int b1 = 9;
int r1 = 8;
int b2 = 7;
int r2 = 6;
int b3 = 5;
int r3 = 4;
int b4 = 3;
int r4 = 2;

dht DHT;

double TempC;     //define temperature variables
double TempC0;
double TempC1;
double TempC2;
double TempC3;
double TempC4;
double AvTempC;

double TempF;
double TempF0;
double TempF1;
double TempF2;
double TempF3;
double TempF4;
double AvTempF;

double Humid;
double Humid0;
double Humid1;
double Humid2;
double Humid3;
double Humid4;
double AvHumid;

int data;

void setup(){
  Serial.begin(9600);
  lcd.begin(2,16);
}
void loop(){
  
  DHT.read11(dht_pin0);
  Humid = DHT.humidity;
  Humid0 = Humid;
  TempC = DHT.temperature;
  TempC0 = TempC;
  TempF0 = (TempC0*1.8) + 32; 
//  Serial.println("Station 1 readings");
//  Serial.print("Humidity = ");
   Serial.println(Humid0);
//  Serial.println("%    ");
//  Serial.print("Temperature = ");
  Serial.println(TempC0); 
//  Serial.print(" C; ");
  Serial.println(TempF0);
//  Serial.println(" F");
//  Serial.println("");
  
  DHT.read11(dht_pin1);
  Humid = DHT.humidity;
  Humid1 = Humid;
  TempC = DHT.temperature;
  TempC1 = TempC;
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

  DHT.read11(dht_pin2);
  Humid = DHT.humidity;
  Humid2 = Humid;
  TempC = DHT.temperature;
  TempC2 = TempC;
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
  
  DHT.read11(dht_pin3);
  Humid = DHT.humidity;
  Humid3 = Humid;
  TempC = DHT.temperature;
  TempC3 = TempC;
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
  
  DHT.read11(dht_pin4);
  Humid = DHT.humidity;
  Humid4 = Humid;
  TempC = DHT.temperature;
  TempC4 = TempC;
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
  Serial.println(AvHumid);
  Serial.println(AvTempC);
//  Serial.print(" C; ");
  Serial.println(AvTempF);
//  Serial.println(" F");
//  Serial.print("Average Humidity: ");

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

Serial.flush();
  
}
