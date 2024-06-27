#include <esp_camera.h>

// Camera configuration
#define CAMERA_MODEL_WROVER_KIT // Has PSRAM
#include "camera_pins.h"

// Threshold value for red intensity detection
const int RED_INTENSITY_THRESHOLD = 230; // Adjust this value as needed

void setup() {
  // Start the serial communication
  Serial.begin(115200);
  
  // Give some time for the serial communication to start
  delay(1000);

  // Initialize the camera
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
  config.pixel_format = PIXFORMAT_GRAYSCALE; // Use grayscale format
  
  // Init with high specs to pre-allocate larger buffers
  if (psramFound()) {
    config.frame_size = FRAMESIZE_VGA;
    config.jpeg_quality = 20;  // 0-63 lower number means higher quality
    config.fb_count = 2;       // if more than one, i2s runs in continuous mode
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;  // 0-63 lower number means higher quality
    config.fb_count = 1;       // if more than one, i2s runs in continuous mode
  }
  
  // Camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return;
  }

  // Output success message
  Serial.println("Camera is working");
}

void loop() {
  // Capture a frame from the camera
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Check for red color in the captured frame and calculate average y-value
  int redPixelCount = 0;
  long sumYValue = 0;
  int width = fb->width;
  int height = fb->height;
  //Used to eliminate cases where 1-10 pixels will count as a margin of error
  int zeroThreshold = 10;
  //define a dictionary type structure for individual pixel distances
  //distanceDict = empty

  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int i = y * width + x;
      uint8_t intensity = fb->buf[i];
      
      // Check if the intensity corresponds to red
      if (intensity > RED_INTENSITY_THRESHOLD) {
        //calculate distance
        //distanceDict add {(x, y), DISTANCE}
        redPixelCount++;
        sumYValue += y;
      }
    }
  }

  // Calculate the average y-value if any red pixels are detected
  float avgYValue = (redPixelCount > zeroThreshold) ? (float)sumYValue / redPixelCount : 0;

  float centerDistance = 0;
  if (avgYValue > 0 && avgYValue <= 20) {
    centerDistance = (.05 * avgYValue);
  } else if (avgYValue > 20 && avgYValue <= 125) {
    centerDistance = (.01 * avgYValue) + 0.75;
  } else if (avgYValue > 125 && avgYValue <= 222) {
    centerDistance = (0.01 * avgYValue) + 0.7;
  } else if (avgYValue > 222 && avgYValue <= 340) {
    centerDistance = (0.0254 * avgYValue) - 2.65;
  } else if (avgYValue > 340 && avgYValue <= 388) {
    centerDistance = (0.0625 * avgYValue) - 15.25;
  } else if (avgYValue > 388) {
    centerDistance = (0.08333 * avgYValue) - 23.33;
  }

  // Output the number of high-intensity pixels detected
  if (redPixelCount < zeroThreshold) {
    Serial.println("Number of high-intensity pixels detected: 0");
    Serial.println("Average y-value: 0");
  } else {
    Serial.print("Number of high-intensity pixels detected: ");
    Serial.println(redPixelCount);

    // Output the average y-value
    Serial.print("Average y-value: ");
    Serial.println(avgYValue);

    // Output the average distance
    Serial.print("Average distance: ");
    Serial.println(centerDistance);    
  }

  //Output the distance dictionary somewhere?


  // Free the frame buffer memory
  esp_camera_fb_return(fb);

  // Delay before capturing the next frame
  delay(1000);
}
