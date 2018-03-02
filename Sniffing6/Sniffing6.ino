// by Ray Burnette 20161013 compiled on Linux 16.3 using Arduino 1.6.12

#include <ESP8266WiFi.h>
#include "./functions.h"



#define disable 0
#define enable  1
// uint8_t channel = 1;
unsigned int channel = 1;

// reporting settings
char reporting_ssid[] = "lab.dev";
char reporting_pass[] = "devlab123";
char reporting_ip[] = "10.0.0.9";
int reporting_timeout_seconds = 10;

int send_data() {

	char * ip = reporting_ip;
	uint32_t port = 30333;
	WiFiClient con;
	while (!con.connected()) {
		Serial.printf("Connecting to : %s ", ip);
		if (con.connect(ip, port)) {
			Serial.println("Success");
			break;  
		}
		Serial.println("Failure");
		delay(500);
	}
  Serial.println(WiFi.localIP());

      Serial.println("\n-------------------------------------------------------------------------------------\n");
      for (int u = 0; u < clients_known_count; u++) print_client(clients_known[u]);
      for (int u = 0; u < aps_known_count; u++) print_beacon(aps_known[u]);
      Serial.println("\n-------------------------------------------------------------------------------------\n");

  con.println(WiFi.macAddress());
  for (int u = 0; u < clients_known_count; u++) connection_print_client(clients_known[u], con);
  for (int u = 0; u < aps_known_count; u++) connection_print_beacon(aps_known[u], con);
	con.flush();
  con.stop();
  while(con.status() != 0){
    yield();
    if(con.connected()){
      con.~WiFiClient();
    }
  }
}


int report()
{
  wifi_promiscuous_enable(disable);
  Serial.println("Attempting to report");
  WiFi.begin(reporting_ssid, reporting_pass);

  int elapsed_time = 0;
  while((WiFi.status() != WL_CONNECTED) && (elapsed_time < reporting_timeout_seconds*1000))
  {
    delay(100);
    elapsed_time+=100;
    Serial.printf(".");
  }
  Serial.println("Connected");
  send_data();
  WiFi.disconnect();
  wifi_promiscuous_enable(enable);
}


void setup() {
  Serial.begin(57600);
  Serial.printf("\n\nSDK version:%s\n\r", system_get_sdk_version());
  Serial.println(F("ESP8266 mini-sniff by Ray Burnette http://www.hackster.io/rayburne/projects"));
  Serial.println(F("Type:   /-------MAC------/-----WiFi Access Point SSID-----/  /----MAC---/  Chnl  RSSI"));

  wifi_set_opmode(STATION_MODE);            // Promiscuous works only with station mode
  wifi_set_channel(channel);
  wifi_promiscuous_enable(disable);
  wifi_set_promiscuous_rx_cb(promisc_cb);   // Set up promiscuous callback
  wifi_promiscuous_enable(enable);
}

void loop() {
  channel = 1;
  wifi_set_channel(channel);
  while (true) {
    nothing_new++;                          // Array is not finite, check bounds and adjust if required
    if (nothing_new > 200) {
      nothing_new = 0;
      channel++;
      if (channel == 15)// Only scan channels 1 to 14
      {
        report();
        break;
      }
      wifi_set_channel(channel);
    }
    
    delay(1);  // critical processing timeslice for NONOS SDK! No delay(0) yield()
    // Press keyboard ENTER in console with NL active to repaint the screen
    if ((Serial.available() > 0) && (Serial.read() == '\n')) {
      Serial.println("\n-------------------------------------------------------------------------------------\n");
      for (int u = 0; u < clients_known_count; u++) print_client(clients_known[u]);
      for (int u = 0; u < aps_known_count; u++) print_beacon(aps_known[u]);
      Serial.println("\n-------------------------------------------------------------------------------------\n");
    }
  }
}



