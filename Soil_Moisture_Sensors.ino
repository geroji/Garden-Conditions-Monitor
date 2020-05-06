int soil_Mod0 = A0;
int soil_Mod1 = A1;
int soil_Mod2 = A2;
int soil_Mod3 = A3;
int soil_Mod4 = A4;

int soil_Moist0;
int soil_Moist1;
int soil_Moist2;
int soil_Moist3;
int soil_Moist4;

void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
 soil_Moist0 = analogRead(soil_Mod0);
 Serial.println(soil_Moist0);
 soil_Moist1 = analogRead(soil_Mod1);
 Serial.println(soil_Moist1);
 soil_Moist2 = analogRead(soil_Mod2);
 Serial.println(soil_Moist2);
 soil_Moist3 = analogRead(soil_Mod3);
 Serial.println(soil_Moist3);
 soil_Moist4 = analogRead(soil_Mod4);
 Serial.println(soil_Moist4);
 Serial.flush();
 delay(60000);
}
