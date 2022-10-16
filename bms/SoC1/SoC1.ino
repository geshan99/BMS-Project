float reading1;
float volt1;
float SoC1;
int analogpin1=A0;
float reading2;
float volt2;
float SoC2;
int analogpin2=A1;
String output;

void setup() {
  Serial.begin(9600);
}

void loop() {
 reading1=analogRead(analogpin1);
 volt1=(reading1/1023)*5;
 reading2=analogRead(analogpin2);
 volt2=(reading2/1023)*5;
 
 if (volt1>3.8){
  volt1=3.8;
  };
 if (volt1<3.5){
  volt1=3.51;
  };
 if (volt2>3.8){
  volt2=3.8;
  };
 if (volt2<3.5){
  volt2=3.51;
  };
  
  
 Serial.print(volt1);
 Serial.print(',');
 Serial.print(volt2);
 Serial.print('\n');
 
 delay(5000);

}
