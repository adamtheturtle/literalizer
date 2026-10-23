#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("a\rb");
cJSON_AddItemToObject(_n0, "cr", _n1);
cJSON *_n2 = cJSON_CreateString("a\r\nb");
cJSON_AddItemToObject(_n0, "crlf", _n2);
cJSON *_n3 = cJSON_CreateString("a\nb");
cJSON_AddItemToObject(_n0, "lf", _n3);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
