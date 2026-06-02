#include <cjson/cJSON.h>
int main(void) {
cJSON *_n0 = cJSON_CreateObject();
cJSON *_n1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_n0, "name", _n1);
cJSON *_n2 = cJSON_CreateArray();
cJSON *_n3 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(_n2, _n3);
cJSON *_n4 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(_n2, _n4);
cJSON *_n5 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(_n2, _n5);
cJSON_AddItemToObject(_n0, "scores", _n2);
cJSON *my_data = _n0;
(void)my_data;
cJSON *_m0 = cJSON_CreateObject();
cJSON *_m1 = cJSON_CreateString("Alice");
cJSON_AddItemToObject(_m0, "name", _m1);
cJSON *_m2 = cJSON_CreateArray();
cJSON *_m3 = cJSON_CreateNumber((double)10);
cJSON_AddItemToArray(_m2, _m3);
cJSON *_m4 = cJSON_CreateNumber((double)20);
cJSON_AddItemToArray(_m2, _m4);
cJSON *_m5 = cJSON_CreateNumber((double)30);
cJSON_AddItemToArray(_m2, _m5);
cJSON_AddItemToObject(_m0, "scores", _m2);
my_data = _m0;
    (void)my_data;
    return 0;
}
