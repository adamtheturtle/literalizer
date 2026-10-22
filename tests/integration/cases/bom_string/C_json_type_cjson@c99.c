#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("﻿");
cJSON_AddItemToObject(_n0, "x", _n1);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
