#define CurrentSensor A0
float sample;
float total;
float i;
float i_;
float avgAdcVoltage;

void setup() {
 Serial.begin(9600);
 pinMode(CurrentSensor,INPUT);
}

void loop() { 
readCurrent();
}
void readCurrent(){
  total=0;
  for (int ;i<300;i++){
    sample=analogRead(CurrentSensor);
    total=total+sample;
    }
  avgAdcVoltage=total/300; 
  avgAdcVoltage=avgAdcVoltage*5000/1024;
  i_=(avgAdcVoltage-2500)/100;
  i=i_*3.4558-3.2689;
  Serial.println(i_);
  Serial.println(i);
  delay(1000);
  }
