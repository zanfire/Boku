
#include <Ethernet.h>
#include <SPI.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 2 
#define MQTT_CLIENTID "ArduinoCorridoi"
#define MQTT_PUBLISH_TOPIC_TEMPC "Telemetires\Rooms\1\TempC"
#define MQTT_PUBLISH_TOPIC_HUMIDITY "Telemetires\Rooms\1\Humidity"
#define MQTT_SERVER "192.168.0.195"

DHT dht(DHTPIN);

byte mac[] = { 0x90, 0xA2, 0xDA, 0x0D, 0xD9, 0x97 };
byte my_ip[] = { 192, 168, 1, 200 }; // google will tell you: "public ip address"

EthernetClient ethClient;
PubSubClient client(MQTT_SERVER, 1883, callback, ethClient);

unsigned long last_publish_ts = 0;

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
}

void startEthernet(){
  Serial.print("Initializing eth ... ");
  if (Ethernet.begin(mac) == 0) {
    Ethernet.begin(mac, my_ip);
    Serial.println(" ?? ok");
  }
  else Serial.println("ok"); 
  delay(1000);
}

void startMQTT(){
  Serial.print("Initializing mqtt client ... ");
  if (client.connect(MQTT_CLIENTID)) {
    Serial.println(" ok");
  }
  else Serial.println("failed"); 
}

void setup() {
  Serial.begin(9600);
  // Startup of Sensors, Ethernet and MQTT. 
  dht.begin();
  startEthernet();
  startMQTT();
}

void loop() {
  unsigned long now = millis();

  // Perform a read and publish each minute. NOTE this if handle the wrap around
  if (now - last_publish_ts >= 60000) {
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // check if returns are valid, if they are NaN (not a number) then something went wrong!
    if (isnan(t) || isnan(h)) {
      Serial.println("Failed to read from DHT");
    } 
    else {
      char buf[32];
      client.publish(MQTT_PUBLISH_TOPIC_TEMPC, dtostrf(t, 4, 2, buf));
      client.publish(MQTT_PUBLISH_TOPIC_HUMIDITY, dtostrf(h, 4, 2, buf));
      last_publish_ts = now;
    }
  }
  
  // Keep alive MQTT client.
  client.loop();
}

