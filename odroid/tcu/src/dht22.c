#include "include/dht22.h"

DHTErrorCode check_pull_up(int pin){
  pinMode(pin, INPUT);
  delayMicroseconds(50);
  if(digitalRead( pin ) == LOW) {
    return DHT_NO_PULLUP;
  }
  return DHT_OK;
}

// ----------------------------------------------------------------------------

DHTErrorCode dht22_read(int pin, float *humidity, float *temperature){

  if(check_pull_up(pin) != DHT_OK){
    return     DHT_NO_PULLUP;
  }
  int j = 0;
  int counter = 0;
  int data[5] = { 0, 0, 0, 0, 0 };
  int laststate = HIGH;

  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
  delay(18);

  pinMode(pin, INPUT);

  for (int i = 0; i < MAX_TIMINGS; i++ )	{
    counter = 0;
    while ( digitalRead( pin ) == laststate )	{
      counter++;
      //delayMicroseconds( 1 );
      if ( counter == 255 )	{
        break;
      }
    }
    laststate = digitalRead( pin );

    if ( counter == 255 ){
      break;
    }

    if ( (i >= 4) && (i % 2 == 0) )	{
      data[j / 8] <<= 1;
      if ( counter > 100 ){
        data[j / 8] |= 1;
      }
      j++;
    }
  }

  if(j < 40){
    return DHT_NO_DATA;
  }

  if (data[4] != ( (data[0] + data[1] + data[2] + data[3]) & 0xFF) ){
    return DHT_BAD_CRC;
  }

  int raw_hum = ((int)data[0] << 8) + data[1];
  int raw_tmu = ((int) data[2] << 8) + data[3];

  if ( data[2] & 0x80 ) {
    raw_tmu = -raw_tmu;
  }

  *humidity = raw_hum / 10.0f;
  *temperature = raw_tmu / 10.0f;

  return DHT_OK;
}
