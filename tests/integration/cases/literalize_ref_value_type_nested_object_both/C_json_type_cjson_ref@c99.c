#include <cjson/cJSON.h>
int main(void) {
cJSON *_n8 = cJSON_CreateArray();
cJSON *_n9 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n8, _n9);
cJSON *_n10 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n8, _n10);
cJSON *shared = _n8;
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateArray();
cJSON *_n2 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_n1, _n2);
cJSON *_n3 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_n1, _n3);
cJSON_AddItemToObject(_n0, "field", _n1);
cJSON *my_data = _n0;
(void)my_data;
cJSON *_m4 = cJSON_CreateObject();
cJSON *_m5 = cJSON_CreateArray();
cJSON *_m6 = cJSON_CreateNumber((double)1);
cJSON_AddItemToArray(_m5, _m6);
cJSON *_m7 = cJSON_CreateNumber((double)2);
cJSON_AddItemToArray(_m5, _m7);
cJSON_AddItemToObject(_m4, "field", _m5);
my_data = _m4;
    (void)my_data;
    return 0;
}
