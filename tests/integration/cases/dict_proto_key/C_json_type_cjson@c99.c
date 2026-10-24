#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateObject();
cJSON *_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToObject(_n1, "x", _n2);
cJSON_AddItemToObject(_n0, "__proto__", _n1);
cJSON *_n3 = cJSON_CreateObject();
cJSON *_n4 = cJSON_CreateNumber((double)3);
cJSON_AddItemToObject(_n3, "__proto__", _n4);
cJSON_AddItemToObject(_n0, "n", _n3);
cJSON *_n5 = cJSON_CreateNumber((double)2);
cJSON_AddItemToObject(_n0, "y", _n5);
cJSON *my_data = _n0;
    (void)my_data;
    return 0;
}
