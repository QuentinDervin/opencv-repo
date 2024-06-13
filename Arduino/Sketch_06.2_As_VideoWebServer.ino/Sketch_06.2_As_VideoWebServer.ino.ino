// Select camera model
#define CAMERA_MODEL_WROVER_KIT // Has PSRAM

#include <WiFi.h>
#include "esp_camera.h"
#include "camera_pins.h"
#include "app_httpd.h"


const char* ssid = "SHELL D0A029";
const char* password = "zAdRqTy6Y73YeTaR";

const char index_html[] = R"rawliteral(
<html>
  <head>
    <title>Camera Stream</title>
  </head>
  <body>
    <h1>Camera Stream</h1>
    <img src="/stream" />
  </body>
</html>
)rawliteral";

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_GRAYSCALE;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t* s = esp_camera_sensor_get();
  s->set_framesize(s, FRAMESIZE_VGA);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();
  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
}

void loop() {
  detectRedColor();
  delay(5000); // Check for red color every 5 seconds
}

void detectRedColor() {
  camera_fb_t* fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  uint16_t* image = (uint16_t*)fb->buf;
  int width = fb->width;
  int height = fb->height;
  bool red_detected = false;

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      uint16_t pixel = image[y * width + x];
      uint8_t r = (pixel >> 11) & 0x1F;
      uint8_t g = (pixel >> 5) & 0x3F;
      uint8_t b = pixel & 0x1F;

      if (r > 20 && g < 10 && b < 10) {
        red_detected = true;
        break;
      }
    }
    if (red_detected) {
      break;
    }
  }

  esp_camera_fb_return(fb);

  if (red_detected) {
    Serial.println("Red color detected!");
  } else {
    Serial.println("No red color detected.");
  }
}
