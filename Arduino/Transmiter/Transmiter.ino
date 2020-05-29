#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

RH_ASK driver;

#define INDEX_FINGER 2
#define MIDDLE_FINGER 3
#define RING_FINGER 4
#define BABY_FINGER 5
#define LED 8

#define ACTIVE LOW

void setup()
{
    Serial.begin(9600);    // Debugging only
    if (!driver.init())
         Serial.println("init failed");

    pinMode(INDEX_FINGER, INPUT_PULLUP);
    pinMode(MIDDLE_FINGER, INPUT_PULLUP);
    pinMode(RING_FINGER, INPUT_PULLUP);
    pinMode(BABY_FINGER, INPUT_PULLUP);
    pinMode(LED, OUTPUT);
}

void loop()
{
    int index_finger_status = digitalRead(INDEX_FINGER);
    int middle_finger_status = digitalRead(MIDDLE_FINGER);
    int ring_finger_status = digitalRead(RING_FINGER);
    int baby_finger_status = digitalRead(BABY_FINGER);

    if(index_finger_status == ACTIVE){
      Serial.println("INDEX ACTIVE");
      sendCommand("I");
    }

    else if(middle_finger_status == ACTIVE){
      Serial.println("MIDDLE ACTIVE");
      sendCommand("M");
    }

    
    else if(ring_finger_status == ACTIVE){
      Serial.println("RING ACTIVE");
      sendCommand("R");
    }

    
    else if(baby_finger_status == ACTIVE){
      Serial.println("BABY ACTIVE");
      sendCommand("B");
    }
}

void sendCommand(const char *command){
  digitalWrite(LED, 1);
  const char *msg = command;
  driver.send((uint8_t *)msg, strlen(msg));
  driver.waitPacketSent();
  delay(1000);
  digitalWrite(LED, 0);
}
