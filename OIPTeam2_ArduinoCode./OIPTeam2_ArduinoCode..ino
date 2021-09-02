#include <Servo.h>
#include "DHT.h"

#define sensorPower 52
#define sensorPin A5
#define DHTPIN 40
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

int j = 10; //10 sec for dry
int k = 10; //10 sec for sterilize led
int t = 10; // 10 sec wash
int x = 10; // led bottom solenoid valve
int y = 10; // led top solenoid valve
int val = 0; // water level sensor
int pos = 90; // pos of servo
int humval = 0; // recorded humidity value before closing lid
String hum; // humidity
Servo servo_9;

int red_light_pin = 12;
int green_light_pin = 11;
int blue_light_pin = 10;

void setup() {
  // initialize digital pin  for the LED_BUILTIN as an output.
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(7, OUTPUT); // pump
  pinMode(6, OUTPUT); // fan
  pinMode(2, OUTPUT); // fan 2
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
  pinMode(sensorPower, OUTPUT); //water level sensor power
  digitalWrite(sensorPower, LOW);
  servo_9.attach(9);
  Serial.println(F("DHT11 test!"));
  dht.begin();
  Serial.println("Program Start");
  digitalWrite(44, HIGH);
  pinMode(48, OUTPUT); // led solenoid top
  pinMode(46, OUTPUT); // led ultrasonic cleaner
  pinMode(44, OUTPUT); // led solenoid bottom

}

const int LightLevelToSwitchAt = 100; //set to about 20 percent of scale


// the loop function runs forever, reading the light level and turning on the LED if its dark

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() == 0) // start serial comm
  {
    int LightValue = analogRead(A0); //read lightvalue
    Serial.println(LightValue); //print lightvalue
    unlock(); //unlock lid
    RGB_color (255, 225, 0); //yellow
    if (LightValue > 100) { // if lux exceed
      Serial.println("lid_open"); // Lid is open! Process cannot start!
      int humval = humidity(h); // save humidity level 
      delay (1000);
    }
    if (LightValue < 100) {
      Serial.println("lid_closed"); // Lid is open! Process cannot start!
      while (LightValue < 100) { //while lux below
        delay(500);

        String data = (Serial.readStringUntil('\n')); //start reading from rbp

        if (data == "fill") //if receive, run
        {
        Serial.print("Mode Received to be:  ");
        Serial.println(data);
          fill2();
        }
        else if (data == "dry") //if receive, run
        {
        Serial.print("Mode Received to be:  "); 
        Serial.println(data);
          drying ();
        }

        else if (data == "sterilize") //if receive, run
        {
        Serial.print("Mode Received to be:  ");
        Serial.println(data);
          sterilize ();
        }
        else if (data == "full") //if receive, run
        {
          fill2 ();
          delay (1000);
          drying ();
          delay (1000);
          sterilize ();
        }
        else if (data == "done") //if receive, run
        {
          unlock();
          break;
        }
        else if (data == "humidity")
        {
          delay (1000);
          humidity ();
        }

        else {
          //.println("Nothing Recevied, still waiting");
          delay (500);
        }
      }
    }
  }
  else {
    Serial.println("Communication Error!");
    delay (500);
  }
}



void RGB_color(int red_light_value, int green_light_value, int blue_light_value)
{
  analogWrite(red_light_pin, red_light_value);
  analogWrite(green_light_pin, green_light_value);
  analogWrite(blue_light_pin, blue_light_value);
}

void lock () { //lock lid
  servo_9.write(90);
  delay(1000);
}

void unlock () { // unlock lid
  servo_9.write(0);
  delay(1000);
}

void drying () {  // run both fans
  for (j = 30; j > 0; j--) { 
    digitalWrite(6, HIGH);
    digitalWrite(2, HIGH);
    Serial.print("drying is ");
    RGB_color(255, 0, 235); //pink
    Serial.println(j);
    delay(1000);
  }
  if (j == 0) {  // when fans done return
    digitalWrite(6, LOW);
    digitalWrite(2, LOW);
    Serial.println("drying is done");
    RGB_color(255, 0, 235); //pink;
  }
}

void sterilize () { // run led
  for (k = 30; k > 0; k--) {
    RGB_color (255, 0, 0); //red
    digitalWrite(5, HIGH);
    Serial.print("sterilizing is ");
    Serial.println(k);
    delay(1000);
  }
  if (k == 0) { // when led done return
    digitalWrite(5, LOW);
    delay(500);
    Serial.println("Process is done!");
    RGB_color (0, 0, 255); //green
  }
}


void fill2() {  //run full washing cycle
  lock();
  RGB_color(255, 0, 235); //pink
  int level = readSensor();
  Serial.print("Water level: ");
  Serial.println(level);
  for (y = 25; y > 0; y--) {
    digitalWrite(7, HIGH); // on pump
    digitalWrite(48, HIGH); // open top solenoid
    digitalWrite(44, HIGH); // flush bottom
    Serial.print("flushing system done in"); //return string 
    Serial.println (y);
    delay(1000);
  }
  if (y == 0) { // when flushing done
    digitalWrite(44, LOW); // close bottom solenoid
  }
  if (level < 300) { 
    while (level < 300) { // while the level is less than 300
      int level = readSensor(); // keep reading sensor 
      Serial.println(level);
      delay(300);
      if (level > 300) { //if level exceeds value
        digitalWrite(7, LOW);  //stop pump
        digitalWrite(48, LOW); // close top solenoid
        Serial.println("filling_done"); //return string 
        for (t = 20; t > 0; t--) { // countdown us cleaner
          digitalWrite(46, HIGH); // turn on us cleaner
          Serial.print("Ultrasonic done in"); //return string 
          Serial.println (t);
          delay(1000);
        }
        if (t == 0) { 
          digitalWrite(46, LOW); // turn off us cleaner
          Serial.println("Ultrasonic done!"); //return string 
          for (x = 10; x > 0; x--)
          {
            Serial.print("draining water in"); //return string 
            Serial.println(x);
            digitalWrite(44, HIGH); // open bottom solenoid
            delay(1000);

          }
          break;
        }
      }

    }
  }
}


int readSensor() {
  digitalWrite(sensorPower, HIGH);  // Turn the sensor ON
  delay(10);              // wait 10 milliseconds
  val = analogRead(sensorPin);    // Read the analog value form sensor
  digitalWrite(sensorPower, LOW);   // Turn the sensor OFF
  return val;             // send current reading
}

int humidity() {
  //delay (1000);
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  if (humval > h) { // rmb change this!!!!
    hum = "dry";
  }
  else {
    hum = "dry";
  }
  //Serial.print("Humidity is: ");
  Serial.println(h);
  Serial.println(hum);
  delay(2000);
}
