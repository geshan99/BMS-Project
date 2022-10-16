float val1 = 0;
float volt1_cal=0.0;
int analogpin1 =A0;
float volt1 =0.0;

void setup() {
  
Serial.begin(9600);

}

void loop() {
  
 val1=analogRead(analogpin1);
 volt1=(val1/1023)*5;
 volt1_cal=0.97638247*volt1+0.00276823+0.05888562*volt1*volt1;//after the calibration
 Serial.println(volt1);
 delay(5000);
}
