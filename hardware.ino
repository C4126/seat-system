//客户端
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Ticker.h>
#include <SPI.h>
#include <MFRC522.h>

constexpr uint8_t RST_PIN = D3;  // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = D8;   // Configurable, see typical pin layout above

MFRC522_SPI spiDevice = MFRC522_SPI(SS_PIN, RST_PIN);
MFRC522 mfrc522 = MFRC522(&spiDevice);  // Create MFRC522 instance

#define WIFISSID "Redmi_FA9A"
#define PASSWD "PASSWORD"

#define ID 1

const char* host = "";  //服务端的ip地址

Ticker flipper;
WiFiClient client;
#include "SSD1306Spi.h"
#define ID_LEN (sizeof(mfrc522.uid.uidByte) * 400)


/* 新建一个oled屏幕对象，需要输入IIC地址，SDA和SCL引脚号 */
SSD1306Spi oled(D0, D4, D1);

char status[100][100];

//发送心跳包（随意发送一次数据） 用于保持连接
void flip() {
  int n = 0;
  int cnt = 0;
  client.print("<get-status>");
  while (client.available() > 0) {
    char c = client.read();
    if (c == '<') n = 1;
    else if (c == ';' && n != -1 && n != 0) {
      status[n - 2][cnt] = 0;
      n++;
      cnt = 0;
    } else if (n == 1) {
      if (c - '0' != ID) {
        n = -1;
        continue;
      }
    } else if (n > 1) {
      status[n - 2][cnt] = c;
      cnt++;
    }
    Serial.write(c);
    if (c == '>') break;
    Serial.write(cnt + '0');
    Serial.write(n + '0');
  }
  status[n - 2][cnt - 1] = 0;
  Serial.write("current status:");
  Serial.write(status[0]);
  Serial.write(status[1]);
  Serial.write(status[2]);
  Serial.write(status[3]);
  Serial.write("end.\n");
}

void drawRect(void) {
  for (int16_t i = 0; i < oled.getHeight() / 2; i += 2) {
    oled.drawRect(i, i, oled.getWidth() - 2 * i, oled.getHeight() - 2 * i);
    oled.display();
    delay(50);
  }
}

void setup() {
  Serial.begin(115200);

  Serial.println("Initalizing OLED...\n");

  /* 2. oled屏幕初始化 */
  oled.init();
  oled.flipScreenVertically();  // 设置屏幕翻转
  oled.setContrast(255);        // 设置屏幕亮度
  Serial.println("Connecting...\n");
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFISSID, PASSWD);       // change it to your ussid and password
  mfrc522.PCD_Init();                 // Init MFRC522
  mfrc522.PCD_DumpVersionToSerial();  // Show details of PCD - MFRC522 Card Reader details
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
  drawRect();  // 测试屏幕显示
  oled.clear();
  oled.display();  // 清除屏幕

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  if (!client.connect("192.168.31.233", 1234))  //连接的IP地址和
  {
    Serial.println("Connection to host failed");
    delay(1000);
    return;
  }
  flipper.attach(10, flip);  //每隔180秒执行一次回调函数
}


char tag[ID_LEN] = { 0 };

char* check_for_card() {
  // Look for new cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return NULL;
  }

  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    Serial.println("Bad read (was card removed too quickly?)");
    return NULL;
  }

  if (mfrc522.uid.size == 0) {
    Serial.println("Bad card (size = 0)");
    return NULL;
  }
  tag[0] = 0;
  for (int i = 0; i < mfrc522.uid.size; i++) {
    char buff[5];  // 3 digits, dash and \0.
    snprintf(buff, sizeof(buff), "%s%d", i ? "-" : "", mfrc522.uid.uidByte[i]);
    strncat(tag, buff, sizeof(tag));
  };
  Serial.println("Good scan: ");
  Serial.println(tag);


  // disengage with the card.
  //
  mfrc522.PICC_HaltA();
  return tag;
}

void loop() {
  char* s = check_for_card();
  if (s != NULL) {
    client.print("<");
    client.print(ID);
    client.print(';');
    client.print(s);
    client.print(">");
  }

  oled.cls();
  oled.setFont(ArialMT_Plain_24);
  oled.drawString(0, 0, status[0]);
  oled.drawString(64, 0, status[1]);
  oled.drawString(0, 32, status[2]);
  oled.drawString(64, 32, status[3]);
  oled.display();

  delay(500);
}
