#include "DHT.h"
#define MAX_ITER 10
#define DHTTYPE DHT22
DHT dht2(2, DHTTYPE);
int startbyte;
int i;
float auxTemp;
float auxHum;
float meanHum[3] = {0.0, 0.0, 0.0};
float meanTemp[3] = {0.0, 0.0, 0.0};
void setup()
{
  Serial.begin(9600);
  dht2.begin();
}
void loop()
{
  if (Serial.available() > 0)
  {
    startbyte = Serial.read();
    if (startbyte == 't')
    {
      meanHum[0] = 0.0;
      meanTemp[0] = 0.0;
      for (i=0;i<MAX_ITER;i++)
      {
        auxTemp = dht2.readTemperature();
        //auxHum = dht2.readHumidity();
        meanTemp[0] += auxTemp/(float)MAX_ITER;
        //meanHum[0] += auxHum/(float)MAX_ITER;
        delay(200);
      }
      Serial.print(meanTemp[0],4); Serial.print("\n");
      //Serial.print(meanHum[0],4); Serial.println("");
    
    }
  }
}
