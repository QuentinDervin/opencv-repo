#ifndef APP_HTTPD_H
#define APP_HTTPD_H

#include "esp_http_server.h"

extern httpd_handle_t stream_httpd;
extern httpd_handle_t camera_httpd;

void startCameraServer();

#endif // APP_HTTPD_H
